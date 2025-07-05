# MMAT JSON Reporter Tests
# Tests for the JSON reporting utility.

import unittest
import json
import os
from mmat.reporting.json_reporter import JsonReporter
from mmat.reporting.reporter import Reporter # Import base Reporter for type checking/mocking if needed

class TestJsonReporter(unittest.TestCase):

    def setUp(self):
        """Set up a temporary output file for testing."""
        self.output_file = "test_report.json"
        self.reporter = JsonReporter(self.output_file)
        # Ensure the file is empty or doesn't exist before each test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def tearDown(self):
        """Clean up the temporary output file."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_report_test_start(self):
        """Test reporting the start of a test."""
        self.reporter.report_test_start("TestFeature.test_scenario_1")
        # Start doesn't write immediately, state is held internally

    def test_report_test_end_passed(self):
        """Test reporting a passed test."""
        self.reporter.report_test_start("TestFeature.test_scenario_1")
        self.reporter.report_test_end("TestFeature.test_scenario_1", "PASSED")

        # Check internal state or wait for summary to write

    def test_report_test_end_failed(self):
        """Test reporting a failed test with details."""
        self.reporter.report_test_start("TestFeature.test_scenario_2")
        self.reporter.report_test_end("TestFeature.test_scenario_2", "FAILED", "Assertion failed: expected X got Y")

        # Check internal state or wait for summary to write

    def test_report_test_end_skipped(self):
        """Test reporting a skipped test."""
        self.reporter.report_test_start("TestFeature.test_scenario_3")
        self.reporter.report_test_end("TestFeature.test_scenario_3", "SKIPPED")

        # Check internal state or wait for summary to write

    def test_report_summary_writes_file(self):
        """Test that report_summary writes the accumulated results to the file."""
        self.reporter.report_test_start("TestA")
        self.reporter.report_test_end("TestA", "PASSED")
        self.reporter.report_test_start("TestB")
        self.reporter.report_test_end("TestB", "FAILED", "Error details")
        self.reporter.report_test_start("TestC")
        self.reporter.report_test_end("TestC", "SKIPPED")

        self.reporter.report_summary(total=3, passed=1, failed=1, skipped=1)

        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as f:
            report_data = json.load(f)

        self.assertIn("summary", report_data)
        self.assertEqual(report_data["summary"]["total"], 3)
        self.assertEqual(report_data["summary"]["passed"], 1)
        self.assertEqual(report_data["summary"]["failed"], 1)
        self.assertEqual(report_data["summary"]["skipped"], 1)

        self.assertIn("results", report_data)
        self.assertEqual(len(report_data["results"]), 3)

        # Check individual test results (order might matter depending on implementation)
        # Assuming order is preserved based on report_test_end calls
        self.assertEqual(report_data["results"][0]["name"], "TestA")
        self.assertEqual(report_data["results"][0]["status"], "PASSED")
        self.assertNotIn("details", report_data["results"][0])

        self.assertEqual(report_data["results"][1]["name"], "TestB")
        self.assertEqual(report_data["results"][1]["status"], "FAILED")
        self.assertEqual(report_data["results"][1]["details"], "Error details")

        self.assertEqual(report_data["results"][2]["name"], "TestC")
        self.assertEqual(report_data["results"][2]["status"], "SKIPPED")
        self.assertNotIn("details", report_data["results"][2])


if __name__ == '__main__':
    unittest.main()
