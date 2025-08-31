import discord
from discord.ext import commands
from discord import app_commands

from utils.music import MusicManager

class StopMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="stop", description="Zatrzymuje muzykę")
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild = interaction.guild
        locale = str(interaction.locale).split("-")[0]
        
        vc = guild.voice_client # type: ignore
        if vc:
            self.musicManager.stop(vc=vc, guild_id=guild.id) # type: ignore
            await vc.disconnect(force=False)

        await interaction.followup.send(self.langManager.t(locale, "music.stopped"))


async def setup(bot: commands.Bot):
    await bot.add_cog(StopMusic(bot))
