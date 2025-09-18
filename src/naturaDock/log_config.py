
import logging
import sys
from pathlib import Path

def setup_logging(log_file: Path, verbose: bool):
    """
    Sets up logging for the application.

    Args:
        log_file: The path to the log file.
        verbose: Whether to enable verbose logging to the console.
    """
    log_file.parent.mkdir(exist_ok=True)

    # Create a logger
    logger = logging.getLogger("naturaDock")
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Log all messages to the file

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        console_handler.setLevel(logging.INFO)
    else:
        console_handler.setLevel(logging.WARNING)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Set the formatter for the handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
