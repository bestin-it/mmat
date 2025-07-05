# mmat/analysis/analyzer.py

from mmat.analysis.html_analyzer import HTMLAnalyzer
from mmat.analysis.screenshot_analyzer import ScreenshotAnalyzer
from mmat.graph.graph_api import GraphAPI
from mmat.models.reasoning_model import ReasoningModel
from mmat.models.vision_model import VisionModel
from mmat.environment.environment import Environment
from mmat.utils.logger import Logger
from typing import Dict, Any

class Analyzer:
    """
    Coordinates different analysis modules (HTML, Screenshot) to gather information
    about the application under test and update the knowledge graph.
    """
    def __init__(self, reasoning_model: ReasoningModel, vision_model: VisionModel, graph_api: GraphAPI, environment: Environment):
        """
        Initializes the Analyzer.

        Args:
            reasoning_model: An instance of the ReasoningModel.
            vision_model: An instance of the VisionModel.
            graph_api: An instance of the GraphAPI.
            environment: The current test environment.
        """
        self.logger = Logger(__name__)
        self.html_analyzer = HTMLAnalyzer(reasoning_model, graph_api, environment)
        self.screenshot_analyzer = ScreenshotAnalyzer(vision_model, graph_api)
        self.graph_api = graph_api

    def perform_analysis(self, screenshot_path: str) -> Dict[str, Any]:
        """
        Performs a comprehensive analysis including DOM and screenshot analysis.

        Args:
            screenshot_path: The file path to the screenshot image for visual analysis.

        Returns:
            A dictionary containing the combined analysis results.
        """
        self.logger.info("Performing comprehensive analysis...")
        combined_results = {}

        # Perform HTML analysis
        try:
            html_analysis_result = self.html_analyzer.analyze_dom()
            combined_results["html_analysis"] = html_analysis_result
            self.logger.info("HTML analysis completed.")
        except Exception as e:
            self.logger.error(f"HTML analysis failed: {e}")
            # Decide how to handle failure: continue, raise, etc.
            combined_results["html_analysis_error"] = str(e)


        # Perform screenshot analysis
        try:
            screenshot_analysis_result = self.screenshot_analyzer.analyze_screenshot(screenshot_path)
            combined_results["screenshot_analysis"] = screenshot_analysis_result
            self.logger.info("Screenshot analysis completed.")
        except Exception as e:
            self.logger.error(f"Screenshot analysis failed: {e}")
            # Decide how to handle failure: continue, raise, etc.
            combined_results["screenshot_analysis_error"] = str(e)

        self.logger.info("Comprehensive analysis complete.")
        return combined_results

    # Add methods for other types of analysis if needed
