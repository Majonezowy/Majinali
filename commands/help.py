import discord
from discord.ext import commands
from views.help_view import HelpView  # Import your view

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="pomoc", description="Displays a list of available commands.")
    async def abc(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Command 1", value="Description of command 1", inline=False)

        view = HelpView()
        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
