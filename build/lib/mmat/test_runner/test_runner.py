import yaml
import os

from mmat.driver.playwright_driver import PlaywrightDriver
from mmat.config.config_manager import ConfigManager
from mmat.test_steps.web_steps import NavigateStep, FillStep, ClickStep
from mmat.test_steps.base_step import TestStep # Import BaseStep

class TestRunner:
    """
    Handles the execution of MMAT test plans.
    """
    def __init__(self, driver: PlaywrightDriver, config_manager: ConfigManager):
        """
        Initializes the TestRunner.

        Args:
            driver (PlaywrightDriver): The Playwright driver instance.
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.driver = driver
        self.config_manager = config_manager
        self.config = self.config_manager.config
        print("[TestRunner] Initialized.")

    def load_test_plan(self, test_plan_path: str) -> dict | None:
        """
        Loads and parses a test plan from a YAML file.

        Args:
            test_plan_path (str): Path to the test plan YAML file.

        Returns:
            dict | None: The test plan dictionary if successful, None otherwise.
        """
        if not os.path.exists(test_plan_path):
            print(f"[TestRunner] Error: Test plan file not found at {test_plan_path}")
            return None

        try:
            with open(test_plan_path, 'r') as f:
                test_plan = yaml.safe_load(f)
            print(f"[TestRunner] Loaded test plan from {test_plan_path}")
            return test_plan
        except yaml.YAMLError as e:
            print(f"[TestRunner] Error loading test plan {test_plan_path}: {e}")
            return None

    def execute_plan(self, test_plan: dict, start_step: int = 1) -> bool:
        """
        Executes a given test plan.

        Args:
            test_plan (dict): The test plan dictionary.
            start_step (int): The step number to start execution from (1-based index).

        Returns:
            bool: True if the plan executed successfully, False otherwise.
        """
        if not test_plan or 'steps' not in test_plan:
            print("[TestRunner] Error: Invalid test plan format. 'steps' key is missing.")
            return False

        steps = test_plan.get('steps', [])
        total_steps = len(steps)

        if start_step < 1 or start_step > total_steps:
            print(f"[TestRunner] Error: Invalid start step {start_step}. Must be between 1 and {total_steps}.")
            return False

        print(f"[TestRunner] Executing test plan with {total_steps} steps, starting from step {start_step}.")

        # Prepare test data if available
        test_data = test_plan.get('test_data', {})

        for i in range(start_step - 1, total_steps):
            step_data = steps[i]
            step_number = i + 1
            step_name = step_data.get('name', f'Step {step_number}')
            step_type = step_data.get('type')

            print(f"[TestRunner] Executing step {step_number}/{total_steps}: {step_name} (Type: {step_type})")

            try:
                # Instantiate the correct step class based on type
                step_instance: TestStep | None = None
                if step_type == 'web.navigate':
                    step_instance = NavigateStep(step_data, self.driver)
                elif step_type == 'web.fill':
                    step_instance = FillStep(step_data, self.driver)
                elif step_type == 'web.click':
                    step_instance = ClickStep(step_data, self.driver)
                # Add other step types here as they are implemented (e.g., visual.click, api.call)
                else:
                    print(f"[TestRunner] Warning: Unknown step type '{step_type}'. Skipping step.")
                    continue # Skip unknown step types

                if step_instance:
                    success = step_instance.execute()
                    if success:
                        print(f"[TestRunner] Step {step_number} '{step_name}' completed successfully. ✔️")
                    else:
                        print(f"[TestRunner] Step {step_number} '{step_name}' failed. ❌")
                        # Depending on requirements, you might stop execution on failure
                        # For now, let's continue to the next step
                        # return False # Uncomment to stop on first failure

            except Exception as e:
                print(f"[TestRunner] An error occurred during execution of step {step_number} '{step_name}': {e} ❌")
                # return False # Uncomment to stop on first exception

        print("[TestRunner] Test plan execution finished.")
        return True # Indicate that execution finished (not necessarily all steps succeeded)

    # The execute_step method is now integrated into execute_plan
    # Keep it as a placeholder or remove if not needed elsewhere
    def execute_step(self, step_data: dict, test_data: dict) -> bool:
        """
        Executes a single step from the test plan (internal helper).

        Args:
            step_data (dict): The step dictionary.
            test_data (dict): The test data dictionary.

        Returns:
            bool: True if the step executed successfully, False otherwise.
        """
        print(f"[TestRunner] Internal execute_step called for: {step_data.get('name', 'Unnamed Step')}")
        # This method is now primarily handled by the logic within execute_plan
        # and the individual step classes. This can be removed if not used.
        print("[TestRunner] Warning: execute_step is deprecated. Step execution is handled within execute_plan.")
        return False # Indicate that this method is not the primary execution path

    # Add other methods related to test execution
    # def validate_plan(self, test_plan: dict) -> bool:
    #     """Validates the structure and content of a test plan."""
    #     print("[TestRunner] Validating test plan.")
    #     # Placeholder for validation logic
    #     pass
