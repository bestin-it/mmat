# MMAT Reasoning Model Interface
# Defines the interface for reasoning models used in MMAT.

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ReasoningModel(ABC):
    """
    Abstract base class for MMAT Reasoning Models.

    Reasoning models are responsible for analyzing structured data (like HTML DOM)
    and performing logical operations, such as generating test plans or identifying
    elements based on structure.
    """

    @abstractmethod
    def analyze_dom(self, dom_structure: str) -> Dict[str, Any]:
        """
        Analyzes the HTML DOM structure and extracts relevant information.

        Args:
            dom_structure: A string representation of the HTML DOM structure.

        Returns:
            A dictionary containing the analysis results (e.g., identified elements, structure).
        """
        pass

    @abstractmethod
    def generate_test_plan(self, description: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates a sequence of test steps based on a natural language description
        and current context (e.g., initial page state).

        Args:
            description: A natural language description of the test objective.
            context: A dictionary containing relevant context (e.g., start URL, test data).

        Returns:
            A list of dictionaries, where each dictionary represents a test step.
        """
        pass

    @abstractmethod
    def identify_element_by_structure(self, dom_structure: str, description: str) -> Dict[str, Any]:
        """
        Identifies a specific element within the DOM structure based on a description.

        Args:
            dom_structure: A string representation of the HTML DOM structure.
            description: A natural language description of the element to find.

        Returns:
            A dictionary containing information about the identified element (e.g., selector, attributes).
        """
        pass

    # Add other abstract methods as needed based on reasoning model capabilities
