import discord
from discord.ext import commands
from discord import app_commands

from utils.music import MusicManager

class StopMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore

    @app_commands.command(name="stop", description="Zatrzymuje muzykę")
    async def queue(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        vc = guild.voice_client # type: ignore
        await interaction.response.defer()
        if vc:
            self.musicManager.stop(vc=vc, guild_id=guild.id) # type: ignore
            await vc.disconnect(force=False)

        await interaction.followup.send("Zatrzymano muzykę!")


async def setup(bot: commands.Bot):
    await bot.add_cog(StopMusic(bot))
