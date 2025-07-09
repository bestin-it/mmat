import base64
import requests
from typing import Any, Dict, List, Tuple
from mmat.models.vision_model import VisionModel # Import VisionModel from the correct path
from mmat.utils.logger import Logger

class LocalApiVisionModel(VisionModel):
    """
    Vision model implementation that interacts with a local API endpoint
    (e.g., LM Studio) for multimodal analysis.
    """
    def __init__(self, api_url: str, model_name: str):
        """
        Initializes the LocalApiVisionModel.

        Args:
            api_url: The URL of the local API endpoint (e.g., http://localhost:1234/v1).
            model_name: The name of the model to use (e.g., mistralai/mistral-small-3.2).
        """
        self.logger = Logger(__name__)
        self.api_url = api_url
        self.model_name = model_name
        self.logger.info(f"Initialized LocalApiVisionModel for {model_name} at {api_url}")

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encodes an image file to a base64 string."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            self.logger.error(f"Image file not found: {image_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error encoding image {image_path}: {e}")
            raise

    def analyze_screenshot(self, screenshot_path: str) -> Dict[str, Any]:
        """
        Analyzes a screenshot using the local multimodal model.

        Args:
            screenshot_path: The file path to the screenshot image.

        Returns:
            A dictionary containing the visual analysis results.
        """
        self.logger.info(f"Sending screenshot {screenshot_path} for analysis to {self.api_url}")
        base64_image = self._encode_image_to_base64(screenshot_path)

        # Construct the payload for the local API (assuming OpenAI-like chat completion format)
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this screenshot and describe its content, layout, and any interactive elements."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 1000 # Adjust as needed
        }

        try:
            response = requests.post(f"{self.api_url}/chat/completions", json=payload)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            analysis_result = response.json()
            self.logger.info("Received analysis result from local API.")
            # The structure of analysis_result depends on the API response format.
            # We'll need to parse this later in ScreenshotAnalyzer.
            return analysis_result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling local vision API: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error processing vision API response: {e}")
            raise

    def identify_element_visually(self, screenshot_path: str, description: str) -> Dict[str, Any]:
        """
        Identifies a specific element within a screenshot based on a description
        using the local multimodal model.

        Args:
            screenshot_path: The file path to the screenshot image.
            description: A natural language description of the element to find.

        Returns:
            A dictionary containing information about the identified element,
            including visual references like BBOX coordinates, OCR text, or a textual description.
            Returns an empty dictionary or None if the element cannot be identified.
        """
        self.logger.info(f"Attempting to visually identify element '{description}' in {screenshot_path}")
        base64_image = self._encode_image_to_base64(screenshot_path)

        # Construct the payload for the local API
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Identify the element described as '{description}' in this screenshot. Provide its bounding box coordinates (x1, y1, x2, y2) if possible, or a textual description if coordinates are not available. Respond in JSON format like {{ \"element\": {{ \"description\": \"...\", \"bbox\": [x1, y1, x2, y2] }} }} or {{ \"element\": {{ \"description\": \"...\" }} }} if no bbox." },
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 500 # Adjust as needed
        }

        try:
            response = requests.post(f"{self.api_url}/chat/completions", json=payload)
            response.raise_for_status()
            api_response = response.json()

            # Attempt to parse the response content, assuming the model tries to output JSON
            # This parsing might need refinement based on actual model output
            if api_response and api_response.get("choices"):
                model_output = api_response["choices"][0]["message"]["content"]
                self.logger.debug(f"Model raw output for identification: {model_output}")
                # Try to find and parse JSON within the output
                try:
                    # Simple attempt to extract JSON block if model wraps it
                    import json
                    # Find the first and last curly brace to extract potential JSON
                    json_start = model_output.find('{')
                    json_end = model_output.rfind('}')
                    if json_start != -1 and json_end != -1 and json_end > json_start:
                         json_string = model_output[json_start : json_end + 1]
                         element_info = json.loads(json_string).get("element")
                         if element_info:
                             self.logger.info(f"Identified element visually: {element_info}")
                             return element_info
                         else:
                             self.logger.warning("Model output did not contain expected 'element' key.")
                             return {}
                    else:
                         self.logger.warning("Could not find JSON structure in model output.")
                         return {} # Return empty if JSON structure not found
                except json.JSONDecodeError:
                    self.logger.warning("Failed to decode JSON from model output.")
                    # If JSON parsing fails, return the raw text description
                    return {"description": model_output.strip()}
                except Exception as e:
                    self.logger.error(f"Error parsing model output for identification: {e}")
                    return {} # Return empty on parsing error
            else:
                self.logger.warning("No valid response or choices from local vision API for identification.")
                return {} # Return empty if no valid response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling local vision API for identification: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error during visual identification: {e}")
            raise

# Note: The actual integration of this model into the MMAT framework
# (e.g., loading it based on config.yaml) will need to be handled
# in the appropriate MMAT initialization logic (likely in mmat/core/mmat.py
# or mmat/config/config_manager.py).
