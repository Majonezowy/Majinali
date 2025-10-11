from discord import ui, app_commands, Interaction
from discord.ext import commands
import discord

class SettingsView(ui.LayoutView):
    def __init__(self):
        super().__init__()

        # Just add the TextDisplay and Separator directly
        self.add_item(ui.TextDisplay('# Settings\n-# Example settings view'))
        self.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
        self.add_item(ui.Container(ui.TextDisplay("Test i chuj")))

class TestDb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test_db", description="Test Components v2 example [DEBUG]")
    async def test_db(self, interaction: Interaction):
        view = SettingsView()
        await interaction.response.send_message(
            view=view
        )

async def setup(bot):
    await bot.add_cog(TestDb(bot))
