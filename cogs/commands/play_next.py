import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp
from collections import deque
from typing import Optional, Any

class SkipMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager = self.bot.musicManager  # type: ignore

    @app_commands.command(name="skip", description="Pomija obecną piosenkę")
    async def skip(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        if guild is None:
            return

        member = guild.get_member(member.id)
        if not member or not member.voice or not member.voice.channel:
            return await interaction.response.send_message(
                "❌ Musisz być w kanale głosowym!", ephemeral=True
            )

        await interaction.response.defer()

        vc = guild.voice_client
        if not vc:
            return await interaction.followup.send("❌ Bot nie jest połączony z kanałem głosowym.")

        if vc.is_playing():
            vc.stop()

        await self.musicManager.play_next(vc, guild.id)

        queue = self.bot.queue.get(guild.id)
        if queue and len(queue) > 0:
            await interaction.followup.send("⏭️ Pominięto utwór. Gram następny w kolejce 🎶")
        else:
            await interaction.followup.send("⏭️ Pominięto utwór. Kolejka jest pusta ❌")


async def setup(bot: commands.Bot):
    await bot.add_cog(SkipMusic(bot))
