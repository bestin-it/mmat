# MMAT Model Plugin
# Defines the base class for model plugins.

from .plugin import Plugin
from ..models.reasoning_model import ReasoningModel # Assuming a base ReasoningModel class exists
from ..models.vision_model import VisionModel # Assuming a base VisionModel class exists
from typing import Dict, Any, Union

class ModelPlugin(Plugin):
    """
    Base class for MMAT Model Plugins.

    Model plugins provide interfaces for different AI models (reasoning, vision, etc.).
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the model plugin.

        Args:
            config: Configuration dictionary for the plugin.
        """
        super().__init__(config)

    def create_model(self, model_type: str) -> Union[ReasoningModel, VisionModel]:
        """
        Creates and returns an instance of the specific model based on type.

        Args:
            model_type: The type of model to create (e.g., 'reasoning', 'vision').

        This method must be implemented by concrete model plugins.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Add other common methods expected from model plugins if needed
