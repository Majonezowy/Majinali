import discord
from discord.ext import commands
from discord import app_commands

from utils.lang_manager import LangManager
from utils import logger
from cogs.permissions.is_dev import is_dev

class ClearCache(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="clear_cache", description="Usuwa cache z językami")
    @is_dev()
    async def clear_cache(self, interaction: discord.Interaction):
        self.langManager.cache = {}        
        
        return await interaction.followup.send("Lang cache cleared", ephemeral=True)
        
    @clear_cache.error
    async def play_music_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await logger.handle_error(interaction, error, self.langManager)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(ClearCache(bot))
