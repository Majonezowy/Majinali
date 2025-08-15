import discord
from discord.ext import commands

class Category(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #@commands.hybrid_command(name="pomoc", description="Displays a list of available commands.")
    #async def command(self, ctx: commands.Context):
        ...

async def setup(bot: commands.Bot):
    await bot.add_cog(Category(bot))
