# mmat/models/model.py

class Model:
    """
    Base class for different types of models used in the framework.
    Defines the interface for model interactions.
    """
    def process(self, data):
        """
        Processes the input data using the model.
        """
        # Placeholder for model processing logic
        pass

# Specific model implementations will inherit from this base class
# e.g., ReasoningModel, VisionModel
