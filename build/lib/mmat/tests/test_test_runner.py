# MMAT Test Runner Tests
# Tests for the core test execution logic.

import unittest
from mmat.core.test_runner import TestRunner
from mmat.reporting.reporter import Reporter

# Mock Reporter for testing
class MockReporter(Reporter):
    def __init__(self):
        self.results = []

    def report_test_start(self, test_name):
        self.results.append(f"Start: {test_name}")

    def report_test_end(self, test_name, status, details=None):
        result = f"End: {test_name} - {status}"
        if details:
            result += f" - {details}"
        self.results.append(result)

    def report_summary(self, total, passed, failed, skipped):
        self.results.append(f"Summary: Total={total}, Passed={passed}, Failed={failed}, Skipped={skipped}")

# Mock Test Case for testing
class MockTestCase:
    def __init__(self, name, should_pass=True, should_skip=False, error_details=None):
        self.name = name
        self.should_pass = should_pass
        self.should_skip = should_skip
        self.error_details = error_details

    def run(self, reporter):
        reporter.report_test_start(self.name)
        if self.should_skip:
            reporter.report_test_end(self.name, "SKIPPED")
            return "SKIPPED"
        try:
            if self.should_pass:
                reporter.report_test_end(self.name, "PASSED")
                return "PASSED"
            else:
                raise Exception(self.error_details if self.error_details else "Test failed")
        except Exception as e:
            reporter.report_test_end(self.name, "FAILED", str(e))
            return "FAILED"


class TestTestRunner(unittest.TestCase):

    def test_run_tests_basic(self):
        """Test running a mix of passing, failing, and skipped tests."""
        mock_reporter = MockReporter()
        mock_tests = [
            MockTestCase("TestA", should_pass=True),
            MockTestCase("TestB", should_pass=False, error_details="Something went wrong"),
            MockTestCase("TestC", should_pass=True),
            MockTestCase("TestD", should_skip=True),
            MockTestCase("TestE", should_pass=False)
        ]

        runner = TestRunner(mock_reporter)
        runner.run_tests(mock_tests)

        expected_results = [
            "Start: TestA",
            "End: TestA - PASSED",
            "Start: TestB",
            "End: TestB - FAILED - Something went wrong",
            "Start: TestC",
            "End: TestC - PASSED",
            "Start: TestD",
            "End: TestD - SKIPPED",
            "Start: TestE",
            "End: TestE - FAILED - Test failed",
            "Summary: Total=5, Passed=2, Failed=2, Skipped=1"
        ]

        self.assertEqual(mock_reporter.results, expected_results)

    def test_run_tests_empty_list(self):
        """Test running with an empty list of tests."""
        mock_reporter = MockReporter()
        mock_tests = []

        runner = TestRunner(mock_reporter)
        runner.run_tests(mock_tests)

        expected_results = [
            "Summary: Total=0, Passed=0, Failed=0, Skipped=0"
        ]

        self.assertEqual(mock_reporter.results, expected_results)

if __name__ == '__main__':
    unittest.main()
