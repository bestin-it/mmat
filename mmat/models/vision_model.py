# MMAT Vision Model Interface
# Defines the interface for vision models used in MMAT.

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

class VisionModel(ABC):
    """
    Abstract base class for MMAT Vision Models.

    Vision models are responsible for analyzing visual data (screenshots)
    and identifying elements based on their appearance.
    """

    @abstractmethod
    def analyze_screenshot(self, screenshot_path: str) -> Dict[str, Any]:
        """
        Analyzes a screenshot and extracts relevant visual information.

        Args:
            screenshot_path: The file path to the screenshot image.

        Returns:
            A dictionary containing the visual analysis results (e.g., layout, detected elements).
        """
        pass

    @abstractmethod
    def identify_element_visually(self, screenshot_path: str, description: str) -> Dict[str, Any]:
        """
        Identifies a specific element within a screenshot based on a description.
        This method is used for visual-only element identification (e.g., using BBOX, OCR).

        Args:
            screenshot_path: The file path to the screenshot image.
            description: A natural language description of the element to find.

        Returns:
            A dictionary containing information about the identified element,
            including visual references like BBOX coordinates, OCR text, or a textual description.
            Returns an empty dictionary or None if the element cannot be identified.
        """
        pass

    # Add other abstract methods as needed based on vision model capabilities
