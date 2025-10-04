from discord import app_commands, Interaction
from discord.ext import commands

from typing import Optional
from utility.lang_manager import LangManager

class CheckLocate(commands.Cog):
    dev_only = True
    def __init__(self, bot):
        self.bot = bot
        self.langManager: LangManager = self.bot.lang_manager

    @app_commands.command(name="check_locate", description="Check locate")
    async def check_locate(self, interaction: Interaction, lang: Optional[str], key: Optional[str]):
        v = ""
        if key and lang:
            v = self.langManager.t(lang, key)
            
        await interaction.response.send_message(f"{interaction.locale}\n{v}")
        
async def setup(bot):
    await bot.add_cog(CheckLocate(bot))
