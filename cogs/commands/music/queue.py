import discord
from discord.ext import commands
from discord import app_commands

from utils.music import MusicManager
from utils.lang_manager import LangManager

from cogs.views.music.queue import QueueView

class ShowQueue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore
        self.langManager: LangManager = self.bot.lang_manager # type: ignore

    @app_commands.command(name="queue", description="Wyświetla kolejkę")
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        guild = interaction.guild
        member = interaction.user
        locale = str(interaction.locale).split("-")[0]
        if guild is None:
            return

        queue = self.bot.queue.get(guild.id) # type: ignore
        if not queue:
            queue = self.langManager.t(locale, "music.queue_empty")
        view = QueueView(queue, locale, self.langManager)
        
        await interaction.followup.send(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowQueue(bot))
