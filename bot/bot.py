import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from bot.setup_db import setup_database
from bot.logger_config import logger

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def setup_hook():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # bot/
    PROJECT_ROOT = os.path.dirname(BASE_DIR)               # Majinali/
    COMMANDS_DIR = os.path.join(PROJECT_ROOT, "cogs", "commands")
    print(COMMANDS_DIR)
    EVENTS_DIR = os.path.join(PROJECT_ROOT, "cogs", "events")
    CONTEXT_DIR = os.path.join(PROJECT_ROOT, "cogs", "context")

    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading command: {filename[:-3]}")
            await bot.load_extension(f"cogs.commands.{filename[:-3]}")

    for filename in os.listdir(EVENTS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading event: {filename[:-3]}")
            await bot.load_extension(f"cogs.events.{filename[:-3]}")

    for filename in os.listdir(CONTEXT_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            logger.info(f"Loading context: {filename[:-3]}")
            await bot.load_extension(f"cogs.context.{filename[:-3]}")

    logger.info("All cogs loaded successfully.\033[0m")

@bot.event
async def on_ready():
    assert bot.user is not None, "Bot user is not set."
    await bot.tree.sync()
    logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    #setup_database()
    logger.info("Database setup complete.")
    bot.run(TOKEN)