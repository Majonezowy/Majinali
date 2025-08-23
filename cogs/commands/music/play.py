import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
from collections import deque
from typing import Optional, Any
from utils.music import MusicManager
import asyncio

FFMPEG_PATH = "ffmpeg.exe"

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_at_eof 1',
    'options': '-vn'
}

async def fetch_info(query: str, ydl_opts: dict[str, Any]) -> Optional[dict[str, Any]]:
    """
    Pobiera informacje o utworze z YouTube w osobnym wątku, aby nie blokować event loop.
    """
    loop = asyncio.get_running_loop()
    
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
            return {"url": stream_url, "title": title, "id": info.get("id")} # type: ignore
    
    return await loop.run_in_executor(None, blocking_call)
class PlayMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore

    @app_commands.command(name="play", description="Odtwórz muzykę z linku (YouTube/SoundCloud)")
    @app_commands.describe(query="Nazwa lub URL piosenki")
    async def play_music(self, interaction: discord.Interaction, query: str):
        guild = interaction.guild
        member = interaction.user
        if guild is None:
            return

        member = guild.get_member(member.id)
        if not member or not member.voice or not member.voice.channel:
            return await interaction.response.send_message("❌ Musisz być w kanale głosowym!", ephemeral=True)

        await interaction.response.defer()

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True
        }

        if not query.startswith("http"):
            ydl_opts.update({'default_search': 'ytsearch'})

        result = await fetch_info(query, ydl_opts)
        if result is None:
            return await interaction.followup.send("❌ Nie udało się pobrać audio.")

        stream_url = result["url"]
        title = result["title"]
        yt_link = f"https://www.youtube.com/watch?v={result['id']}"

        vc = guild.voice_client
        if not vc:
            vc = await member.voice.channel.connect()
        else:
            await vc.move_to(member.voice.channel) # type: ignore

        self.musicManager.add_to_queue(guild.id, stream_url)

        if not vc.is_playing(): # type: ignore
            await self.musicManager.play_next(vc, guild.id) # type: ignore
            yt_link = f"https://www.youtube.com/watch?v={result['id']}"
            await interaction.followup.send(f"▶️ Gram teraz: [**{title}**]({yt_link})")
        else:
            await interaction.followup.send(f"➕ Dodano do kolejki: **{title}**")

    @play_music.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.errors.ConnectionClosed):
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayMusic(bot))
