from typing import Optional, Union

from .test_case import TestCase
from .test_suite import TestSuite
from .test_step import TestStep
# Assuming environment and reporting modules will be available
# from mmat.environment.environment import BaseEnvironment
# from mmat.reporting.reporter import BaseReporter

class TestRunner:
    """Runs test cases and test suites step-by-step."""

    def __init__(
        self,
        # environment: BaseEnvironment, # Placeholder for browser environment
        # reporter: BaseReporter # Placeholder for reporting
    ):
        """
        Initializes the TestRunner.

        Args:
            environment: The browser environment to use for execution.
            reporter: The reporter to use for logging results.
        """
        # self.environment = environment
        # self.reporter = reporter
        pass # Placeholder initialization

    def run(self, test: Union[TestCase, TestSuite], start_step: int = 1):
        """
        Runs a test case or test suite.

        Args:
            test: The TestCase or TestSuite to run.
            start_step: The step number to start execution from (1-based index).
        """
        if isinstance(test, TestSuite):
            print(f"[MMAT] Running test suite: {test.name}")
            for i, test_case in enumerate(test.test_cases):
                print(f"[MMAT] Running test case {i+1}/{len(test.test_cases)}: {test_case.name}")
                self._run_test_case(test_case, start_step if i == 0 else 1) # Only apply start_step to the first case
        elif isinstance(test, TestCase):
            print(f"[MMAT] Running test case: {test.name}")
            self._run_test_case(test, start_step)
        else:
            print(f"[MMAT] Error: Invalid test type provided: {type(test)}")

    def _run_test_case(self, test_case: TestCase, start_step: int):
        """Internal method to run a single test case."""
        total_steps = len(test_case.steps)
        print(f"[MMAT] Total steps: {total_steps}")

        if start_step < 1 or start_step > total_steps:
            print(f"[MMAT] Warning: Invalid start step {start_step}. Starting from step 1.")
            current_step_index = 0
        else:
            current_step_index = start_step - 1

        for i in range(current_step_index, total_steps):
            step = test_case.steps[i]
            step_number = i + 1
            print(f"Step {step_number}/{total_steps}: {step.description or step.action}...")

            try:
                # Placeholder for step execution logic
                # result = self.environment.execute_step(step)
                # step.status = 'passed' # Or 'failed' based on result
                # step.result = result
                # self.reporter.report_step(step_number, step)
                print(f"Step {step_number}/{total_steps}: {step.description or step.action}   ✔️ OK (Simulated)") # Simulated success
                step.status = 'passed' # Simulated status update

            except Exception as e:
                # step.status = 'failed'
                # step.error = str(e)
                # self.reporter.report_step(step_number, step)
                print(f"Step {step_number}/{total_steps}: {step.description or step.action}   ❌ Failed (Simulated)") # Simulated failure
                step.status = 'failed' # Simulated status update
                step.error = str(e) # Simulated error

            # Optional: Stop on first failure
            # if step.status == 'failed':
            #     test_case.status = 'failed'
            #     test_case.error = f"Step {step_number} failed"
            #     print(f"[MMAT] Test case failed at step {step_number}.")
            #     break

        # Determine final test case status (simplified)
        if all(step.status == 'passed' for step in test_case.steps[current_step_index:]):
             test_case.status = 'passed'
             print(f"[MMAT] Test case '{test_case.name}' finished successfully.")
        else:
             test_case.status = 'failed'
             print(f"[MMAT] Test case '{test_case.name}' finished with errors.")

        # self.reporter.report_test_case(test_case)
