import ast
import uuid
from typing import Dict, Any, List, Union, Optional

from mmat.core.test_case import TestCase
from mmat.core.test_step import TestStep
from mmat.core.test_suite import TestSuite

class PlaywrightImporter(ast.NodeVisitor):
    """
    Parses a Playwright Python script and converts it into an MMAT TestSuite.
    """
    def __init__(self):
        self.test_suite: Optional[TestSuite] = None
        self.current_test_case: Optional[TestCase] = None
        self.test_cases: List[TestCase] = []

    def import_from_file(self, file_path: str) -> Dict[str, Any]: # Changed return type to Dict
        """
        Reads a Playwright Python file, parses it, and returns an MMAT TestSuite.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=file_path)

        # Assume the file name (without extension) is the test suite name
        suite_name = file_path.split('/')[-1].replace('.py', '')
        self.test_suite = TestSuite(name=suite_name, test_cases=[])

        self.visit(node)

        self.test_suite.test_cases = self.test_cases

        # Construct the full test plan structure
        test_plan_dict = {
            "test_plan": {
                "name": f"Imported Test Plan for: {suite_name}",
                "description": f"Test plan imported from Playwright script: {file_path}",
                "test_suites": [
                    self.test_suite.to_dict() # Convert the TestSuite object to dictionary
                ]
            }
        }
        return test_plan_dict

    def visit_FunctionDef(self, node):
        """Visit function definitions - potentially new test cases."""
        if node.name.startswith('test_'): # Simple heuristic for test functions
             print(f"Found potential test case function: {node.name}")
             # Extract description from comments or docstrings if available
             description = ast.get_docstring(node)
             self.current_test_case = TestCase(name=node.name, description=description, steps=[])
             self.generic_visit(node) # Visit nodes within the function
             if self.current_test_case and self.current_test_case.steps:
                 self.test_cases.append(self.current_test_case)
             self.current_test_case = None # Reset for next function
        else:
            self.generic_visit(node) # Continue visiting other nodes

    def visit_Call(self, node):
        """Visit function calls - potentially test steps."""
        if self.current_test_case:
            step_action = None
            step_parameters: Dict[str, Any] = {}
            step_description = None

            # Handle calls like page.goto, page.fill, page.click
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == 'page':
                method_name = node.func.attr
                pos_args, kw_args = self._parse_call_arguments(node.args, node.keywords)

                if method_name == 'goto':
                    step_action = 'navigate'
                    if pos_args:
                        step_parameters['url'] = pos_args[0]
                    step_description = f"Go to URL: {step_parameters.get('url', '')}"
                elif method_name == 'fill':
                    step_action = 'fill'
                    if pos_args:
                        step_parameters['selector'] = pos_args[0]
                        if len(pos_args) > 1:
                            step_parameters['text'] = pos_args[1] # Playwright fill takes selector, value
                    step_parameters.update(kw_args) # Add any keyword args
                    step_description = f"Fill '{step_parameters.get('selector', '')}' with '{step_parameters.get('text', '')}'"
                elif method_name == 'click':
                    step_action = 'click'
                    if pos_args:
                        step_parameters['selector'] = pos_args[0]
                    step_parameters.update(kw_args)
                    step_description = f"Click '{step_parameters.get('selector', '')}'"
                # Add more page actions as needed

            # Handle expect(locator).to_be_visible() pattern
            elif isinstance(node.func, ast.Attribute) and node.func.attr == 'to_be_visible':
                # Check if the value of to_be_visible is an expect call
                if isinstance(node.func.value, ast.Call) and \
                   isinstance(node.func.value.func, ast.Name) and node.func.value.func.id == 'expect':
                    
                    # Get the argument of the expect call, which should be the locator call
                    if node.func.value.args and isinstance(node.func.value.args[0], ast.Call):
                        locator_call = node.func.value.args[0]
                        if isinstance(locator_call.func, ast.Attribute) and \
                           isinstance(locator_call.func.value, ast.Name) and locator_call.func.value.id == 'page' and \
                           locator_call.func.attr == 'locator':
                            
                            locator_pos_args, locator_kw_args = self._parse_call_arguments(locator_call.args, locator_call.keywords)
                            
                            step_action = 'assert_element_visible'
                            if locator_pos_args:
                                step_parameters['selector'] = locator_pos_args[0]
                            step_parameters.update(locator_kw_args)
                            step_description = f"Assert element '{step_parameters.get('selector', '')}' is visible"
                # Add more expect assertions as needed (e.g., to_have_url)
            elif isinstance(node.func, ast.Attribute) and node.func.attr == 'to_have_url':
                if isinstance(node.func.value, ast.Name) and node.func.value.id == 'page':
                    pos_args, kw_args = self._parse_call_arguments(node.args, node.keywords)
                    step_action = 'assert_url'
                    if pos_args:
                        step_parameters['expected'] = pos_args[0]
                    step_parameters.update(kw_args)
                    step_description = f"Assert URL is '{step_parameters.get('expected', '')}'"


            if step_action:
                step = TestStep(
                    action=step_action,
                    # MMAT TestStep uses 'args' for parameters, not 'target' directly for selectors
                    # The 'target' field is more for visual targets or complex objects.
                    # For Playwright selectors, they are part of 'parameters' (which maps to 'args' in TestStep)
                    args=step_parameters,
                    description=step_description
                )
                self.current_test_case.add_step(step)

        self.generic_visit(node) # Continue visiting arguments and other parts of the call

    def _parse_call_arguments(self, args: List[ast.expr], keywords: List[ast.keyword]) -> (List[Any], Dict[str, Any]):
        """
        Parses AST call arguments and keywords into a list of positional arguments
        and a dictionary of keyword arguments.
        """
        parsed_pos_args: List[Any] = []
        parsed_kw_args: Dict[str, Any] = {}

        # Parse positional arguments
        for arg in args:
            try:
                # Using literal_eval is safer for simple constants (strings, numbers, booleans, None)
                value = ast.literal_eval(arg)
                parsed_pos_args.append(value)
            except (ValueError, SyntaxError):
                # If not a literal, try to get the ID for Name nodes (variables)
                if isinstance(arg, ast.Name):
                    parsed_pos_args.append(arg.id)
                else:
                    # Fallback for other complex expressions
                    parsed_pos_args.append(f"<{ast.dump(arg)}>") # Placeholder representation

        # Parse keyword arguments
        for keyword in keywords:
            if keyword.arg: # Ensure argument name exists
                try:
                    value = ast.literal_eval(keyword.value)
                    parsed_kw_args[keyword.arg] = value
                except (ValueError, SyntaxError):
                    if isinstance(keyword.value, ast.Name):
                        parsed_kw_args[keyword.arg] = keyword.value.id
                    else:
                        parsed_kw_args[keyword.arg] = f"<{ast.dump(keyword.value)}>"

        return parsed_pos_args, parsed_kw_args
