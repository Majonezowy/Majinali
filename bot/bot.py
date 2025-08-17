import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from setup_db import setup_database
from logger_config import logger

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def setup_hook():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading command: {filename[:-3]}")
            await bot.load_extension(f"commands.{filename[:-3]}")
    
    for filename in os.listdir("./events"):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading event: {filename[:-3]}")
            await bot.load_extension(f"events.{filename[:-3]}")
    
    for filename in os.listdir("./context"):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading context: {filename[:-3]}")
            await bot.load_extension(f"context.{filename[:-3]}")

    logger.info("All cogs loaded successfully.\033[0m")

@bot.event
async def on_ready():
    assert bot.user is not None, "Bot user is not set."
    await bot.tree.sync()
    logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    setup_database()
    logger.info("Database setup complete.")
    bot.run(TOKEN)