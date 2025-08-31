import logging
import discord
from discord import app_commands
import traceback

from typing import Optional

from utils.lang_manager import LangManager
from utils.config import load_config

data = load_config()
def get_level(data):
    
    if not data:
        return logging.DEBUG
    
    logging_data = data.get("logging", None)
    
    if not logging_data:
        return logging.DEBUG
    
    level_name = logging_data.get("level", logging.DEBUG)
    
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return levels.get(level_name.upper(), logging.DEBUG)

try:
    import colorama
    colorama.just_fix_windows_console()
except ImportError:
    pass

# ANSI codes
BOLD = "\033[1m"
RESET = "\033[0m"

COLORS = {
    'DEBUG': '\033[94m',          # Blue
    'INFO': '\033[92m',           # Green
    'WARNING': '\033[93m',        # Yellow
    'ERROR': '\033[91m',          # Red
    'CRITICAL': '\033[95m',       # Magenta
    'FILENAME': '\033[35m',       # Purple
    'MESSAGE': "\033[38;5;231m",  # Gray
}

def color256(id_: int) -> str:
    return f"\033[38;5;{id_}m"

class ColorFormatter(logging.Formatter):
    def __init__(self, datefmt=None, time_color_id=246):
        super().__init__(datefmt=datefmt)
        self.time_color = color256(time_color_id)

    def format(self, record):
        msg_plain = record.getMessage()

        asctime_plain = self.formatTime(record, self.datefmt)
        time_colored = f"{BOLD}{self.time_color}{asctime_plain}{RESET}"

        level_col = COLORS.get(record.levelname, "")
        level_colored = f"{BOLD}{level_col}{record.levelname}{RESET}\t"

        filename_colored = f"{COLORS['FILENAME']}{record.filename}{RESET}"

        message_colored = f"{COLORS['MESSAGE']}{msg_plain}{RESET}"

        return f"{time_colored} {level_colored}  {filename_colored}  {message_colored}"

logger = logging.getLogger("Majinali")
level = get_level(data)
logger.setLevel(level)

console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(ColorFormatter(datefmt="%Y-%m-%d %H:%M:%S", time_color_id=246))

logger.addHandler(console_handler)

async def handle_error(interaction: discord.Interaction, error: app_commands.AppCommandError, lang_manager: LangManager):
    try:
        member = interaction.user
        locale = str(interaction.locale).split("-")[0]
        
        if not lang_manager:
            logger.error("No langmanager")
            return
        
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            content = lang_manager.t(locale, "command_on_cooldown", time=f"{error.retry_after:.2f}")
        elif isinstance(error, app_commands.CheckFailure):
            content = lang_manager.t(locale, "no_permissions")
        elif isinstance(error, app_commands.CommandNotFound):
            content = lang_manager.t(locale, "command_not_found")
        else:
            content = lang_manager.t(locale, "error")
            
        if member.id == 693544583891517600:
            content += f"\n{str(error)}"
        
        if not interaction.response.is_done():
            await interaction.response.send_message(content, ephemeral=True)
        else:
            await interaction.followup.send(content, ephemeral=True)
    except Exception as e:
        logger.error(f"{e}\n{traceback.format_exc()}")
        
