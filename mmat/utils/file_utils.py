import json
import os
from typing import Any, Dict

from ..core.test_suite import TestSuite # Import TestSuite

def load_test_suite_from_file(file_path: str) -> TestSuite: # Refine return type
    """
    Loads a test suite definition from a JSON file and converts it to a TestSuite object.

    Args:
        file_path: The path to the test suite JSON file.

    Returns:
        A dictionary representing the loaded test suite data.
        TODO: Convert this dictionary into a TestSuite object.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test suite file not found: {file_path}")

    with open(file_path, 'r') as f:
        test_suite_data = json.load(f)

    # This might require passing the TestSuite class or using a factory.
    return TestSuite.from_dict(test_suite_data)

# Example Usage (for demonstration)
if __name__ == "__main__":
    # Create a dummy JSON file for testing
    dummy_suite_content = {
        "name": "Example Suite",
        "description": "A dummy test suite",
        "test_cases": [
            {
                "name": "Dummy Case 1",
                "description": "First dummy case",
                "steps": [
                    {"type": "navigate", "description": "Go somewhere", "params": {"url": "about:blank"}}
                ]
            }
        ]
    }
    dummy_file_path = "dummy_test_suite.json"
    with open(dummy_file_path, 'w') as f:
        json.dump(dummy_suite_content, f, indent=4)

    try:
        loaded_data = load_test_suite_from_file(dummy_file_path)
        print("Successfully loaded dummy test suite data:")
        print(loaded_data)
    except Exception as e:
        print(f"Error loading dummy test suite: {e}")
    finally:
        # Clean up the dummy file
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)
