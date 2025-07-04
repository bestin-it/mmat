# MMAT Environment Plugin
# Defines the base class for environment plugins.

from .plugin import Plugin
from ..environment.environment import Environment # Assuming a base Environment class exists

class EnvironmentPlugin(Plugin):
    """
    Base class for MMAT Environment Plugins.

    Environment plugins provide the interface for interacting with the system
    under test (SUT).
    """

    def __init__(self, config):
        """
        Initializes the environment plugin.

        Args:
            config: Configuration dictionary for the plugin.
        """
        super().__init__(config)

    def create_environment(self) -> Environment:
        """
        Creates and returns an instance of the specific environment.

        This method must be implemented by concrete environment plugins.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Add other common methods expected from environment plugins if needed
    # e.g., connect, disconnect, cleanup, etc.
