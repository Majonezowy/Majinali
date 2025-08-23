import discord
from discord.ext import commands
from collections import deque
from typing import Optional, Any
import yt_dlp
import asyncio

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
        self.queue: dict[int, deque] = self.bot.queue  # type: ignore
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

                audio_formats = [f for f in info.get("formats", []) if f.get("acodec") != "none"] # type: ignore
                if not audio_formats:
                    return None

                stream_url = audio_formats[-1]["url"]
                title = info.get("title", "Unknown") # type: ignore
                return { "url": stream_url, "title": title, "id": info.get("id") } # type: ignore
        
        return await loop.run_in_executor(None, blocking_call)

    def add_to_queue(self, guild_id: int, query: str) -> None:
        if guild_id not in self.queue:
            self.queue[guild_id] = deque()
            
        self.queue[guild_id].append(query)

    def get_next_from_queue(self, guild_id: int) -> Optional[str]:
        if guild_id in self.queue and self.queue[guild_id]:
            return self.queue[guild_id][0]
        
        return None

    async def play_next(self, vc: discord.VoiceClient, guild_id: int) -> Optional[str]:
        if guild_id not in self.playing_locks:
            self.playing_locks[guild_id] = asyncio.Lock()
            
        if guild_id not in self.stopped:
            self.stopped[guild_id] = False

        async with self.playing_locks[guild_id]:
            if vc.is_playing() or self.stopped[guild_id]:
                return

            if guild_id not in self.queue or not self.queue[guild_id]:
                return await vc.disconnect()

            next_song = self.queue[guild_id][0]
            info = await self.fetch_info(next_song, ydl_opts)
            
            if not info:
                self.queue[guild_id].popleft()
                return await self.play_next(vc, guild_id)

            stream_url = info["url"]
            
            source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_opts) # type: ignore
            volume_source = discord.PCMVolumeTransformer(source, volume=self.volume)

            def after_playing(err):
                if self.stopped[guild_id]:
                    return 
                
                if guild_id in self.queue and self.queue[guild_id]:
                    self.queue[guild_id].popleft()
                    
                asyncio.run_coroutine_threadsafe(self.play_next(vc, guild_id), self.bot.loop)

            vc.play(volume_source, after=after_playing)
            return info["title"]

    def stop(self, vc: discord.VoiceClient, guild_id: int) -> None:
        if guild_id not in self.stopped:
            self.stopped[guild_id] = False
            
        self.stopped[guild_id] = True
        
        if guild_id in self.queue:
            self.queue[guild_id].clear()
            
        if vc.is_playing():
            vc.stop()

    def set_volume(self, volume: int, vc: Optional[discord.VoiceClient] = None) -> None:
        if volume < 0 or volume > 100:
            return
        
        self.volume = volume

        if vc and vc.is_playing() and isinstance(vc.source, discord.PCMVolumeTransformer):
            vc.source.volume = volume / 100

    async def skip_current(self, vc: discord.VoiceClient, guild_id: int) -> None:
        if guild_id not in self.playing_locks:
            self.playing_locks[guild_id] = asyncio.Lock()

        async with self.playing_locks[guild_id]:
            if vc.is_playing():
                vc.stop()

        

