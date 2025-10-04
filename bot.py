import os
import os

import sys
import traceback
from dotenv import load_dotenv

import discord
from discord.ext import commands

from utility.db.db import DatabaseClient
from utility.db.setup_db import setup_database

from utility.db.nsql import nSQL
from utility.config import load_config

from utility.logger import logger

# Muzyka
from utility.music import MusicManager

# Języki
from utility.lang_manager import LangManager

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=discord.Intents.all())
        self.db = DatabaseClient()
        
        self.config = load_config()
        if not self.config:
            logger.error("No config file!")
            self.config = {}
            
        self.dev_ids = self.config.get("dev_ids", []) or []
        self.dev_guild = self.config.get("dev_guild", 0) or 0
        
        # Muzyka
        #self.queue: dict[int, deque] = {} # guild_id -> queue object
        self.queue = nSQL(type=self.config.get("nsql", "dict") or "dict")
        self.musicManager = MusicManager(self)

        # Własne kanały
        self.own_channels: dict[int, int] = {} # user_id -> channel_id

        # Język
        self.lang_manager = LangManager()
        
    async def setup_hook(self):
        await self.__load_ffmepg()

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
                    await self.load_extension(module)
                except Exception as e:
                    logger.error(f"❌ Failed to load {module}: {e}\n{traceback.format_exc()}")
                except KeyboardInterrupt:
                    sys.exit(-1)

    @staticmethod
    async def __load_ffmepg() -> None:
        os.environ["PATH"] = os.path.abspath("bin") + os.pathsep + os.environ["PATH"]

    async def on_ready(self):
        assert self.user is not None, "Bot user is not set."
        await self.tree.sync()
        logger.info(f"Bot logged in as {self.user} (ID: {self.user.id})")

    async def close(self):
        await self.db.close()
        await super().close()

if __name__ == "__main__":
    bot = Bot()
    if discord.version_info.minor < 6:
        logger.error("discord.py version >2.6 required")
        exit()

    logger.info("Starting bot...")
    bot.run(TOKEN)
