# MMAT Logging Utility
# This file contains a simple logging utility for the framework.

import logging
import sys

# Configure basic logging
# You might want to make this configurable via the main config file later
logging.basicConfig(
    level=logging.INFO, # Default logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout # Log to console
)

class Logger:
    """
    A simple wrapper around the standard Python logging module.
    Provides a consistent way to get loggers throughout the framework.
    """
    def __init__(self, name: str):
        """
        Initializes the logger for a specific module or component.

        Args:
            name: The name of the logger (usually __name__ of the module).
        """
        self._logger = logging.getLogger(name)

    def debug(self, message: str) -> None:
        """Logs a debug message."""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """Logs an info message."""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Logs a warning message."""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """Logs an error message."""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """Logs a critical message."""
        self._logger.critical(message)

    # You could add methods for setting level, adding handlers, etc.
    # based on configuration if needed later.
