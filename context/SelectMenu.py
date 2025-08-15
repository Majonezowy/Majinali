import discord
from discord import app_commands
from discord.ext import commands

from views.gif_selector_view import GifView

class SelectMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.ctx_menu = app_commands.ContextMenu(
            name="Gif Selector",
            callback=self.gifSelect
        )

        self.ctx_menu.allowed_contexts = app_commands.AppCommandContext(
            guild=True,
            dm_channel=True,
            private_channel=True
        )

        self.ctx_menu.allowed_installs = app_commands.AppInstallationType(
            guild=True,
            user=True
        )

        self.bot.tree.add_command(self.ctx_menu)

    async def gifSelect(self, interaction: discord.Interaction, message: discord.Message):
        view = GifView(message)
        await interaction.response.send_message(
            content="🎬 Wybierz GIF do wysłania:",
            view=view,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(SelectMenu(bot))
