from .base_step import TestStep
from .web_steps import NavigateStep, ClickStep, FillStep

# You can import other step types here as they are created

STEP_TYPES = {
    "navigate": NavigateStep,
    "click": ClickStep,
    "fill": FillStep,
    # Add other step types here
}

def create_step(step_data, driver):
    """
    Factory function to create a test step instance based on its type.

    Args:
        step_data (dict): Dictionary containing the step's configuration data.
        driver: The driver instance to pass to the step.

    Returns:
        TestStep: An instance of the appropriate TestStep subclass, or None if the type is unknown.
    """
    step_type = step_data.get("type")
    if step_type in STEP_TYPES:
        return STEP_TYPES[step_type](step_data, driver)
    else:
        print(f"[TestSteps] Warning: Unknown step type: {step_type}")
        return None
