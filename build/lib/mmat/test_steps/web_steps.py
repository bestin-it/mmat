from .base_step import TestStep

class NavigateStep(TestStep):
    """
    Test step to navigate to a specified URL.
    """
    def __init__(self, step_data, driver):
        super().__init__(step_data, driver)
        self.url = step_data.get("url")
        if not self.url:
            print(f"[NavigateStep] Error: 'url' is required for NavigateStep.")

    def execute(self):
        """
        Executes the navigation step.
        """
        if not self.url:
            print("[NavigateStep] Execution failed: 'url' not provided.")
            return False
        print(f"[NavigateStep] Executing: {self.description}")
        try:
            self.driver.navigate(self.url)
            return True
        except Exception as e:
            print(f"[NavigateStep] Execution failed: {e}")
            return False

class ClickStep(TestStep):
    """
    Test step to click an element using a CSS selector.
    """
    def __init__(self, step_data, driver):
        super().__init__(step_data, driver)
        self.selector = step_data.get("selector")
        if not self.selector:
            print(f"[ClickStep] Error: 'selector' is required for ClickStep.")

    def execute(self):
        """
        Executes the click step.
        """
        if not self.selector:
            print("[ClickStep] Execution failed: 'selector' not provided.")
            return False
        print(f"[ClickStep] Executing: {self.description}")
        try:
            self.driver.click(self.selector)
            return True
        except Exception as e:
            print(f"[ClickStep] Execution failed: {e}")
            return False

class FillStep(TestStep):
    """
    Test step to fill an input field using a CSS selector and a value.
    """
    def __init__(self, step_data, driver):
        super().__init__(step_data, driver)
        self.selector = step_data.get("selector")
        self.value = step_data.get("value")
        if not self.selector or self.value is None:
             print(f"[FillStep] Error: 'selector' and 'value' are required for FillStep.")


    def execute(self):
        """
        Executes the fill step.
        """
        if not self.selector or self.value is None:
            print("[FillStep] Execution failed: 'selector' or 'value' not provided.")
            return False
        print(f"[FillStep] Executing: {self.description}")
        try:
            self.driver.fill(self.selector, self.value)
            return True
        except Exception as e:
            print(f"[FillStep] Execution failed: {e}")
            return False

# Add other web-specific test steps here (e.g., ScreenshotStep, SelectStep, HoverStep, etc.)
