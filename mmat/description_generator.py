import ast
import uuid
from typing import Dict, Any, List, Union, Optional

from mmat.core.test_case import TestCase
from mmat.core.test_step import TestStep
from mmat.core.test_suite import TestSuite
from mmat.models.reasoning_model import ReasoningModel # Assuming this class exists

class DescriptionGenerator:
    """
    Generates a human-readable functional description from an MMAT TestSuite (as a dictionary).
    """
    def __init__(self, reasoning_model: ReasoningModel):
        """
        Initializes the DescriptionGenerator with a reasoning model.

        Args:
            reasoning_model: An instance of a configured ReasoningModel.
        """
        self.reasoning_model = reasoning_model

    def generate_description(self, test_suite_dict: Dict[str, Any]) -> str: # Changed type hint to Dict
        """
        Generates a functional description for the given TestSuite dictionary using the reasoning model.

        Args:
            test_suite_dict: The TestSuite dictionary to describe.

        Returns:
            A string containing the generated functional description.
        """
        # Prepare the input for the reasoning model
        test_suite_representation = self._format_test_suite_for_llm(test_suite_dict) # Pass dictionary

        # Construct the prompt for the LLM
        prompt_messages = [
            {"role": "system", "content": "You are an expert in technical documentation. Your task is to generate a concise and clear functional description based *only* on the provided test suite structure and steps. Do not include any conversational filler, introductions, or conclusions. Provide only the functional description."},
            {"role": "user", "content": f"Test Suite:\n{test_suite_representation}\n\nFunctional Description:"}
        ]

        print("[DescriptionGenerator] Sending prompt to reasoning model...")
        try:
            generated_text = self.reasoning_model.generate_text(prompt_messages) # Pass messages list
            print("[DescriptionGenerator] Received response from reasoning model.")

            # Post-process to remove conversational filler if present
            lines = generated_text.strip().split('\n')
            cleaned_lines = []
            in_preamble = True
            for line in lines:
                stripped_line = line.strip()
                if in_preamble:
                    # Check for common conversational starts or internal thought patterns
                    if not (stripped_line.startswith("Okay, so") or
                            stripped_line.startswith("First, I need to understand") or
                            stripped_line.startswith("Given that") or
                            stripped_line.startswith("But the task") or
                            stripped_line.startswith("Perhaps the task") or
                            stripped_line.startswith("So, based") or
                            stripped_line.startswith("Alternatively,") or
                            stripped_line.startswith("Wait, looking back") or
                            stripped_line.startswith("This is an unnamed test suite") or
                            stripped_line.startswith("The Unnamed Test Suite is")):
                        in_preamble = False
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            
            final_description = "\n".join(cleaned_lines).strip()
            
            if not final_description or final_description.startswith("Okay,") or final_description.startswith("First,"):
                return "A functional description could not be generated due to an issue with the reasoning model's output."

            return final_description

        except Exception as e:
            print(f"[DescriptionGenerator] Error calling reasoning model: {e}")
            return f"Error generating description: {e}"

    def _format_test_suite_for_llm(self, test_suite_dict: Dict[str, Any]) -> str: # Changed type hint to Dict
        """
        Formats the TestSuite dictionary into a string representation suitable for an LLM.
        """
        formatted_string = f"Test Suite Name: {test_suite_dict.get('name', 'Unnamed Test Suite')}\n"
        if test_suite_dict.get('description'):
             formatted_string += f"Test Suite Description: {test_suite_dict.get('description')}\n"
        formatted_string += "\n"

        for i, test_case_dict in enumerate(test_suite_dict.get('test_cases', [])): # Iterate over list of dicts
            formatted_string += f"Test Case {i+1}: {test_case_dict.get('name', 'Unnamed Test Case')}\n"
            if test_case_dict.get('description'):
                formatted_string += f"  Description: {test_case_dict.get('description')}\n"
            formatted_string += "  Steps:\n"
            for j, step_dict in enumerate(test_case_dict.get('steps', [])): # Iterate over list of dicts
                step_details = f"    Step {j+1}: Action='{step_dict.get('action')}'"
                if step_dict.get('target'):
                    step_details += f", Target='{step_dict.get('target')}'"
                if step_dict.get('args'):
                    step_details += f", Args={step_dict.get('args')}"
                if step_dict.get('expected_result'):
                    step_details += f", Expected Result='{step_dict.get('expected_result')}'"
                if step_dict.get('description'):
                     step_details += f", Description='{step_dict.get('description')}'"
                formatted_string += f"{step_details}\n"
            formatted_string += "\n"

        return formatted_string
