from typing import Dict, Any, List, Union

from mmat.core.test_suite import TestSuite
from mmat.core.test_case import TestCase
from mmat.core.test_step import TestStep
from mmat.models.reasoning_model import ReasoningModel # Assuming this class exists

class DescriptionGenerator:
    """
    Generates a human-readable functional description from an MMAT TestSuite.
    """
    def __init__(self, reasoning_model: ReasoningModel):
        """
        Initializes the DescriptionGenerator with a reasoning model.

        Args:
            reasoning_model: An instance of a configured ReasoningModel.
        """
        self.reasoning_model = reasoning_model

    def generate_description(self, test_suite: TestSuite) -> str:
        """
        Generates a functional description for the given TestSuite using the reasoning model.

        Args:
            test_suite: The TestSuite object to describe.

        Returns:
            A string containing the generated functional description.
        """
        # Prepare the input for the reasoning model
        # This could be a structured text representation of the test suite
        test_suite_representation = self._format_test_suite_for_llm(test_suite)

        # Construct the prompt for the LLM
        prompt = f"""
Generate a concise and clear functional description based on the following test suite structure and steps.
Focus on describing the user flow and the purpose of the tests.

Test Suite:
{test_suite_representation}

Functional Description:
"""

        print("[DescriptionGenerator] Sending prompt to reasoning model...")
        # Call the reasoning model to generate the description
        # Assuming the ReasoningModel has a method like 'generate_text'
        try:
            generated_text = self.reasoning_model.generate_text(prompt)
            print("[DescriptionGenerator] Received response from reasoning model.")
            return generated_text.strip()
        except Exception as e:
            print(f"[DescriptionGenerator] Error calling reasoning model: {e}")
            return f"Error generating description: {e}" # Return error message or raise exception

    def _format_test_suite_for_llm(self, test_suite: TestSuite) -> str:
        """
        Formats the TestSuite object into a string representation suitable for an LLM.
        """
        formatted_string = f"Test Suite Name: {test_suite.name}\n"
        if test_suite.description:
             formatted_string += f"Test Suite Description: {test_suite.description}\n"
        formatted_string += "\n"

        for i, test_case in enumerate(test_suite.test_cases):
            formatted_string += f"Test Case {i+1}: {test_case.name}\n"
            if test_case.description:
                formatted_string += f"  Description: {test_case.description}\n"
            formatted_string += "  Steps:\n"
            for j, step in enumerate(test_case.steps):
                step_details = f"    Step {j+1}: Action='{step.action}'"
                if step.target:
                    step_details += f", Target='{step.target}'"
                if step.args:
                    step_details += f", Args={step.args}"
                if step.expected_result:
                    step_details += f", Expected Result='{step.expected_result}'"
                if step.description:
                     step_details += f", Description='{step.description}'"
                formatted_string += f"{step_details}\n"
            formatted_string += "\n"

        return formatted_string

# Example Usage (for testing during development)
# if __name__ == "__main__":
#     # This requires a running reasoning model configured in config.yaml
#     # and the MMAT class to be initialized to provide the model instance.
#     # This example is conceptual and needs a proper MMAT setup to run.
#     print("Conceptual example usage of DescriptionGenerator")
#     # try:
#     #     # Assuming you have an MMAT instance and can access its reasoning model
#     #     # from mmat.core.mmat import MMAT
#     #     # mmat_app = MMAT() # This requires config.yaml and potentially running services
#     #     # reasoning_model_instance = mmat_app.reasoning_model
#
#     #     # Create a dummy TestSuite for demonstration
#     #     dummy_step1 = TestStep(action="navigate", target="http://example.com/login", description="Go to login page")
#     #     dummy_step2 = TestStep(action="fill", target="#username", args={"value": "testuser"}, description="Enter username")
#     #     dummy_case = TestCase(name="Login Test", description="Verify user login", steps=[dummy_step1, dummy_step2])
#     #     dummy_suite = TestSuite(name="Authentication Suite", test_cases=[dummy_case])
#
#     #     # if reasoning_model_instance:
#     #     #     generator = DescriptionGenerator(reasoning_model_instance)
#     #     #     description = generator.generate_description(dummy_suite)
#     #     #     print("\nGenerated Description:")
#     #     #     print(description)
#     #     # else:
#     #     #     print("Reasoning model not initialized.")
#
#     # except Exception as e:
#     #     print(f"An error occurred during conceptual example: {e}")
