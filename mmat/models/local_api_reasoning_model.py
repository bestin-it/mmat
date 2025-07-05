# MMAT Local API Reasoning Model Implementation

import requests
import json # Import the json module
from typing import Any, Dict, List

from .reasoning_model import ReasoningModel

class LocalApiReasoningModel(ReasoningModel):
    """
    Reasoning model implementation that interacts with a local LLM API endpoint.
    """
    def __init__(self, api_url: str, model_name: str):
        """
        Initializes the LocalApiReasoningModel.

        Args:
            api_url: The URL of the local LLM API endpoint (e.g., http://172.29.32.1:1234/v1).
            model_name: The name of the model to use (e.g., mistralai/magistral-small).
        """
        self.api_url = api_url
        self.model_name = model_name
        print(f"[LocalApiReasoningModel] Initialized with API URL: {self.api_url}, Model: {self.model_name}")

    def analyze_dom(self, dom_structure: str) -> Dict[str, Any]:
        """
        Analyzes the HTML DOM structure using the reasoning model.
        (Implementation needed)
        """
        print("[LocalApiReasoningModel] analyze_dom called (implementation needed)")
        # Placeholder implementation
        return {"analysis_result": "DOM analysis not implemented yet"}

    def generate_test_plan(self, description: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates a sequence of test steps based on a natural language description
        and current context using the reasoning model.

        Args:
            description: A natural language description of the test objective.
            context: A dictionary containing relevant context (e.g., start URL, test data).

        Returns:
            A list of dictionaries, where each dictionary represents a test step.
        """
        print(f"[LocalApiReasoningModel] Generating test plan for description: '{description}'")
        print(f"[LocalApiReasoningModel] Context: {context}")

        # Construct the prompt for the LLM
        # This prompt needs to guide the LLM to output test steps in a structured format (e.g., JSON)
        prompt_messages = [
            {"role": "system", "content": "You are a test automation expert. Your task is to convert natural language descriptions of user interactions into a sequence of structured test steps in JSON format. Each step should be an object with 'action' (e.g., 'navigate', 'fill', 'click', 'assert_url', 'assert_element_visible') and 'parameters' (a dictionary specific to the action). For 'fill' and 'click', include a 'selector'. For 'navigate', include a 'url'. For assertions, include 'expected' or 'selector'. Provide only the JSON array of steps."},
            {"role": "user", "content": f"Generate test steps for the following scenario:\nDescription: {description}\nContext: {context}\n\nOutput the steps as a JSON array."}
        ]

        try:
            # Make the API call to the local LLM server
            response = requests.post(
                f"{self.api_url}/chat/completions", # Assuming chat completions endpoint
                json={
                    "model": self.model_name,
                    "messages": prompt_messages,
                    "max_tokens": 1000, # Adjust as needed
                    "temperature": 0.7, # Adjust as needed
                    # Add other parameters if required by the API
                }
            )
            response.raise_for_status() # Raise an exception for bad status codes

            api_response = response.json()
            print(f"[LocalApiReasoningModel] Received API response: {api_response}")

            # Parse the API response to extract test steps
            generated_steps = self._parse_llm_response(api_response)

            if generated_steps:
                print("[LocalApiReasoningModel] Successfully generated steps from LLM.")
                return generated_steps
            else:
                print("[LocalApiReasoningModel] LLM response did not contain valid test steps.")
                return None

        except requests.exceptions.RequestException as e:
            print(f"[LocalApiReasoningModel] Error calling LLM API: {e}")
            return None
        except Exception as e:
            print(f"[LocalApiReasoningModel] An unexpected error occurred during LLM interaction: {e}")
            import traceback
            traceback.print_exc() # Print traceback for debugging
            return None

    def identify_element_by_structure(self, dom_structure: str, description: str) -> Dict[str, Any]:
        """
        Identifies a specific element within the DOM structure based on a description
        using the reasoning model.
        (Implementation needed)
        """
        print("[LocalApiReasoningModel] identify_element_by_structure called (implementation needed)")
        # Placeholder implementation
        return {"element_selector": "body", "confidence": 0.5}

    def _parse_llm_response(self, api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parses the LLM API response to extract test steps.
        Assumes the LLM returns a JSON array of steps within the first message content.
        """
        print("[LocalApiReasoningModel] Parsing LLM response...")
        try:
            # Assuming the response structure is similar to OpenAI chat completions
            # and the generated steps are in the content of the first message choice.
            choices = api_response.get("choices", [])
            if not choices:
                print("[LocalApiReasoningModel] No choices found in LLM response.")
                return []

            message = choices[0].get("message", {})
            if not message:
                print("[LocalApiReasoningModel] No message found in first choice.")
                return []

            content = message.get("content", "")
            if not content:
                print("[LocalApiReasoningModel] No content found in message.")
                return []

            print(f"[LocalApiReasoningModel] Raw LLM content: {content}")

            # Attempt to parse the content as a JSON array
            # The LLM might include introductory/trailing text, so try to extract the JSON part
            # A more robust parser might be needed depending on the LLM's output
            try:
                # Simple attempt to find and parse the first JSON array
                json_start = content.find('[')
                json_end = content.rfind(']')
                if json_start != -1 and json_end != -1 and json_end > json_start:
                    json_string = content[json_start : json_end + 1]
                    steps_list = json.loads(json_string)
                    print("[LocalApiReasoningModel] Successfully parsed JSON steps from LLM content.")
                    # Basic validation: check if it's a list of dictionaries
                    if isinstance(steps_list, list) and all(isinstance(step, dict) for step in steps_list):
                        return steps_list
                    else:
                        print("[LocalApiReasoningModel] Parsed JSON is not a list of dictionaries.")
                        return []
                else:
                    print("[LocalApiReasoningModel] Could not find a JSON array in LLM content.")
                    return []
            except json.JSONDecodeError as e:
                print(f"[LocalApiReasoningModel] JSON parsing failed: {e}")
                return []

        except Exception as e:
            print(f"[LocalApiReasoningModel] An unexpected error occurred during response parsing: {e}")
            import traceback
            traceback.print_exc() # Print traceback for debugging
            return []
