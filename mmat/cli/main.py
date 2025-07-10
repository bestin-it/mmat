import argparse
import sys
import os

# Add the project root to the Python path to allow for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from mmat.core.mmat import MMAT # Uncomment the import

def main():
    """Main entry point for the MMAT CLI."""
    print("[DEBUG] main() function in mmat/cli/main.py is being executed.")
    parser = argparse.ArgumentParser(description="MMAT - Model-based Multi-Agent Testing Framework")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a new E2E test plan from a description")
    generate_parser.add_argument(
        "--desc",
        required=True,
        help="Description of the test to generate",
    )
    generate_parser.add_argument(
        "--output",
        required=True,
        help="Output path for the generated test plan file (JSON)",
    )
    generate_parser.add_argument(
        "--force",
        action="store_true", # Store True if flag is present
        help="Overwrite output file if it already exists",
    )

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a test plan")
    run_parser.add_argument("test", help="Path to the test plan file (YAML or JSON)") # Changed to 'test' to match MMAT.run args
    run_parser.add_argument(
        "--step", # Changed to 'step' to match MMAT.run args
        type=int,
        default=1,
        help="Step number to start execution from (1-based index)",
    )
    run_parser.add_argument(
        "--config",
        default="config/config.yaml", # Default config path
        help="Path to the configuration file (YAML or JSON)",
    )
    # Add other potential run options here (e.g., --reporter, --environment)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new MMAT project structure")
    init_parser.add_argument(
        "project_name",
        nargs="?", # Make project_name optional
        default="my_mmat_project", # Default project name
        help="Name of the project directory to create (default: my_mmat_project)",
    )

    # Export command (new)
    export_parser = subparsers.add_parser("export", help="Export an MMAT test plan to a different format (e.g., Playwright code)")
    export_parser.add_argument(
        "test_plan_path",
        help="Path to the MMAT test plan file (YAML or JSON)",
    )
    export_parser.add_argument(
        "--output",
        help="Optional output path for the generated code. If not provided, prints to stdout.",
    )
    export_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists",
    )

    # Import command (new)
    import_parser = subparsers.add_parser("import-e2e", help="Import an E2E test script (e.g., Playwright) and convert it to an MMAT test plan")
    import_parser.add_argument(
        "input_file",
        help="Path to the E2E test script file (e.g., Playwright Python)",
    )
    import_parser.add_argument(
        "--output",
        help="Optional output path for the generated MMAT test plan file (YAML or JSON). If not provided, prints to stdout.",
    )
    import_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists",
    )

    # Describe command
    describe_parser = subparsers.add_parser("describe", help="Convert an MMAT test plan into a human-readable functional description")
    describe_parser.add_argument(
        "test_plan_path",
        help="Path to the MMAT test plan file (YAML or JSON)",
    )
    describe_parser.add_argument(
        "--output",
        help="Optional output path for the generated functional description file (e.g., Markdown). If not provided, prints to stdout.",
    )
    describe_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists",
    )

    # Feedback command
    feedback_parser = subparsers.add_parser("feedback", help="Provide feedback on a test run or specific test step")
    feedback_parser.add_argument(
        "test",
        help="Path to the test plan file (YAML or JSON) for which to provide feedback",
    )
    feedback_parser.add_argument(
        "--step",
        type=int,
        help="Optional: The specific step number (1-based index) to provide feedback for. If not provided, feedback applies to the entire test.",
    )
    feedback_parser.add_argument(
        "--report",
        help="Optional: Path to the test report file (e.g., JSON) to use for context.",
    )
    feedback_parser.add_argument(
        "--config",
        default="config/config.yaml", # Default config path
        help="Path to the configuration file (YAML or JSON)",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List available test plans or functional descriptions")
    list_parser.add_argument(
        "--type",
        choices=["functional", "e2e", "all"],
        default="all",
        help="Type of files to list: 'functional' (test plans), 'e2e' (E2E scripts), or 'all' (default)",
    )
    list_parser.add_argument(
        "--path",
        default=".",
        help="Path to the directory to search for files (default: current directory)",
    )

    # Show command
    show_parser = subparsers.add_parser("show", help="Display the content of a test plan or functional description")
    show_parser.add_argument(
        "file_path",
        help="Path to the file to display (test plan or functional description)",
    )

    args = parser.parse_args()

    # Instantiate MMAT with the specified config path
    config_path = args.config if hasattr(args, 'config') else "config/config.yaml"
    mmat_app = MMAT(config_path=config_path)
    mmat_app.run(args)


if __name__ == "__main__":
    main()
