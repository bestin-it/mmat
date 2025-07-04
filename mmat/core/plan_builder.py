import yaml
import json
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

    def build_from_file(self, file_path: str) -> Union[TestSuite, TestCase]:
        """
        Loads test definition from a file and builds the test objects.

        Args:
            file_path: The path to the test definition file.

        Returns:
            A TestSuite or TestCase object.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file content is invalid or parsing fails.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test plan file not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.lower().endswith(('.yaml', '.yml')):
                    data = yaml.safe_load(f)
                elif file_path.lower().endswith('.json'):
                    data = json.load(f)
                else:
                    raise ValueError(f"Unsupported file format for test plan: {file_path}. Use .yaml, .yml, or .json")

            if not isinstance(data, dict):
                 raise ValueError(f"Invalid test plan file content: {file_path}. Content must be a dictionary.")

            return self.build_from_dict(data)

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing test plan file {file_path}: {e}")
        except Exception as e:
            # Catch other potential errors during file processing or build_from_dict
            raise ValueError(f"An error occurred while processing test plan file {file_path}: {e}")
