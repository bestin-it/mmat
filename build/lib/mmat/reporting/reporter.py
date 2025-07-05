# MMAT Base Reporter
# Defines the base class for all MMAT reporters.

from abc import ABC, abstractmethod
from typing import Dict, Any

class Reporter(ABC):
    """
    Abstract base class for MMAT reporters.

    Reporters are responsible for collecting and presenting test results.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the reporter.

        Args:
            config: Configuration dictionary for the reporter.
        """
        self.config = config
        self.results: Dict[str, Any] = {}

    @abstractmethod
    async def start_suite(self, suite_name: str):
        """
        Called when a test suite starts.

        Args:
            suite_name: The name of the test suite.
        """
        pass

    @abstractmethod
    async def end_suite(self, suite_name: str):
        """
        Called when a test suite ends.

        Args:
            suite_name: The name of the test suite.
        """
        pass

    @abstractmethod
    async def start_case(self, suite_name: str, case_name: str):
        """
        Called when a test case starts.

        Args:
            suite_name: The name of the parent test suite.
            case_name: The name of the test case.
        """
        pass

    @abstractmethod
    async def end_case(self, suite_name: str, case_name: str, status: str, details: Dict[str, Any]):
        """
        Called when a test case ends.

        Args:
            suite_name: The name of the parent test suite.
            case_name: The name of the test case.
            status: The status of the test case (e.g., "passed", "failed", "skipped").
            details: A dictionary containing additional details about the test case result.
        """
        pass

    @abstractmethod
    async def publish_results(self):
        """
        Publishes or saves the collected test results.
        """
        pass

    # Add methods for handling test steps, assertions, etc., as needed
