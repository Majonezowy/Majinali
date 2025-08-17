import discord
from discord import app_commands
from discord.ext import commands

from views.gif_selector_view import GifView

# Replace with the user ID you want to allow
ALLOWED_USER_ID = 123456789012345678  

class SelectMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(
            name="Gif Selector",
            callback=self.gifSelect,
        )

        # Optional: limits where the command can be used
        self.ctx_menu.allowed_contexts = app_commands.AppCommandContext(
            guild=True,
            dm_channel=True,
            private_channel=True
        )

        self.bot.tree.add_command(self.ctx_menu)

    async def gifSelect(self, interaction: discord.Interaction, message: discord.Message):
        # Check if the user is allowed
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message(
                "❌ You are not allowed to use this command.",
                ephemeral=True
            )
            return

        view = GifView(message)
        await interaction.response.send_message(
            content="🎬 Wybierz GIF do wysłania:",
            view=view,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(SelectMenu(bot))
