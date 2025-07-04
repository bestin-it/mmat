# MMAT - Model-based Manual Acceptance Testing framework

MMAT is a Python framework designed to facilitate model-based manual acceptance testing. It leverages various components like reasoning models, vision models, and environments (like browsers) to automate the process of generating, executing, and reporting on manual acceptance tests based on functional descriptions or other data sources.

The core idea is to start with a simple description or prompt of the desired functionality. MMAT can then interact with a given URL or web page(s) to understand the user interface and behavior. Based on this analysis, the framework aims to generate a structured test plan, typically in JSON or YAML format. This plan describes the test with a clear list of steps needed to repeat the manual acceptance test.

Furthermore, MMAT is designed to allow users to generate executable code, such as Playwright Python scripts, directly from this structured test plan. The framework should also provide the capability to run this generated code, enabling automated execution of the manual acceptance tests defined through the model-based approach.

## Installation

MMAT is a Python package.

**Prerequisites:**

*   Python 3.8+

### Installing via Pip from GitHub

You can install MMAT directly from the GitHub repository using pip:

```bash
pip install git+https://github.com/yourusername/mmat.git
```

Replace `yourusername` with the actual GitHub username or organization.

### Setting up the 'mmat' Alias on Windows

To set up the `mmat` alias on Windows, run the provided `setup.py` script from the project root (`c:/Projects/Matt`):

```bash
python setup.py install
```

This script creates the `mmat` alias, allowing you to run MMAT commands from any directory in your Windows terminal (Command Prompt or PowerShell).

Example usage:

```bash
mmat --help
```

## Project Setup and Structure

MMAT provides an `init` command to help you quickly set up a basic project structure. This command creates a directory with a suggested layout for your test assets and configuration.

To initialize a new MMAT project, navigate to the directory where you want to create the project and run:

```bash
mmat init [project_name]
```

*   `[project_name]` (Optional): The name of the directory to create for your project. If not provided, it defaults to `my_mmat_project`.

This will create a directory structure similar to:

```
[project_name]/
├── functional_descriptions/
│   └── # Your functional descriptions go here (e.g., login.md)
├── tests/
│   ├── functional/
│   │   └── # Your functional test plans go here (e.g., login_test_plan.yaml)
│   └── e2e/
│       └── # Your exported e2e tests go here (e.g., login_test.py)
├── config/
│   └── config.yaml # Your MMAT configuration file
└── # Other project files (e.g., requirements.txt, README.md)
```

After initialization, you’ll integrate the `mmat` library into your project’s dependencies (e.g., adding `mmat` to `requirements.txt`).

The typical structure when using `mmat` might look like:

```
your_project/
├── functional_descriptions/
│   └── login.md
├── tests/
│   ├── functional/
│   │   └── login_test_plan.yaml
│   └── e2e/
│       └── login_test.py
├── config/
│   └── config.yaml
├── src/ # Your application source code
│   └── …
├── .gitignore
├── requirements.txt # Project dependencies
└── README.md # Project’s README
```

In this structure:

*   `functional_descriptions/`: Store your functional requirements, typically in Markdown.
*   `tests/functional/`: Store your functional test plans (YAML or JSON), which can be generated from functional descriptions or written manually.
*   `tests/e2e/`: Store exported end-to-end test scripts (e.g., Playwright Python).
*   `config/`: Keep `config.yaml` (MMAT’s global configuration for models, environments, etc.).
*   `requirements.txt`: List `mmat` and any other dependencies.

### Functional Description

Functional descriptions are the starting point for generating test plans using MMAT's `build` command. These files describe the desired behavior of your application or specific features. They are typically written in a human-readable format like Markdown.

Example: `functional_descriptions/login.md`

```markdown
# User Login Feature

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
```

### Functional Test Plan

Functional tests in MMAT are defined in structured test plans, typically in YAML or JSON format. These plans outline the sequence of steps to perform a specific test case. They can be generated automatically from functional descriptions using the `mmat build` command or written manually.

Example: `tests/functional/login_test_plan.yaml` (Generated from the functional description above)

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

### E2E Test in Playwright

MMAT can export functional test plans into executable end-to-end test scripts for frameworks like Playwright. These exported scripts can be run independently of MMAT or used as a starting point for further test development. These files are typically stored in the `tests/e2e/` directory.

Example: `tests/e2e/login_test.py` (Exported from the functional test plan above)

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

### Configuration (config.yaml) and Models

The `config.yaml` file contains the global configuration for your MMAT project. This includes settings for environments (like browsers), models (reasoning and vision), and reporting. This file is typically located at the root of your project's configuration directory.

Example: `config/config.yaml`

```yaml
environments:
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

MMAT utilizes Language Models (LLMs) and Vision Models (VMs) for various tasks, including test plan generation and analysis. The configuration for these models is managed within the `config.yaml` file, typically located in your project's `config/` directory.

The `models` section in `config.yaml` allows you to define different model providers and their specific configurations. MMAT supports various providers, and you can configure multiple models for different purposes (e.g., a reasoning model for generating test steps and a vision model for analyzing screenshots).

Example `models` section in `config/config.yaml`:

```yaml
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

  # You can add configurations for other models or providers here
  another_model:
    provider: openai
    type: llm
    config:
      model_name: gpt-4o
      api_key: ${OPENAI_API_KEY} # Using environment variable
```

Key parameters within a model configuration typically include:

*   `provider`: Specifies the service or tool providing the model (e.g., `local_api`, `local_ollama`, `openai`, `lm_studio`).
*   `type`: Indicates the type of model (e.g., `llm` for Language Models, `vision` for Vision Models).
*   `config`: A dictionary containing provider-specific settings, such as API endpoints, model names, API keys, etc.

Ensure that the `endpoint` and `model_name` in your configuration accurately reflect the models you have available and how they are being served (e.g., via LM Studio, Ollama, or a cloud service). You can use environment variables (e.g., `${OPENAI_API_KEY}`) for sensitive information like API keys.

### Setting up Local Models (LM Studio)

MMAT can utilize local Language Models (LLMs) and Vision Models (VMs) for tasks like test plan generation and analysis. LM Studio is a popular desktop application that allows you to discover, download, and run local LLMs.

Here’s how to set up LM Studio and configure MMAT to use models served by it:

1.  **Download and Install LM Studio:**
    *   Go to the [LM Studio website](https://lmstudio.ai/) and download the appropriate version for your OS (Windows, macOS, Linux).
    *   Install LM Studio following the on-screen instructions.

2.  **Download Models in LM Studio:**
    *   Open LM Studio.
    *   Use the search bar to find models. For MMAT, you’ll likely need a reasoning model (general-purpose LLM) and potentially a multimodal/vision model (e.g., LLaVA) if you plan to use vision-based features.
    *   Click “Download” next to the models you want. Choose a suitable size/quantization (e.g., Q4_K_M for a balance of speed vs. quality).

3.  **Serve Models in LM Studio:**
    *   Go to the “Local Inference Server” tab (usually the third icon from the top). Select the model to serve from the dropdown.
    *   Click “Start Server.” LM Studio will display an API endpoint (e.g., `http://localhost:1234`).

4.  **Configure MMAT’s `config.yaml`:**
    *   Open your project’s `config/config.yaml`.
    *   Modify the `models` section to point to LM Studio’s endpoint. Refer to [Section 3.4](#section-config) for a detailed example of the `config.yaml` structure.
    *   *Ensure `endpoint` matches what LM Studio shows.* The `model_name` must exactly match the model name in LM Studio. MMAT’s LM Studio provider will use this to send requests for inference.

5.  **Run MMAT:**
    *   With LM Studio running and serving the required models, you can now run MMAT commands (e.g., `mmat run`, `mmat build`) that use those local models.

## Understanding Graphs in MMAT

The `graph/` module in MMAT is planned to handle internal representations and interactions related to test flows, dependencies, or other structural aspects of the testing process. This is likely an internal component used for analysis, visualization, or orchestration, rather than requiring a separate graph database or visualization tool for basic usage.

Detailed setup for visualizing or interacting with these internal graph structures will be provided in future documentation. For standard test execution, you typically don’t need any extra graph setup beyond installing and configuring MMAT as described above.

## Usage (Planned)

MMAT provides a command-line interface (CLI) to interact with the framework, primarily through the `run` and `build` commands.

### `mmat run`

The `mmat run` command is used to execute a specified test plan. When you run a test plan, MMAT will:

1.  Load configuration from the specified `--config` file.
2.  Load the test plan (given by `<plan_identifier>` and `--plan-type`).
3.  Initialize environments and models as defined in the configuration.
4.  Iterate through test suites and test cases in the test plan.
5.  Execute each test step sequentially using the configured environment (e.g., a browser).
6.  Perform validations and assertions as defined.
7.  Collect results and generate reports using the configured reporters.

**Syntax:**

```bash
mmat run <plan_identifier> --plan-type <type> --config <config_file> [options]
```

*   `<plan_identifier>`: Path to your test plan file (e.g., `tests/functional/login_test_plan.yaml`).
*   `--plan-type <type>`: Format of the test plan (e.g., `yaml`, `json`).
*   `--config <config_file>`: Path to your MMAT configuration file (e.g., `config/config.yaml`).
*   `[options]`: Additional options (e.g., filtering test cases, verbosity).

**Example:**

```bash
mmat run tests/functional/login_test_plan.yaml --plan-type yaml --config config/config.yaml
```

This will execute the test plan in `tests/functional/login_test_plan.yaml` with settings from `config/config.yaml`.

### `mmat build`

The `mmat build` command is intended for generating or processing test plans—often using the configured models. Its primary roles may include:

*   Generating a structured test plan (YAML/JSON) from a less-structured input (e.g., a functional description) using a reasoning model.
*   Updating or expanding an existing test plan based on new information or analysis.
*   Performing static analysis on a test plan.

**Syntax:**

```bash
mmat build <input_identifier> --input-type <type> --output <output_path> --config <config_file> [options]
```

*   `<input_identifier>`: Source for building the plan (e.g., a functional description file, URL, etc.).
*   `--input-type <type>`: Format of the input (e.g., `markdown`, `url`, `json`).
*   `--output <output_path>`: Path to save the generated/processed test plan (e.g., `tests/generated/auth_tests.yaml`).
*   `--config <config_file>`: Path to your MMAT configuration file (for models, environment, etc.).
*   `[options]`: Additional options controlling generation.

**Example:**

```bash
mmat build functional_description.md --input-type markdown --output tests/generated/auth_tests.yaml --config config/config.yaml
```

This would generate a YAML test plan at `tests/generated/auth_tests.yaml` based on `functional_description.md`, using models defined in `config/config.yaml`.

### `mmat export`

The `mmat export` command converts an existing MMAT test plan into executable code (e.g., Playwright Python). This lets you run tests outside MMAT or use the generated script as a starting point.

When you run `mmat export`, MMAT will:

1. Load the specified test plan.
2. Translate test steps into the syntax of the target format (e.g., Playwright Python API calls).
3. Save the generated code to the specified output file.

**Syntax:**

```bash
mmat export <test_plan_path> --output <output_path> [--force]
```

*   `<test_plan_path>`: Path to the MMAT test plan (e.g., `tests/functional/login_test_plan.yaml`).
*   `--output <output_path>`: Path where generated code should be saved (e.g., `exported_tests/login_test.py`).
*   `--force` (Optional): Overwrite the output file if it exists.

**Example:**

```bash
mmat export tests/functional/login_test_plan.yaml --output exported_tests/login_test.py
```

This will export `tests/functional/login_test_plan.yaml` to a Playwright Python file named `login_test.py` in `exported_tests`.

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

### `mmat import-e2e`

The `mmat import-e2e` command converts an existing end-to-end test script (currently supports Playwright Python) into an MMAT functional test plan (YAML or JSON). This allows you to bring existing automated tests into the MMAT framework for management, analysis, or further processing.

When you run `mmat import-e2e`, MMAT will:

1.  Parse the specified E2E test script.
2.  Identify test cases and steps within the script.
3.  Translate the identified actions and elements into MMAT test steps.
4.  Structure the results into an MMAT TestSuite and TestCases.
5.  Output the resulting test plan in YAML or JSON format.

**Syntax:**

```bash
mmat import-e2e <input_file> [--output <output_path>] [--force]
```

*   `<input_file>`: Path to the E2E test script file (e.g., `tests/e2e/login_test.py`).
*   `--output <output_path>` (Optional): Path to save the generated MMAT test plan (e.g., `imported_plans/login_plan.yaml`). If not provided, the plan is printed to standard output.
*   `--force` (Optional): Overwrite the output file if it exists.

**Example:**

```bash
mmat import-e2e tests/e2e/test_user_login.py --output tests/functional/imported_user_login_plan.yaml
```

This will import the Playwright script `tests/e2e/test_user_login.py` and save the resulting MMAT test plan to `tests/functional/imported_user_login_plan.yaml`.

### `mmat describe`

The `mmat describe` command converts an MMAT functional test plan (YAML or JSON) into a human-readable functional description. This process utilizes a configured reasoning model (LLM) to interpret the structured test steps and generate a coherent description of the test's purpose and flow.

When you run `mmat describe`, MMAT will:

1.  Load the specified test plan file.
2.  Format the test plan data for the reasoning model.
3.  Send the formatted data as a prompt to the configured LLM.
4.  Receive the generated description from the LLM.
5.  Output the resulting description to a file or standard output.

**Syntax:**

```bash
mmat describe <test_plan_path> [--output <output_path>] [--force]
```

*   `<test_plan_path>`: Path to the MMAT test plan file (YAML or JSON).
*   `--output <output_path>` (Optional): Path to save the generated functional description file (e.g., Markdown). If not provided, prints to standard output.
*   `--force` (Optional): Overwrite the output file if it exists.

**Example:**

```bash
mmat describe tests/functional/login_test_plan.yaml --output functional_descriptions/login_description.md
```

This will load the test plan from `tests/functional/login_test_plan.yaml` and save the generated functional description to `functional_descriptions/login_description.md`.

**Example (printing to stdout):**

```bash
mmat describe tests/functional/login_test_plan.yaml
```

This will load the test plan and print the generated functional description directly to your terminal.

## Contributing (Planned)

Contributions are welcome! Please see the `CONTRIBUTING.md` (to be created) for details on how to propose changes, run tests, and submit pull requests.

## License

This project is licensed under the MIT License—see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   Mention any libraries, tools, or resources that were helpful.

## Features (Planned)

*   **Model-based Test Plan Generation:** Generate test suites and test cases from functional descriptions or structured data using AI models.
*   **Environment Interaction:** Interact with various environments (e.g., web browsers via Puppeteer) to execute test steps.
*   **Test Data Management:** Manage and utilize test data for test execution.
*   **Validation and Analysis:** Validate test results and analyze outcomes using models.
*   **Reporting:** Generate test reports in various formats.
*   **Plugin System:** Allow extending the framework with custom components (environments, reporters, models, etc.).
*   **CLI Interface:** Command-line interface for running and building test plans.
