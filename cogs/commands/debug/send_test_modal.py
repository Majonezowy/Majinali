from discord import app_commands, Interaction
from discord.ext import commands
import discord

from utility.creator import ModalCreator

data = {
    "title": "Przykład",
    "id-1": {
        "label": "Tekst na polem1",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "id-2": {
        "label": "Tekst na polem2",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "id-3": {
        "label": "Tekst na polem3",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "id-4": {
        "label": "Tekst na polem3",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "id-5": {
        "label": "Tekst na polem3",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "id-6": {
        "label": "Tekst na polem3",
        "placeholder": "Placeholder",
        "style": discord.TextStyle.short,
        "required": True,
        "min_length": 1,
        "max_length": 4000,
        "default": "domyslna wartosc",
        "row": None
    },
    "on_submit": lambda: ...
}

class SendTestModal(commands.Cog):    
    dev_only = True
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_test_modal", description="Send Test Modal")
    async def send_test_modal(self, interaction: Interaction):
        await interaction.response.send_modal(ModalCreator(data))
        
async def setup(bot):
    await bot.add_cog(SendTestModal(bot))
