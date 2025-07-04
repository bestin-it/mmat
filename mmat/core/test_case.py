# mmat/core/test_case.py

from typing import List, Optional
from mmat.core.test_step import TestStep

class TestCase:
    """
    Represents a single test case, composed of a sequence of test steps.
    """
    def __init__(self, name: str, description: Optional[str] = None, steps: Optional[List[TestStep]] = None):
        """
        Initializes a TestCase.

        Args:
            name: A unique name for the test case.
            description: An optional description of the test case's purpose.
            steps: A list of TestStep objects that make up the test case.
        """
        self.name = name
        self.description = description
        self.steps = steps if steps is not None else []
        self.status: Optional[str] = None # e.g., "passed", "failed", "skipped", "not_run"

    def add_step(self, step: TestStep):
        """
        Adds a test step to the test case.

        Args:
            step: The TestStep object to add.
        """
        self.steps.append(step)

    def __str__(self) -> str:
        return f"TestCase(name='{self.name}', status='{self.status}', steps={len(self.steps)})"

    def __repr__(self) -> str:
        return f"TestCase(name='{self.name}', description='{self.description}', steps={self.steps}, status='{self.status}')"

    def to_dict(self) -> dict:
        """
        Converts the TestCase object to a dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps] # Assuming TestStep has a to_dict method
        }
