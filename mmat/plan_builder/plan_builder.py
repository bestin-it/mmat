import os
import yaml
import json
from typing import Any, Dict, List

from mmat.models.reasoning_model import ReasoningModel # Import ReasoningModel

class PlanBuilder:
    """
    Handles loading and parsing MMAT test plans and generating them from descriptions.
    """
    def __init__(self, config, reasoning_model: ReasoningModel = None):
        """
        Initializes the PlanBuilder.

        Args:
            config (dict): Configuration for the plan builder.
            reasoning_model (ReasoningModel, optional): An instance of a ReasoningModel. Defaults to None.
        """
        self.config = config
        self.reasoning_model = reasoning_model
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

        if not self.reasoning_model:
            print("[PlanBuilder] Error: Reasoning model is not available. Cannot generate test plan from description.")
            return None

        # Prepare context for the reasoning model
        context = {
            "description": description,
            # Add other relevant context here, e.g.,
            # "current_url": url,
            # "available_elements": "..." # Could add DOM structure analysis results here later
        }
        if url:
             context["start_url"] = url # Add start URL to context if provided

        try:
            # Use the reasoning model to generate test steps
            generated_steps = self.reasoning_model.generate_test_plan(description, context)

            if generated_steps is None:
                 print("[PlanBuilder] Reasoning model failed to generate test steps.")
                 return None

            # Construct the full test plan structure
            generated_plan = {
                "test_plan": {
                    "name": f"Generated Test Plan for: {description[:50]}...",
                    "description": description,
                    "test_suites": [
                        {
                            "name": "Default Test Suite",
                            "description": f"Test suite generated from {description[:50]}...",
                            "test_cases": [
                                {
                                    "name": "Default Test Case",
                                    "description": f"Test case generated from {description[:50]}...",
                                    "steps": generated_steps
                                }
                            ]
                        }
                    ]
                }
            }

            print("[PlanBuilder] Test plan generated using reasoning model.")
            return generated_plan

        except Exception as e:
            print(f"[PlanBuilder] An error occurred while generating plan with reasoning model: {e}")
            return None

    # Add other methods related to plan building or validation
