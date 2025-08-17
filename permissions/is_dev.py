import discord
import os

from discord import app_commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="./../.env")



def is_dev():
    """Returns a check allowing only the dev to run the command."""
    async def predicate(interaction: discord.Interaction) -> bool:
        dev_id = os.getenv("dev_id")
        if not dev_id:
            return False
        return interaction.user.id == int(dev_id)
    
    return app_commands.check(predicate)