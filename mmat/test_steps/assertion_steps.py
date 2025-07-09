from .base_step import TestStep

class AssertUrlStep(TestStep):
    """
    Test step to assert the current URL matches an expected URL.
    """
    def __init__(self, step_data, driver):
        super().__init__(step_data, driver)
        self.expected_url = step_data.get("expected")
        if not self.expected_url:
            print(f"[AssertUrlStep] Error: 'expected' URL is required for AssertUrlStep.")

    def execute(self):
        """
        Executes the URL assertion step.
        """
        if not self.expected_url:
            print("[AssertUrlStep] Execution failed: 'expected' URL not provided.")
            return False
        print(f"[AssertUrlStep] Executing: {self.description}")
        try:
            current_url = self.driver.get_current_url() # Assuming driver has this method
            if self.expected_url in current_url: # Simple check, can be enhanced with regex or full match
                print(f"[AssertUrlStep] Assertion successful: Current URL '{current_url}' contains expected '{self.expected_url}'.")
                return True
            else:
                print(f"[AssertUrlStep] Assertion failed: Current URL '{current_url}' does not contain expected '{self.expected_url}'.")
                return False
        except Exception as e:
            print(f"[AssertUrlStep] Execution failed: {e}")
            return False

class AssertElementVisibleStep(TestStep):
    """
    Test step to assert an element is visible on the page.
    """
    def __init__(self, step_data, driver):
        super().__init__(step_data, driver)
        self.selector = step_data.get("selector")
        if not self.selector:
            print(f"[AssertElementVisibleStep] Error: 'selector' is required for AssertElementVisibleStep.")

    def execute(self):
        """
        Executes the element visibility assertion step.
        """
        if not self.selector:
            print("[AssertElementVisibleStep] Execution failed: 'selector' not provided.")
            return False
        print(f"[AssertElementVisibleStep] Executing: {self.description}")
        try:
            is_visible = self.driver.is_element_visible(self.selector) # Assuming driver has this method
            if is_visible:
                print(f"[AssertElementVisibleStep] Assertion successful: Element with selector '{self.selector}' is visible.")
                return True
            else:
                print(f"[AssertElementVisibleStep] Assertion failed: Element with selector '{self.selector}' is not visible.")
                return False
        except Exception as e:
            print(f"[AssertElementVisibleStep] Execution failed: {e}")
            return False
