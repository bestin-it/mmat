# MMAT Reporter Plugin
# Defines the base class for reporter plugins.

from .plugin import Plugin
from ..reporting.reporter import Reporter # Assuming a base Reporter class exists
from typing import Dict, Any

class ReporterPlugin(Plugin):
    """
    Base class for MMAT Reporter Plugins.

    Reporter plugins provide custom reporting mechanisms for test results.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the reporter plugin.

        Args:
            config: Configuration dictionary for the plugin.
        """
        super().__init__(config)

    def create_reporter(self) -> Reporter:
        """
        Creates and returns an instance of the specific reporter.

        This method must be implemented by concrete reporter plugins.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Add other common methods expected from reporter plugins if needed
