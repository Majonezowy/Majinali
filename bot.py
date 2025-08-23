import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from utils.db.db import DatabaseClient
from utils.db.setup_db import setup_database

from utils.logger_config import logger

# Muzyka
from utils.music import MusicManager
from collections import deque

# Języki
from utils.lang_manager import LangManager

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.db = DatabaseClient()

        # Muzyka
        self.queue: dict[int, deque] = {}
        self.musicManager = MusicManager(self)

        # Własne kanały
        self.own_channels: dict[discord.Member, int] = {}

        # Język
        self.lang_manager = LangManager()

    async def setup_hook(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # bot/
        COGS_DIR = os.path.join(BASE_DIR, "cogs")
        COMMANDS_DIR = os.path.join(COGS_DIR, "commands")
        EVENTS_DIR = os.path.join(COGS_DIR, "events")
        CONTEXTS_DIR = os.path.join(COGS_DIR, "contexts")

        # inicjalizacja bazy
        await setup_database(self.db)

        await self.__load_cogs(COMMANDS_DIR)
        await self.__load_cogs(EVENTS_DIR) 
        await self.__load_cogs(CONTEXTS_DIR)

        logger.info("All cogs loaded successfully.\033[0m")

    # async def __load_cogs(self, dir, type):
    #     for filename in os.listdir(dir):
    #        if filename.endswith(".py") and not filename.startswith("__"):
    #            logger.info(f"Loading {type}: {filename[:-3]}")
    #            await self.load_extension(f"cogs.{type}s.{filename[:-3]}")

    async def __load_cogs(self, base_dir="cogs"):
        for root, _, files in os.walk(base_dir):
            for file in files:
                if not file.endswith(".py") or file.startswith("__"):
                    continue
                
                full_path = os.path.join(root, file)

                module = os.path.relpath(full_path, start=".")
                module = module.replace(os.sep, ".").removesuffix(".py")

                logger.info(f"Loading cog: {module}")
                try:
                    await bot.load_extension(module)
                except Exception as e:
                    logger.error(f"❌ Failed to load {module}: {e}")

    async def on_ready(self):
        assert self.user is not None, "Bot user is not set."
        await self.tree.sync()
        logger.info(f"Bot logged in as {self.user} (ID: {self.user.id})")

    async def close(self):        
        await super().close()

if __name__ == "__main__":
    bot = Bot()
    logger.info("Starting bot...")
    print(discord.__version__)
    bot.run(TOKEN)
