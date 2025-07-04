# MMAT Test Step Plugin
# Defines the base class for test step plugins.

from .plugin import Plugin
from ..core.test_step import TestStep # Assuming a base TestStep class exists
from typing import Dict, Any

class TestStepPlugin(Plugin):
    """
    Base class for MMAT Test Step Plugins.

    Test step plugins provide custom test step implementations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the test step plugin.

        Args:
            config: Configuration dictionary for the plugin.
        """
        super().__init__(config)

    def get_test_step_types(self) -> Dict[str, type]:
        """
        Returns a dictionary mapping test step type names to their classes.

        This method must be implemented by concrete test step plugins.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Add other common methods expected from test step plugins if needed
