import discord
from discord.ext import commands
from discord import app_commands
from utils.music import MusicManager

class ShowQueue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.musicManager: MusicManager = self.bot.musicManager  # type: ignore

    @app_commands.command(name="queue", description="Wyświetla kolejkę")
    async def queue(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        if guild is None:
            return

        queue = self.bot.queue.get(guild.id) # type: ignore
        await interaction.response.send_message(str(queue))

async def setup(bot: commands.Bot):
    await bot.add_cog(ShowQueue(bot))
