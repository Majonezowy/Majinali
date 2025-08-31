import discord
import os

from discord import app_commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

def is_dev():
    async def predicate(interaction: discord.Interaction) -> bool:
        dev_id = 1
        if not dev_id:
            return False
        return interaction.user.id == int(dev_id)
    
    return app_commands.check(predicate)