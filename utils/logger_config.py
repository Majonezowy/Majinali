import logging

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

        return f"{time_colored}  {level_colored}  {filename_colored}  {message_colored}"

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(ColorFormatter(datefmt="%Y-%m-%d %H:%M:%S", time_color_id=246))

logger.addHandler(console_handler)
