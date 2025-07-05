from abc import ABC, abstractmethod

class TestStep(ABC):
    """
    Base class for all test steps.
    """
    def __init__(self, step_data, driver):
        """
        Initializes the base test step.

        Args:
            step_data (dict): Dictionary containing the step's configuration data.
            driver: The driver instance (e.g., PlaywrightDriver) to use for execution.
        """
        self.step_data = step_data
        self.driver = driver
        self.step_type = step_data.get("type", "unknown")
        self.description = step_data.get("description", f"Execute {self.step_type} step")
        print(f"[TestStep] Initialized step: {self.description}")

    @abstractmethod
    def execute(self):
        """
        Executes the test step. This method must be implemented by subclasses.

        Returns:
            bool: True if the step executed successfully, False otherwise.
        """
        pass

    def __str__(self):
        return f"Step Type: {self.step_type}, Description: {self.description}"

# Add other common methods or properties for test steps here
