import discord
from discord.ext import commands
from discord import app_commands

from utility.music import MusicManager
from utility.lang_manager import LangManager
from utility import logger

class SetVolume(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="volume", description="Ustawia głośność od 0 do 100")
    async def volume(self, interaction: discord.Interaction, value: int):
        await interaction.response.defer()
        locale = str(interaction.locale).split("-")[0]
        
        if value <= 0 or value > 100:
          return await interaction.response.send_message(self.langManager.t(locale, "music.volume_not_in_range"), ephemeral=True)
        
        guild = interaction.guild
        if not guild:
            return
        vc = guild.voice_client # type: ignore
        if vc and vc.is_playing(): # type: ignore
            self.musicManager.set_volume(value, guild_id=guild.id, vc=vc) # type: ignore
        else:
            self.musicManager.set_volume(value, guild_id=guild.id)

        await interaction.response.send_message(self.langManager.t(locale, "music.volume_set", value=value))
        
    @volume.error
    async def on_volume_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await logger.handle_error(interaction, error, self.langManager)

async def setup(bot: commands.Bot):
    await bot.add_cog(SetVolume(bot))
