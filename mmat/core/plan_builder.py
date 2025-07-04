from typing import Dict, Any, Union, List

from .test_case import TestCase
from .test_suite import TestSuite
from .test_step import TestStep

class PlanBuilder:
    """Builds test suites and test cases from test definitions."""

    def build_from_dict(self, data: Dict[str, Any]) -> Union[TestSuite, TestCase]:
        """
        Builds a TestSuite or TestCase from a dictionary representation.

        Args:
            data: A dictionary containing the test definition.

        Returns:
            A TestSuite or TestCase object.

        Raises:
            ValueError: If the data format is invalid.
        """
        if "test_cases" in data and isinstance(data["test_cases"], list):
            # Assume it's a TestSuite
            if "name" not in data:
                 raise ValueError("TestSuite dictionary must contain a 'name' key.")
            return TestSuite.from_dict(data)
        elif "steps" in data and isinstance(data["steps"], list):
            # Assume it's a TestCase
            if "name" not in data:
                 raise ValueError("TestCase dictionary must contain a 'name' key.")
            return TestCase.from_dict(data)
        else:
            raise ValueError("Invalid test definition format. Must contain 'test_cases' (for suite) or 'steps' (for case).")

    # Placeholder for building from file (e.g., YAML, JSON)
    # def build_from_file(self, file_path: str) -> Union[TestSuite, TestCase]:
    #     """
    #     Loads test definition from a file and builds the test objects.
    #
    #     Args:
    #         file_path: The path to the test definition file.
    #
    #     Returns:
    #         A TestSuite or TestCase object.
    #
    #     Raises:
    #         FileNotFoundError: If the file does not exist.
    #         ValueError: If the file content is invalid.
    #     """
    #     # Placeholder logic: read file, parse content (e.g., YAML/JSON), then call build_from_dict
    #     print(f"Loading test definition from {file_path} (placeholder)")
    #     # Example:
    #     # with open(file_path, 'r') as f:
    #     #     import yaml # or json
    #     #     data = yaml.safe_load(f) # or json.load(f)
    #     # return self.build_from_dict(data)
    #     pass
