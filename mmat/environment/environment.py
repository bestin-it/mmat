# MMAT Environment Base Class
# Defines the base class for all environments.

from typing import Any, Dict

class Environment:
    """
    Base class for MMAT Environments.

    Environments provide the interface for interacting with the system under test (SUT).
    Concrete environment classes should inherit from this base class and implement
    environment-specific logic.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the environment.

        Args:
            config: Configuration dictionary for the environment.
        """
        self.config = config
        # Add common environment initialization logic here if needed

    def connect(self) -> None:
        """
        Establishes a connection to the environment.

        This method should be implemented by concrete environment classes.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def disconnect(self) -> None:
        """
        Disconnects from the environment and performs cleanup.

        This method should be implemented by concrete environment classes.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def execute_step(self, step_type: str, step_config: Dict[str, Any]) -> Any:
        """
        Executes a specific test step within the environment.

        This method should be implemented by concrete environment classes to
        handle the execution of different step types.

        Args:
            step_type: The type of the test step to execute.
            step_config: Configuration dictionary for the test step.

        Returns:
            The result of the step execution.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # Add other common environment interaction methods here if needed
