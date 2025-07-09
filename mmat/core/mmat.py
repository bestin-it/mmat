import sys # Import sys for accessing command line arguments
import argparse # Import argparse for real CLI argument parsing
import os
import yaml
import json

from mmat.driver.playwright_driver import PlaywrightDriver
from mmat.description_generator import DescriptionGenerator # Import DescriptionGenerator
from mmat.test_runner.test_runner import TestRunner
from mmat.config.config_manager import ConfigManager # Import ConfigManager
from mmat.plan_builder.plan_builder import PlanBuilder # Import PlanBuilder
from mmat.models.local_api_reasoning_model import LocalApiReasoningModel # Import the concrete reasoning model
from mmat.models.local_api_vision_model import LocalApiVisionModel # Import the concrete vision model
from mmat.graph.graph_api import GraphAPI # Import GraphAPI
from mmat.analysis.screenshot_analyzer import ScreenshotAnalyzer # Import ScreenshotAnalyzer

class MMAT:
    """
    Core MMAT (Multi Modal AI Tester) framework class.
    Manages the overall test execution, generation, and feedback loop.
    """
    def __init__(self, config_path="config/config.yaml"):
        """
        Initializes the MMAT framework.

        Args:
            config_path (str): Path to the configuration file.
        """
        self.config_manager = ConfigManager(config_path) # Use ConfigManager
        self.config = self.config_manager.config # Load config

        # Initialize other modules (Graph API, Playwright Driver, Models, Analyzers, etc.)
        # based on the loaded configuration.
        print(f"[MMAT] Initialized with config from {config_path}")

        # Initialize core components
        self.playwright_driver = PlaywrightDriver(self.config) # Initialize Playwright Driver
        self.test_runner = TestRunner(self.playwright_driver, self.config_manager) # Initialize Test Runner with driver and config_manager

        # Initialize models based on configuration
        # Initialize models based on configuration
        self.reasoning_model = None
        self.vision_model = None
        models_config = self.config.get('models', {})

        if 'reasoning' in models_config:
            reasoning_config = models_config['reasoning']
            model_type = reasoning_config.get('type')
            # Parameters are expected in a nested 'config' dictionary
            model_params = reasoning_config.get('config', {})
            # The type 'llm' in config.yaml should map to LocalApiReasoningModel
            if model_type == 'llm':
                 try:
                     # LocalApiReasoningModel expects 'api_url' and 'model_name'
                     # Ensure these are present in model_params
                     api_url = model_params.get('endpoint') # Mapping 'endpoint' from config to 'api_url'
                     model_name = model_params.get('model_name')

                     if not api_url or not model_name:
                         print("[MMAT] Error: 'endpoint' or 'model_name' missing in reasoning model config parameters.")
                         self.reasoning_model = None # Ensure model is None if config is incomplete
                     else:
                         self.reasoning_model = LocalApiReasoningModel(api_url=api_url, model_name=model_name)

                 except TypeError as e:
                     print(f"[MMAT] Error initializing reasoning model with parameters {model_params}: {e}")
                     self.reasoning_model = None
                 except Exception as e:
                     print(f"[MMAT] An unexpected error occurred initializing reasoning model: {e}")
                     self.reasoning_model = None
            else:
                print(f"[MMAT] Warning: Unknown reasoning model type '{model_type}' specified in config.")
                self.reasoning_model = None

        if 'vision' in models_config:
            vision_config = models_config['vision']
            vision_config = models_config['vision']
            model_type = vision_config.get('type')
            print(f"[MMAT] Debug: Vision model type read from config: '{model_type}'") # Debug print
            # Parameters are expected in a 'parameters' dictionary
            model_params = vision_config.get('parameters', {})
            # The type 'vision_model' in config.yaml should map to LocalApiVisionModel
            if model_type == 'vision_model':
                 try:
                     # LocalApiVisionModel expects 'api_url' and 'model_name'
                     # Ensure these are present in model_params
                     api_url = model_params.get('api_url') # Use 'api_url' directly from parameters
                     model_name = model_params.get('model_name')

                     if not api_url or not model_name:
                         print("[MMAT] Error: 'api_url' or 'model_name' missing in vision model config parameters.")
                         self.vision_model = None # Ensure model is None if config is incomplete
                     else:
                         self.vision_model = LocalApiVisionModel(api_url=api_url, model_name=model_name)

                 except TypeError as e:
                     print(f"[MMAT] Error initializing vision model with parameters {model_params}: {e}")
                     self.vision_model = None
                 except Exception as e:
                     print(f"[MMAT] An unexpected error occurred initializing vision model: {e}")
                     self.vision_model = None
            else:
                print(f"[MMAT] Warning: Unknown vision model type '{model_type}' specified in config.")
                self.vision_model = None


        # Initialize Plan Builder with config_manager and reasoning model
        self.plan_builder = PlanBuilder(self.config_manager, self.reasoning_model)

        # Initialize Graph API
        self.graph_api = GraphAPI()

        # Debug prints before ScreenshotAnalyzer initialization check
        print(f"[MMAT] Debug: self.vision_model before check: {self.vision_model}")
        print(f"[MMAT] Debug: self.graph_api before check: {self.graph_api}")

        # Initialize Screenshot Analyzer (requires vision model and graph API)
        if self.vision_model and self.graph_api:
            print("[MMAT] Debug: Initializing ScreenshotAnalyzer.")
            self.screenshot_analyzer = ScreenshotAnalyzer(self.vision_model, self.graph_api)
        else:
            self.screenshot_analyzer = None
            print("[MMAT] Warning: Vision model or Graph API not initialized. Screenshot analysis will be unavailable.")


        # Placeholder for other module instances
        self.html_analyzer = None # Initialize HTML Analyzer
        self.reporting = None # Initialize Reporting
        self.feedback_handler = None # Initialize Feedback Handler

    def run(self, args):
        """
        Parses CLI arguments and executes the corresponding command.

        Args:
            args: Parsed command-line arguments from argparse.
        """
        print(f"[MMAT] Executing command: {args.command}")

        if args.command == 'generate':
            print("[MMAT] Generating test plan...")
            description = args.desc
            output_path = args.output
            force = args.force # Get the force flag

            if not description:
                print("[MMAT] Error: Description is required for 'generate' command.")
                return

            if not output_path:
                print("[MMAT] Error: Output path is required for 'generate' command.")
                return

            # Check if output file exists and force is not enabled
            if os.path.exists(output_path) and not force:
                print(f"[MMAT] Error: Output file '{output_path}' already exists. Use --force to overwrite.")
                return

            try:
                test_plan = self.plan_builder.generate_plan_from_description(description)
                if test_plan:
                    # Save the generated test plan to the output file (as YAML)
                    output_dir = os.path.dirname(output_path)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    with open(output_path, 'w') as f:
                        yaml.dump(test_plan, f, indent=2)

                    print(f"[MMAT] Test plan successfully generated and saved to {output_path}")
                else:
                    print("[MMAT] Failed to generate test plan.")
            except Exception as e:
                print(f"[MMAT] An error occurred during test generation: {e}")
                import traceback
                traceback.print_exc() # Print traceback for debugging


        elif args.command == 'run':
            print("[MMAT] Running test plan...")
            test_plan_path = args.test
            start_step = getattr(args, 'step', 1) # Default to step 1 if not provided

            test_plan = self.test_runner.load_test_plan(test_plan_path)
            if test_plan:
                self.test_runner.execute_plan(test_plan, start_step)

        elif args.command == 'export':
            print("[MMAT] Exporting test plan...")
            test_plan_path = args.test_plan_path
            output_path = args.output
            force = args.force

            if not test_plan_path:
                print("[MMAT] Error: Test plan path is required for 'export' command.")
                return

            if not output_path:
                print("[MMAT] Error: Output path is required for 'export' command.")
                return

            # Check if output file exists and force is not enabled
            if os.path.exists(output_path) and not force:
                print(f"[MMAT] Error: Output file '{output_path}' already exists. Use --force to overwrite.")
                return

            test_plan = self.plan_builder.load_plan(test_plan_path)
            if not test_plan:
                print(f"[MMAT] Failed to load test plan from {test_plan_path}")
                return

            try:
                # Generate Playwright code
                playwright_code = self._generate_playwright_code(test_plan)

                # Write to output file
                with open(output_path, 'w') as f:
                    f.write(playwright_code)

                print(f"[MMAT] Test plan successfully exported to Playwright code at {output_path}")

            except Exception as e:
                print(f"[MMAT] An error occurred during export: {e}")

        elif args.command == 'describe':
            print("[MMAT] Generating description...")
            test_plan_path = args.test_plan_path # Assuming the CLI argument is named test_plan_path
            output_path = args.output # Assuming the CLI argument is named output
            force = args.force # Assuming the CLI argument is named force

            if not test_plan_path:
                print("[MMAT] Error: Test plan path is required for 'describe' command.")
                return

            if output_path and os.path.exists(output_path) and not force:
                print(f"[MMAT] Error: Output file '{output_path}' already exists. Use --force to overwrite.")
                return

            # Ensure reasoning model is initialized
            if not self.reasoning_model:
                 print("[MMAT] Error: Reasoning model is not configured or initialized. Cannot generate description.")
                 return

            try:
                # Load the test plan
                # Assuming PlanBuilder.build_from_file is implemented and works
                test_suite = self.plan_builder.build_from_file(test_plan_path)

                # Instantiate DescriptionGenerator and generate description
                generator = DescriptionGenerator(self.reasoning_model)
                description = generator.generate_description(test_suite)

                if output_path:
                    # Save description to file
                    output_dir = os.path.dirname(output_path)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(description)
                    print(f"[MMAT] Functional description successfully generated and saved to {output_path}")
                else:
                    # Print description to stdout
                    print("[MMAT] Generated Functional Description:")
                    print(description)

            except FileNotFoundError:
                print(f"[MMAT] Error: Test plan file not found at {test_plan_path}")
            except ValueError as e:
                print(f"[MMAT] Error loading or processing test plan: {e}")
            except Exception as e:
                print(f"[MMAT] An error occurred during description generation: {e}")
                import traceback
                traceback.print_exc() # Print traceback for debugging


        elif args.command == 'feedback':
            print("[MMAT] Entering feedback mode...")
            # Placeholder for feedback logic
            pass

        elif args.command == 'list':
            print("[MMAT] Listing tests...")
            # Placeholder for list logic
            pass

        elif args.command == 'show':
            print("[MMAT] Showing test details...")
            # Placeholder for show logic
            pass

        elif args.command == 'import-e2e':
            print("[MMAT] Importing E2E test script...")
            input_file_path = args.input_file
            output_path = args.output
            force = args.force

            print(f"[MMAT] Checking for input file at: {input_file_path}") # Debug print
            if not os.path.exists(input_file_path):
                print(f"[MMAT] Error: Input file '{input_file_path}' not found.")
                return

            if output_path and os.path.exists(output_path) and not force:
                print(f"[MMAT] Error: Output file '{output_path}' already exists. Use --force to overwrite.")
                return

            try:
                # Import PlaywrightImporter
                from mmat.importer.playwright_importer import PlaywrightImporter

                importer = PlaywrightImporter()
                test_suite = importer.import_from_file(input_file_path)

                # Convert TestSuite to dictionary
                test_suite_dict = test_suite.to_dict()

                if output_path:
                    # Save to file (YAML or JSON based on extension)
                    output_dir = os.path.dirname(output_path)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    with open(output_path, 'w') as f:
                        if output_path.lower().endswith(('.yaml', '.yml')):
                            yaml.dump(test_suite_dict, f, indent=2)
                            print(f"[MMAT] Test suite successfully imported and saved to YAML at {output_path}")
                        else: # Default to JSON
                            json.dump(test_suite_dict, f, indent=2)
                            print(f"[MMAT] Test suite successfully imported and saved to JSON at {output_path}")
                else:
                    # Print to stdout (as YAML for readability)
                    print("[MMAT] Imported Test Suite (YAML format):")
                    print(yaml.dump(test_suite_dict, indent=2))

            except Exception as e:
                print(f"[MMAT] An error occurred during import: {e}")
                import traceback
                traceback.print_exc() # Print traceback for debugging


        elif args.command == 'init':
            print(f"[MMAT] Initializing new project: {args.project_name}")
            project_dir = args.project_name

            # Create project directory
            if os.path.exists(project_dir):
                print(f"[MMAT] Error: Directory '{project_dir}' already exists.")
                return
            os.makedirs(project_dir)
            print(f"[MMAT] Created directory: {project_dir}")

            # Create subdirectories
            os.makedirs(os.path.join(project_dir, "functional_descriptions"))
            os.makedirs(os.path.join(project_dir, "tests", "functional"))
            os.makedirs(os.path.join(project_dir, "tests", "e2e"))
            os.makedirs(os.path.join(project_dir, "config"))
            print(f"[MMAT] Created subdirectories.")

            # Create example functional description
            functional_description_content = """# User Login Feature

## Description
This feature allows users to log in to the application using their username and password.

## Requirements
- Users must be able to enter their username and password.
- Upon successful login with valid credentials, the user should be redirected to the dashboard.
- If the user provides invalid credentials, an error message should be displayed.
- There should be a "Forgot Password" link.

## Scenarios
- **Successful Login:**
  - Given the user is on the login page
  - When they enter valid username and password
  - And click the login button
  - Then they should be redirected to the dashboard.

- **Failed Login (Invalid Password):**
  - Given the user is on the login page
  - When they enter a valid username and an invalid password
  - And click the login button
  - Then an error message should be displayed.
"""
            with open(os.path.join(project_dir, "functional_descriptions", "user_login.md"), "w") as f:
                f.write(functional_description_content)
            print(f"[MMAT] Created example functional description: {os.path.join(project_dir, 'functional_descriptions', 'user_login.md')}")

            # Create example test plan
            test_plan_content = """test_plan:
  name: User Login Tests
  description: Tests for the user login feature
  test_suites:
    - name: Standard Login
      description: Test standard user login scenarios
      test_cases:
        - name: Successful Login with Valid Credentials
          description: Verify a user can log in successfully
          steps:
            - action: navigate
              target: /login
              description: Go to the login page
            - action: fill
              selector: '#username'
              value: testuser
              description: Enter valid username
            - action: fill
              selector: '#password'
              value: password123
              description: Enter valid password
            - action: click
              selector: '#login-button'
              description: Click the login button
            - action: assert_url
              expected: /dashboard
              description: Verify redirection to dashboard
        - name: Failed Login with Invalid Password
          description: Verify login fails with incorrect password
          steps:
            - action: navigate
              target: /login
              description: Go to the login page
            - action: fill
              selector: '#username'
              value: testuser
              description: Enter valid username
            - action: fill
              selector: '#password'
              value: wrongpassword
              description: Enter invalid password
            - action: click
              selector: '#login-button'
              description: Click the login button
            - action: assert_element_visible
              selector: '.error-message'
              description: Verify error message is displayed
"""
            with open(os.path.join(project_dir, "tests", "functional", "user_login_plan.yaml"), "w") as f:
                f.write(test_plan_content)
            print(f"[MMAT] Created example test plan: {os.path.join(project_dir, 'tests', 'functional', 'user_login_plan.yaml')}")

            # Create example E2E test
            e2e_test_content = """import pytest
from playwright.sync_api import Page, sync_playwright

# Test Suite: Standard Login
# Description: Test standard user login scenarios

# Test Case: Successful Login with Valid Credentials
# Description: Verify a user can log in successfully
def test_successful_login(page: Page):
    page.goto("/login")
    page.fill('#username', 'testuser')
    page.fill('#password', 'password123')
    page.click('#login-button')
    # Verify redirection to dashboard
    assert page.url.endswith('/dashboard')

# Test Case: Failed Login with Invalid Password
# Description: Verify login fails with incorrect password
def test_failed_login_invalid_password(page: Page):
    page.goto("/login")
    page.fill('#username', 'testuser')
    page.fill('#password', 'wrongpassword')
    page.click('#login-button')
    # Verify error message is displayed
    assert page.is_visible('.error-message')
"""
            with open(os.path.join(project_dir, "tests", "e2e", "test_user_login.py"), "w") as f:
                f.write(e2e_test_content)
            print(f"[MMAT] Created example E2E test: {os.path.join(project_dir, 'tests', 'e2e', 'test_user_login.py')}")

            # Create config.yaml with example content
            config_content = """environments:
  browser:
    type: puppeteer
    config:
      baseUrl: http://localhost:3000 # Replace with your application’s base URL
      headless: true # Set to false to see the browser
      defaultTimeout: 10000 # Milliseconds

models:
  reasoning:
    provider: local_api # Example: using a local API endpoint
    type: llm
    config:
      endpoint: http://172.29.32.1:1234/v1
      model_name: mistralai/magistral-small

  vision:
    provider: local_api # Using local API for vision model as well
    type: vision_model # Changed type to match LocalApiVisionModel
    parameters: # Changed to parameters to match LocalApiVisionModel
      api_url: http://172.29.32.1:1234/v1
      model_name: mistralai/mistral-small-3.2

reporting:
  - type: json
    config:
      outputDir: ./reports"""
            with open(os.path.join(project_dir, "config", "config.yaml"), "w") as f:
                f.write(config_content)
            print(f"[MMAT] Created example config file: {os.path.join(project_dir, 'config', 'config.yaml')}")


            # Create requirements.txt with example content
            requirements_content = """mmat
# Add other project dependencies here"""
            with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
                f.write(requirements_content)
            print(f"[MMAT] Created example requirements file: {os.path.join(project_dir, 'requirements.txt')}")


            # Create a basic README.md
            readme_content = f"""# {project_dir}

This is an MMAT project.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `config/config.yaml` with your environment and model settings.
3. Create functional descriptions in `functional_descriptions/`.
4. Build test plans using `mmat build`.
5. Run test plans using `mmat run`.
"""
            with open(os.path.join(project_dir, "README.md"), "w") as f:
                f.write(readme_content)
            print(f"[MMAT] Created example README file: {os.path.join(project_dir, 'README.md')}")


            print(f"[MMAT] Project '{project_dir}' initialized successfully.")


        else:
            print(f"[MMAT] Unknown command: {args.command}")

        print("[MMAT] Command execution finished.")

    def _generate_playwright_code(self, test_plan):
        """
        Generates Playwright Python code from a test plan.

        Args:
            test_plan (dict): The parsed test plan dictionary.

        Returns:
            str: The generated Playwright Python code.
        """
        code = """import asyncio
from playwright.async_api import Playwright, async_playwright, expect

async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch()
    context = await browser.new_context()
    page = await context.new_page()

"""
        indent = "    " * 2 # Indentation for steps within the async function

        for step in test_plan.get("steps", []):
            step_type = step.get("type")
            step_params = step.get("params", {})

            if step_type == "web.navigate":
                url = step_params.get("url")
                if url:
                    code += f'{indent}await page.goto("{url}")\n'
            elif step_type == "web.comment":
                text = step_params.get("text")
                if text:
                    code += f'{indent}# {text}\n'
            # Add more step type mappings here as needed (e.g., click, fill, expect)
            else:
                code += f'{indent}# WARNING: Unsupported step type: {step_type}\n'

        code += """
    # ---------------------
    await context.close()
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == "__main__":
    asyncio.run(main())
"""
        return code

    # The following methods are now handled by the run method based on parsed args
    # or delegated to other classes (TestRunner, PlanBuilder).
    # Keeping them as placeholders or removing them if not needed elsewhere.

    # def run_test(self, test_plan_path, start_step=1):
    #     """Runs a test plan."""
    #     print(f"[MMAT] Running test plan: {test_plan_path} starting from step {start_step}")
    #     # This logic is now in the run method under 'run' command
    #     pass

    # def generate_test(self, description, output_path, force=False):
    #     """Generates a new E2E test from a description."""
    #     print(f"[MMAT] Generating test from description. Output: {output_path}")
    #     # This logic is now in the run method under 'generate' command
    #     pass

    # def export_test(self, test_plan_path, export_format, lang=None, output_path=None):
    #     """Exports an E2E test to a different format (e.g., Playwright code)."""
    #     print(f"[MMAT] Exporting test plan: {test_plan_path} to {export_format}")
    #     # This logic will be in the run method under 'export' command
    #     pass

    # def describe_test(self, test_plan_path, output_path):
    #     """Creates or updates a human-readable test description from a test plan."""
    #     print(f"[MMAT] Generating description for test plan: {test_plan_path}")
    #     # This logic will be in the run method under 'describe' command
    #     pass

    # def feedback(self, test_plan_path):
    #     """Enters improvement mode for a test plan."""
    #     print(f"[MMAT] Entering feedback mode for test plan: {test_plan_path}")
    #     # This logic will be in the run method under 'feedback' command
    #     pass

    # def list_tests(self, filters):
    #     """Lists tests based on filters."""
    #     print(f"[MMAT] Listing tests with filters: {filters}")
    #     # This logic will be in the run method under 'list' command
    #     pass

    # def show_test(self, test_plan_path):
    #     """Displays details of a test plan."""
    #     print(f"[MMAT] Showing details for test plan: {test_plan_path}")
    #     # This logic will be in the run method under 'show' command
    #     pass

    # def validate_plan(self, test_plan_path):
    #     """Validates a test plan."""
    #     print(f"[MMAT] Validating test plan: {test_plan_path}")
    #     # Placeholder for validation logic
    #     pass


if __name__ == "__main__":
    mmat_app = MMAT()
    # Parse command line arguments and pass them to the run method
    args = parse_args()
    mmat_app.run(args)
