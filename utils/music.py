import discord
from discord.ext import commands
from collections import deque
from typing import Optional, Any
import yt_dlp
import asyncio

from typing import Optional
from bs4 import BeautifulSoup
import aiohttp
from youtubesearchpython import VideosSearch
import re

FFMPEG_PATH = "ffmpeg.exe"

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_at_eof 1',
    'options': '-vn'
}

ydl_opts = {
    "format": "bestaudio/best",
    "noplaylist": True
}
class MusicManager:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.queue: dict[int, deque] = self.bot.queue                                                                               # type: ignore
        self.volume: float = 1.0

        self.playing_locks: dict[int, asyncio.Lock] = {}
        self.stopped: dict[int, bool] = {}

    async def fetch_info(self, query: str, ydl_opts: dict[str, Any]) -> Optional[dict[str, Any]]:
        loop = asyncio.get_running_loop()
        if not query.startswith("http"):
            ydl_opts.update({"default_search": "ytsearch"})
        
        def blocking_call():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info: Optional[dict[str, Any]] = ydl.extract_info(query, download=False)
                if not info:
                    return None

                if "entries" in info and isinstance(info["entries"], list) and len(info["entries"]) > 0:
                    info = info["entries"][0]

                audio_formats = [f for f in info.get("formats", []) if f.get("acodec") != "none"]                                  # type: ignore
                if not audio_formats:
                    return None

                stream_url = audio_formats[-1]["url"]
                title = info.get("title", "Unknown")                                                                               # type: ignore
                return {"url": stream_url, "title": title, "id": info.get("id")}                                                   # type: ignore
        
        return await loop.run_in_executor(None, blocking_call)

    def fetch_video_url(self, query: str) -> Optional[str]:
        video_search = VideosSearch(query, limit=1)
        results = video_search.result()['result']                                                                                 # type: ignore
        if results:
            return results[0]['link']                                                                                             # type: ignore
        return None
    
    def add_to_queue(self, guild_id: int, query: str):
        if guild_id not in self.queue:
            self.queue[guild_id] = deque()
        self.queue[guild_id].append(query)

    def get_next_from_queue(self, guild_id: int):
        if guild_id in self.queue and self.queue[guild_id]:
            return self.queue[guild_id][0]
        return None

    async def play_next(self, vc: discord.VoiceClient, guild_id: int):
        if guild_id not in self.playing_locks:
            self.playing_locks[guild_id] = asyncio.Lock()
        if guild_id not in self.stopped:
            self.stopped[guild_id] = False

        async with self.playing_locks[guild_id]:
            if vc.is_playing() or self.stopped[guild_id]:
                return

            if guild_id not in self.queue or not self.queue[guild_id]:
                await vc.disconnect()
                return

            next_song = self.queue[guild_id][0]
            info = await self.fetch_info(next_song, ydl_opts)
            if not info:
                self.queue[guild_id].popleft()
                await self.play_next(vc, guild_id)
                return

            stream_url = info["url"]
            source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_opts)                                                          # type: ignore
            volume_source = discord.PCMVolumeTransformer(source, volume=self.volume)

            def after_playing(err):
                if self.stopped[guild_id]:
                    return 
                if guild_id in self.queue and self.queue[guild_id]:
                    self.queue[guild_id].popleft()
                asyncio.run_coroutine_threadsafe(self.play_next(vc, guild_id), self.bot.loop)
            try:
                vc.play(volume_source, after=after_playing)
            except discord.errors.ClientException:
                return
            return info["title"]

    def stop(self, vc: discord.VoiceClient, guild_id: int):
        if guild_id not in self.stopped:
            self.stopped[guild_id] = False
        self.stopped[guild_id] = True
        if guild_id in self.queue:
            self.queue[guild_id].clear()
        if vc.is_playing():
            vc.stop()

    def set_volume(self, volume: int, vc: Optional[discord.VoiceClient] = None):
        if volume < 0 or volume > 100:
            return
        
        self.volume = volume

        if vc and vc.is_playing() and isinstance(vc.source, discord.PCMVolumeTransformer):
            vc.source.volume = volume / 100

    async def skip_current(self, vc: discord.VoiceClient, guild_id: int):
        if guild_id not in self.playing_locks:
            self.playing_locks[guild_id] = asyncio.Lock()

        async with self.playing_locks[guild_id]:
            if vc.is_playing():
                vc.stop()
                
    async def fetch_metadata(self, url: str) -> dict[str, Optional[str | int]]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:                                                     # type: ignore
                html = await resp.text(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")

                # title
                title_tag = soup.find("meta", property="og:title") or soup.find("title")
                title = title_tag.get("content") if title_tag and title_tag.has_attr("content") else title_tag.string if title_tag else None  # type: ignore

                # description
                desc_tag = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
                description = desc_tag.get("content") if desc_tag and desc_tag.has_attr("content") else None# type: ignore

                # icon
                icon_tag = (
                    soup.find("link", rel="icon")
                    or soup.find("link", rel="shortcut icon")
                    or soup.find("link", rel="apple-touch-icon")
                )
                icon = icon_tag.get("href") if icon_tag and icon_tag.has_attr("href") else None # type: ignore

                # thumbnail
                thumbnail_tag = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
                thumbnail = thumbnail_tag.get("content") if thumbnail_tag and thumbnail_tag.has_attr("content") else None # type: ignore

                # duration (ISO 8601 -> sekundy)
                duration_tag = soup.find("meta", property="video:duration") or soup.find("meta", itemprop="duration")
                iso_duration = duration_tag.get("content") if duration_tag and duration_tag.has_attr("content") else None # type: ignore
                duration = self.parse_iso8601_duration(iso_duration) # type: ignore

                return {
                    "title": title, # type: ignore
                    "description": description,
                    "icon": icon,
                    "thumbnail": thumbnail,
                    "duration": duration,
                }

    @staticmethod
    def parse_iso8601_duration(duration: Optional[str]) -> str:
        if not duration:
            return "0:00"
        pattern = re.compile(
            r'P(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)'
        )
        match = pattern.match(duration)
        if not match:
            return "0:00"
        time_parts = match.groupdict()
        hours = int(time_parts.get("hours") or "0")
        minutes = int(time_parts.get("minutes") or "0")
        seconds = int(time_parts.get("seconds") or "0")
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
