# MMAT Base Plugin
# Defines the base class for all MMAT plugins.

from typing import Dict, Any

class Plugin:
    """
    Abstract base class for MMAT plugins.

    Plugins extend the functionality of the MMAT framework.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the plugin.

        Args:
            config: Configuration dictionary for the plugin.
        """
        self.config = config
        # Plugins can add custom logic, test steps, environments, etc.
        # Specific plugin types will inherit from this base class and implement
        # methods relevant to their functionality.
