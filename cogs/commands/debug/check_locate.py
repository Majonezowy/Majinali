from discord import ui, app_commands, Interaction
from discord.ext import commands
import discord

from typing import Optional
from utils.lang_manager import LangManager

class CheckLocate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="check_locate", description="Check locate")
    async def check_locate(self, interaction: Interaction, lang: Optional[str], key: Optional[str]):
        v = ""
        if key and lang:
            v = self.langManager.t(lang, key)
            
        await interaction.response.send_message(f"{interaction.guild_locale}\n{v}")
        
async def setup(bot):
    await bot.add_cog(CheckLocate(bot))
