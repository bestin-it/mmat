# MMAT - Model-based Manual Acceptance Testing framework

MMAT is a Python framework designed to facilitate model-based manual acceptance testing. It leverages various components like reasoning models, vision models, and environments (like browsers) to automate the process of generating, executing, and reporting on manual acceptance tests based on functional descriptions or other data sources.

## Features (Planned)

*   **Model-based Test Plan Generation:** Generate test suites and test cases from functional descriptions or structured data using AI models.
*   **Environment Interaction:** Interact with various environments (e.g., web browsers via Puppeteer) to execute test steps.
*   **Test Data Management:** Manage and utilize test data for test execution.
*   **Validation and Analysis:** Validate test results and analyze outcomes using models.
*   **Reporting:** Generate test reports in various formats.
*   **Plugin System:** Allow extending the framework with custom components (environments, reporters, models, etc.).
*   **CLI Interface:** Command-line interface for running and building test plans.

## Installation

MMAT is a Python package. You can install it using pip.

**Prerequisites:**

*   Python 3.8+
*   pip

**Installation via pip (Recommended):**

Once the package is published to PyPI:

```bash
pip install mmat
```

**Installation from Source:**

If you want to install the latest version directly from the source code:

```bash
git clone https://github.com/yourusername/mmat.git # Replace with actual repo URL
cd mmat
pip install .
```

This will install the `mmat` package and its dependencies into your Python environment.

## Setting up MMAT Alias (Windows)

To easily run MMAT commands from any directory in your Windows terminal (Command Prompt or PowerShell), you can create an alias or a batch file.

**Method 1: Using a Batch File (Recommended)**

1.  Open a text editor (like Notepad).
2.  Paste the following content:
    ```batch
    @echo off
    "C:\Path\To\Your\Python\Scripts\mmat.exe" %*
    ```
    *Replace `"C:\Path\To\Your\Python\Scripts\mmat.exe"` with the actual path to the `mmat.exe` executable in your Python environment's `Scripts` directory.* You can find this path by running `where mmat` in your terminal after installing MMAT.
3.  Save the file as `mmat.bat` in a directory that is included in your system's `PATH` environment variable (e.g., `C:\Windows\System32` or a custom directory you've added to PATH).
4.  Close and reopen your terminal. You should now be able to run `mmat` commands directly.

**Method 2: Using `doskey` (Temporary or per-session)**

You can create a temporary alias using the `doskey` command in Command Prompt:

```cmd
doskey mmat="C:\Path\To\Your\Python\Scripts\mmat.exe" $*
```
*Replace `"C:\Path\To\Your\Python\Scripts\mmat.exe"` with the actual path.* This alias will only last for the current terminal session. To make it permanent, you would need to add this command to a batch file that runs when your terminal starts.

## Project Setup and Structure

MMAT provides an `init` command to help you quickly set up a basic project structure. This command creates a directory with a suggested layout for your test plans and configuration.

To initialize a new MMAT project, navigate to the directory where you want to create the project and run:

```bash
mmat init [project_name]
```

*   `[project_name]` (Optional): The name of the directory to create for your project. If not provided, it defaults to `my_mmat_project`.

This will create a directory structure similar to this:

```
[project_name]/
├── tests/
│   └── # Your test plans go here (e.g., functional/login_test_plan.yaml)
├── config/
│   └── config.yaml # Your MMAT configuration file
└── # Other project files (e.g., requirements.txt, README.md)
```

After initialization, you will integrate the `mmat` library into your project's dependencies (e.g., by adding `mmat` to your `requirements.txt`).

The typical structure when using `mmat` might look like this:

```
your_project/
├── tests/
│   ├── functional/
│   │   ├── login_test_plan.yaml
│   │   └── registration_test_plan.json
│   └── __init__.py # Optional, depending on how you organize
├── config/
│   └── config.yaml
├── src/ # Your application source code
│   └── ...
├── .gitignore
├── requirements.txt # Or other dependency management file
└── README.md # Your project's README
```

In this structure:

*   `tests/`: This directory is a common place to store your test plans. You can organize test plans into subdirectories (e.g., `functional/`, `integration/`) as needed. Test plans should be in a supported format (e.g., YAML or JSON).
*   `config/`: This directory is a good place to keep your `config.yaml` file, which MMAT uses for global configuration, including model and environment settings.
*   `requirements.txt`: List `mmat` and any other project dependencies here.

You will then use the `mmat` CLI or integrate the library directly into your Python scripts, referencing your test plans and configuration file by their paths relative to where you run the `mmat` command or script.

Here are examples of the content you might have in the files within your project structure:

### `tests/functional/login_test_plan.yaml`

```yaml
test_plan:
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
```

### `tests/functional/registration_test_plan.json`

```json
{
  "test_plan": {
    "name": "User Registration Tests",
    "description": "Tests for the user registration feature",
    "test_suites": [
      {
        "name": "New User Registration",
        "description": "Test new user registration scenarios",
        "test_cases": [
          {
            "name": "Successful Registration",
            "description": "Verify a new user can register successfully",
            "steps": [
              {
                "action": "navigate",
                "target": "/register",
                "description": "Go to the registration page"
              },
              {
                "action": "fill",
                "selector": "#new-username",
                "value": "newuser",
                "description": "Enter desired username"
              },
              {
                "action": "fill",
                "selector": "#new-password",
                "value": "securepassword",
                "description": "Enter desired password"
              },
              {
                "action": "click",
                "selector": "#register-button",
                "description": "Click the register button"
              },
              {
                "action": "assert_url",
                "expected": "/registration-success",
                "description": "Verify redirection to success page"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### `config/config.yaml`

```yaml
environments:
  browser:
    type: puppeteer
    config:
      baseUrl: http://localhost:3000 # Replace with your application's base URL
      headless: true # Set to false to see the browser
      defaultTimeout: 10000 # Milliseconds

models:
  reasoning:
    provider: local_api # Example: using a local API endpoint
    type: llm
    config:
      endpoint: http://localhost:8000/v1
      model_name: my-local-llm

  vision:
    provider: local_ollama # Example: using Ollama
    type: vision
    config:
      model_name: llava:7b
      endpoint: http://localhost:11434/api/generate

reporting:
  - type: json
    config:
      outputDir: ./reports
```

### `requirements.txt`

```
mmat
# Add any other dependencies your project needs
```

## Setting up Local Models with LM Studio

MMAT can utilize local Language Models (LLMs) and Vision Models (VMs) for tasks like test plan generation and analysis. LM Studio is a popular desktop application that allows you to discover, download, and run local LLMs.

Here's how to set up LM Studio and configure MMAT to use models served by it:

1.  **Download and Install LM Studio:**
    *   Go to the [LM Studio website](https://lmstudio.ai/) and download the appropriate version for your operating system (Windows, macOS, Linux).
    *   Install LM Studio following the on-screen instructions.

2.  **Download Models in LM Studio:**
    *   Open LM Studio.
    *   Use the search bar to find models. For MMAT, you'll likely need a reasoning model (a general-purpose LLM) and potentially a multimodal/vision model (like LLaVA) if you plan to use features that analyze screenshots.
    *   Click the "Download" button next to the models you want to use. Choose a suitable model size and quantization (e.g., Q4_K_M is a common balance between performance and quality).

3.  **Serve Models in LM Studio:**
    *   Go to the "Local Inference Server" tab (usually the third icon from the top left).
    *   Select the model you want to serve from the dropdown list.
    *   Click "Start Server". LM Studio will provide an API endpoint (usually `http://localhost:1234`) and port.

4.  **Configure MMAT's `config.yaml`:**
    *   Open your project's `config/config.yaml` file.
    *   Modify the `models` section to point to the LM Studio server.

    ```yaml
    environments:
      browser:
        type: puppeteer
        config:
          baseUrl: http://localhost:3000 # Replace with your application's base URL
          headless: true # Set to false to see the browser
          defaultTimeout: 10000 # Milliseconds

    models:
      reasoning:
        provider: lm_studio # Or a custom provider name
        type: llm
        config:
          endpoint: http://localhost:1234/v1 # Default LM Studio API endpoint
          model_name: your-downloaded-llm-name # Replace with the exact name of the LLM you are serving in LM Studio
          # Add any other required parameters for the LM Studio provider if needed by MMAT

      vision:
        provider: lm_studio # Or a custom provider name
        type: vision # Specify type as vision for multimodal models
        config:
          endpoint: http://localhost:1234/v1 # Default LM Studio API endpoint
          model_name: your-downloaded-vision-model-name # Replace with the exact name of the vision model (e.g., LLaVA) you are serving in LM Studio
          # Add any other required parameters

    reporting:
      - type: json
        config:
          outputDir: ./reports
    ```
    *Ensure the `endpoint` matches the address provided by LM Studio.*
    *The `model_name` in `config.yaml` should exactly match the name of the model you selected and started serving in LM Studio.*
    *MMAT's LM Studio provider (if implemented) will use this configuration to interact with the LM Studio API.*

5.  **Run MMAT:**
    *   With LM Studio running and serving the required models, you can now run MMAT commands that utilize these models.

## Understanding Graphs in MMAT

The `graph/` module in MMAT is planned to handle internal representations and interactions related to test flows, dependencies, or other structural aspects of the testing process. This is likely an internal component of the framework used for analysis, visualization (potentially), or orchestration, rather than requiring you to install a separate graph database or visualization tool for basic usage.

Specific setup details for utilizing or visualizing these internal graph structures will be provided in future documentation as the framework develops. For standard test execution, you typically won't need to perform separate graph setup steps beyond the main MMAT installation and configuration.

## Usage (Planned)

MMAT provides a command-line interface (CLI) to interact with the framework, primarily through the `run` and `build` commands.

### `mmat run`

The `mmat run` command is used to execute a specified test plan. When you run a test plan, MMAT will:

1.  Load the configuration from the specified `--config` file.
2.  Load the test plan identified by `<plan_identifier>` and `--plan-type`.
3.  Initialize the environments and models defined in the configuration.
4.  Iterate through the test suites and test cases within the test plan.
5.  Execute each test step in sequence using the configured environment (e.g., a browser).
6.  Perform validations and assertions as defined in the test steps.
7.  Collect results and generate reports using the configured reporters.

**Syntax:**

```bash
mmat run <plan_identifier> --plan-type <type> --config <config_file> [options]
```

*   `<plan_identifier>`: This is typically the path to your test plan file (e.g., `tests/functional/login_test_plan.yaml`).
*   `--plan-type <type>`: Specifies the format of the test plan file (e.g., `yaml`, `json`).
*   `--config <config_file>`: Specifies the path to your MMAT configuration file (e.g., `config/config.yaml`). This is crucial as it defines the environments, models, and reporting mechanisms to be used.
*   `[options]`: Additional options may be available depending on the MMAT version and plugins, such as filtering test cases, setting verbosity, etc.

**Example:**

```bash
mmat run tests/functional/login_test_plan.yaml --plan-type yaml --config config/config.yaml
```

This command would execute the test plan defined in `tests/functional/login_test_plan.yaml` using the settings from `config/config.yaml`.

### `mmat build`

The `mmat build` command is intended for generating or processing test plans, often leveraging the configured models. While the exact functionality might evolve, its primary purpose is to use MMAT's capabilities (especially model integration) to create or modify test artifacts.

This could involve:

*   Generating a structured test plan (YAML/JSON) from a less structured input like a functional description document (using a reasoning model).
*   Updating or expanding an existing test plan based on new information or analysis.
*   Performing static analysis on a test plan.

**Syntax:**

```bash
mmat build <input_identifier> --input-type <type> --output <output_path> --config <config_file> [options]
```

*   `<input_identifier>`: The source from which to build the test plan (e.g., path to a functional description file, a URL, etc.).
*   `--input-type <type>`: Specifies the format or nature of the input (e.g., `markdown`, `url`, `json`).
*   `--output <output_path>`: The path where the generated or processed test plan should be saved (e.g., `tests/generated/new_test_plan.yaml`).
*   `--config <config_file>`: Specifies the path to your MMAT configuration file, particularly important here for configuring the models used for generation/processing.
*   `[options]`: Additional options might control the generation process, output format, etc.

**Example:**

```bash
mmat build functional_description.md --input-type markdown --output tests/generated/auth_tests.yaml --config config/config.yaml
```

This command would attempt to generate a test plan in YAML format at `tests/generated/auth_tests.yaml` based on the content of `functional_description.md`, using the models and settings defined in `config/config.yaml`.

Refer to the documentation (to be created) for more detailed usage instructions and configuration options.

**Example of Functional Description Input (`functional_description.md`):**

```markdown
# User Authentication Feature

## Login

Users should be able to log in to the application using their registered username and password.

**Successful Login:**
- Navigate to the login page.
- Enter a valid username in the username field.
- Enter a valid password in the password field.
- Click the "Login" button.
- The user should be redirected to the dashboard page.

**Failed Login (Invalid Password):**
- Navigate to the login page.
- Enter a valid username.
- Enter an incorrect password.
- Click the "Login" button.
- An error message should be displayed on the login page.

## Registration

Users should be able to register for a new account.

**Successful Registration:**
- Navigate to the registration page.
- Enter a desired username in the username field.
- Enter a desired password in the password field.
- Click the "Register" button.
- The user should be redirected to a registration success page.
```

### `mmat export`

The `mmat export` command is used to convert an existing MMAT test plan into executable code in a specific format, such as Playwright Python code. This allows users to leverage the test plans generated or defined within MMAT for execution outside the MMAT framework, or as a starting point for further manual scripting.

When you run the `mmat export` command, MMAT will:

1. Load the specified test plan.
2. Process the test plan steps and translate them into the syntax of the target format (e.g., Playwright Python API calls).
3. Save the generated code to the specified output file.

**Syntax:**

```bash
mmat export <test_plan_path> --output <output_path> [--force]
```

*   `<test_plan_path>`: The path to the MMAT test plan file (e.g., `tests/functional/login_test_plan.yaml`).
*   `--output <output_path>`: The path where the generated code should be saved (e.g., `exported_tests/login_test.py`).
*   `--force` (Optional): Overwrite the output file if it already exists.

**Example:**

```bash
mmat export tests/functional/login_test_plan.yaml --output exported_tests/login_test.py
```

This command would export the test plan defined in `tests/functional/login_test_plan.yaml` to a Playwright Python file named `login_test.py` in the `exported_tests` directory.

**Example of Generated Playwright Code (`exported_tests/login_test.py`):**

```python
import pytest
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
```

## Creating Tests

MMAT uses a model-based approach to generate test plans (suites and cases) from functional descriptions or structured data. While the primary method is model-driven, you can also define tests manually.

A test plan is typically defined in a structured format (e.g., YAML or JSON). It consists of one or more test suites, each containing multiple test cases. Each test case is composed of a series of test steps.

Here's a conceptual example of a test plan structure:

```yaml
test_plan:
  name: User Authentication Tests
  description: Tests for user login and registration features
  test_suites:
    - name: Login Functionality
      description: Tests related to user login
      test_cases:
        - name: Successful Login
          description: Verify a user can log in with valid credentials
          steps:
            - action: navigate
              target: /login
              description: Go to the login page
            - action: fill
              selector: '#username'
              value: testuser
              description: Enter username
            - action: fill
              selector: '#password'
              value: password123
              description: Enter password
            - action: click
              selector: '#login-button'
              description: Click the login button
            - action: assert_url
              expected: /dashboard
              description: Verify redirection to dashboard
    - name: Registration Functionality
      description: Tests related to user registration
      test_cases:
        # ... more test cases and steps
```

The specific actions available in `steps` depend on the configured environment and plugins.

## Contributing (Planned)

Contributions are welcome! Please see the CONTRIBUTING.md (to be created) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   Mention any libraries, tools, or resources that were helpful.
