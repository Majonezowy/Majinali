import discord
from discord.ext import commands
from discord import app_commands
from views.help_view import HelpView  # Import your view

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="stworz_ticket", description="Tworzy ticket view.")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.user_install()
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.checks.has_permissions(manage_channels=True)
    async def stworz_ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket",
            description="Wciśnij przycisk poniżej aby otworzyć ticket.",
            color=discord.Color.blue()
        )

        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
