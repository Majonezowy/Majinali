import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
from collections import deque
from typing import Optional, Any
from utils.music import MusicManager

FFMPEG_PATH = "ffmpeg.exe"

ffmpeg_opts = {
    'before_options': '-re -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

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
            "format": "bestaudio[abr<=64]",  # audio o bitrate maks. 64 kbps
            "noplaylist": True
        }
        if not query.startswith("http"):
            ydl_opts.update({'default_search': 'ytsearch'})

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info: Optional[dict[str, Any]] = ydl.extract_info(query, download=False)
                if not info:
                    return await interaction.followup.send("❌ Nie znalazłem niczego pasującego do zapytania.")
                
                if "entries" in info and isinstance(info["entries"], list) and len(info["entries"]) > 0:
                    info = info["entries"][0]

                # wybierz najlepszy format audio
                audio_formats = [f for f in info.get("formats", []) if f.get("acodec") != "none"]
                if not audio_formats:
                    return await interaction.followup.send("❌ Nie udało się znaleźć formatu audio.")

                # najlepszy audio stream
                stream_url = audio_formats[-1]["url"]
                title = info.get("title", "Unknown")

                if not stream_url:
                    return await interaction.followup.send("❌ Nie udało się uzyskać URL streamu.")
        except Exception as e:
            return await interaction.followup.send(f"❌ Błąd pobierania: {e}")

        vc = guild.voice_client
        if not vc:
            vc = await member.voice.channel.connect()
        else:
            await vc.move_to(member.voice.channel)

        self.musicManager.add_to_queue(guild.id, stream_url)

        if not vc.is_playing():
            await self.musicManager.play_next(vc, guild.id)
            yt_link = f"https://www.youtube.com/watch?v={info.get('id')}"
            await interaction.followup.send(f"▶️ Gram teraz: [**{title}**]({yt_link})")
        else:
            await interaction.followup.send(f"➕ Dodano do kolejki: **{title}**")

    @play_music.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.errors.ConnectionClosed):
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayMusic(bot))
