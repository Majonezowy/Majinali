import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
from collections import deque
from typing import Optional, Any
from utils.music import MusicManager
import asyncio

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

        vc = guild.voice_client
        
        if not vc:
            vc = await member.voice.channel.connect()
        else:
            await vc.move_to(member.voice.channel) # type: ignore

        self.musicManager.add_to_queue(guild.id, query)
        asyncio.create_task(self.musicManager.play_next(vc, guild.id)) # type: ignore
        queue_len = len(self.musicManager.queue.get(guild.id, []))
        
        if not vc.is_playing() and queue_len == 1: # type: ignore
            await interaction.followup.send(f"▶️ Gram teraz: **{query}**")
        else:
            await interaction.followup.send(f"➕ Dodano do kolejki: **{query}**")

    @play_music.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.errors.ConnectionClosed):
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayMusic(bot))
