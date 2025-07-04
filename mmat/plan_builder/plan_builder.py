import os
import yaml
import json

class PlanBuilder:
    """
    Handles loading and parsing MMAT test plans.
    """
    def __init__(self, config):
        """
        Initializes the PlanBuilder.

        Args:
            config (dict): Configuration for the plan builder.
        """
        self.config = config
        print("[PlanBuilder] Initialized.")

    def load_plan(self, test_plan_path):
        """
        Loads and parses a test plan from a file.

        Args:
            test_plan_path (str): Path to the test plan file (YAML or JSON).

        Returns:
            dict: The parsed test plan dictionary, or None if loading fails.
        """
        if not os.path.exists(test_plan_path):
            print(f"[PlanBuilder] Error: Test plan file not found at {test_plan_path}")
            return None

        _, file_extension = os.path.splitext(test_plan_path)
        file_extension = file_extension.lower()

        try:
            with open(test_plan_path, 'r') as f:
                if file_extension in ['.yaml', '.yml']:
                    test_plan = yaml.safe_load(f)
                elif file_extension == '.json':
                    test_plan = json.load(f)
                else:
                    print(f"[PlanBuilder] Error: Unsupported file format for test plan: {file_extension}")
                    return None
            print(f"[PlanBuilder] Successfully loaded test plan from {test_plan_path}")
            return test_plan
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            print(f"[PlanBuilder] Error parsing test plan file {test_plan_path}: {e}")
            return None
        except Exception as e:
            print(f"[PlanBuilder] An unexpected error occurred while loading {test_plan_path}: {e}")
            return None

    def generate_plan_from_description(self, description, url=None):
        """
        Generates a test plan from a natural language description.

        Args:
            description (str): The natural language description of the test.
            url (str, optional): The URL to interact with. Defaults to None.

        Returns:
            dict: The generated test plan dictionary, or None if generation fails.
        """
        print(f"[PlanBuilder] Generating plan from description: '{description}'")

        if url:
            print(f"[PlanBuilder] Navigating to URL: {url}")
            # Use puppeteer tool to navigate and potentially analyze the page
            # This part needs actual tool call logic, which is complex within a method.
            # For now, simulate interaction and return a placeholder plan.
            print("[PlanBuilder] Simulating browser interaction and analysis...")
            # In a real implementation, this would involve using MCP tools
            # like puppeteer_navigate, puppeteer_evaluate, etc.
            # and analysis modules to understand the page and description.

        # Placeholder for generated plan structure
        # This structure should match the expected format for test plans
        # e.g., a list of steps with type, parameters, etc.
        generated_plan = {
            "name": f"Generated Test Plan for: {description[:50]}...",
            "description": description,
            "steps": [
                {"type": "web.navigate", "params": {"url": url if url else "about:blank"}},
                # Add more steps based on description and analysis
                {"type": "web.comment", "params": {"text": "Placeholder step based on description and analysis."}}
            ]
        }

        print("[PlanBuilder] Placeholder plan generated.")
        return generated_plan

    # Add other methods related to plan building or validation
