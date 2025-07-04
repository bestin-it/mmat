import uuid
from typing import List, Dict, Any, Optional

from .test_case import TestCase

class TestSuite:
    """Represents a collection of test cases."""

    def __init__(
        self,
        name: str,
        test_cases: Optional[List[TestCase]] = None,
        suite_id: Optional[str] = None,
    ):
        """
        Initializes a TestSuite.

        Args:
            name: The name of the test suite.
            test_cases: A list of TestCase objects.
            suite_id: Unique identifier for the test suite. Generated if None.
        """
        self.suite_id = suite_id if suite_id is not None else str(uuid.uuid4())
        self.name = name
        self.test_cases = test_cases if test_cases is not None else []
        self.status: Optional[str] = None # 'pending', 'running', 'passed', 'failed', 'skipped'
        self.error: Optional[str] = None

    def add_test_case(self, test_case: TestCase):
        """Adds a test case to the suite."""
        self.test_cases.append(test_case)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TestSuite to a dictionary."""
        return {
            "suite_id": self.suite_id,
            "name": self.name,
            "test_cases": [case.to_dict() for case in self.test_cases],
            "status": self.status,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestSuite":
        """Creates a TestSuite from a dictionary."""
        test_cases = [TestCase.from_dict(case_data) for case_data in data.get("test_cases", [])]
        return cls(
            suite_id=data.get("suite_id"),
            name=data["name"],
            test_cases=test_cases,
        )

    def __repr__(self) -> str:
        return f"TestSuite(name='{self.name}', test_cases={len(self.test_cases)} cases)"
