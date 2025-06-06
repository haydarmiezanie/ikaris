import logging
from colorama import init, Fore, Style

# Initialize colorama for Windows and color support in terminal
init(autoreset=True)

class ColorFormatter(logging.Formatter):
    """
    Custom logging formatter that applies color to log levels.
    """
    def format(self, record):
        color = {
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.LIGHTRED_EX
        }.get(record.levelno, "")
        formatted_message = super().format(record)
        return f"{color}{formatted_message}{Style.RESET_ALL}"


def get_logger(name=__name__, level=logging.INFO):
    """
    Configures and returns a logger with colored output based on severity level.

    Parameters:
        name (str): Logger name.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        # Customize the format here if needed
        formatter = ColorFormatter("%(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
