import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from utils.music import MusicManager

class SkipMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager # type: ignore

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

        vc: discord.VoiceClient = guild.voice_client # type: ignore
        
        if not vc:
            return await interaction.response.send_message(
                "❌ Bot nie jest połączony z kanałem głosowym.", ephemeral=True
            )

        await interaction.response.defer()
        asyncio.create_task(self._skip_logic(vc, guild.id, interaction))

    async def _skip_logic(self, vc: discord.VoiceClient, guild_id: int, interaction: discord.Interaction):
        try:
            await self.musicManager.skip_current(vc, guild_id)

            await asyncio.sleep(0.1)

            queue = self.musicManager.queue.get(guild_id, [])
            next_title = None
            
            if queue and len(queue) > 0:
                next_title = queue[0]
                await interaction.followup.send(f"⏭️ Pominięto utwór. Następny w kolejce: **{next_title}** 🎶")
            else:
                await interaction.followup.send("⏭️ Pominięto utwór. Kolejka jest pusta ❌")
                await vc.disconnect()
        except Exception as e:
            await interaction.followup.send(f"❌ Wystąpił błąd przy pomijaniu utworu: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(SkipMusic(bot))
