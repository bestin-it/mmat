# MMAT JSON Reporter
# Implements a reporter that outputs results in JSON format.

import json
from typing import Dict, Any

from mmat.reporting.reporter import Reporter

class JsonReporter(Reporter):
    """
    A reporter that collects test results and outputs them as a JSON file.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.results = {
            "suites": []
        }
        self._current_suite_index = -1
        self._current_case_index = -1

    async def start_suite(self, suite_name: str):
        self.results["suites"].append({
            "name": suite_name,
            "cases": []
        })
        self._current_suite_index = len(self.results["suites"]) - 1
        self._current_case_index = -1 # Reset case index for the new suite

    async def end_suite(self, suite_name: str):
        # No specific action needed at the end of a suite for this reporter's structure
        pass

    async def start_case(self, suite_name: str, case_name: str):
        if self._current_suite_index != -1:
            self.results["suites"][self._current_suite_index]["cases"].append({
                "name": case_name,
                "status": "running", # Initial status
                "details": {}
            })
            self._current_case_index = len(self.results["suites"][self._current_suite_index]["cases"]) - 1

    async def end_case(self, suite_name: str, case_name: str, status: str, details: Dict[str, Any]):
        if self._current_suite_index != -1 and self._current_case_index != -1:
            # Find the correct case to update (in case of async execution order issues, though sequential is expected initially)
            # A more robust approach might involve a dictionary lookup, but for now, assume order.
            case_entry = self.results["suites"][self._current_suite_index]["cases"][self._current_case_index]
            if case_entry["name"] == case_name: # Basic check
                 case_entry["status"] = status
                 case_entry["details"] = details
            else:
                 # Fallback search if order is not guaranteed
                 for i, case in enumerate(self.results["suites"][self._current_suite_index]["cases"]):
                     if case["name"] == case_name:
                         self.results["suites"][self._current_suite_index]["cases"][i]["status"] = status
                         self.results["suites"][self._current_suite_index]["cases"][i]["details"] = details
                         break


    async def publish_results(self):
        output_path = self.config.get("output_path", "mmat_results.json")
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=4)
        print(f"Test results published to {output_path}")

    # Add methods for handling test steps, assertions, etc., if needed for detailed reporting
