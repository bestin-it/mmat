import uuid
from typing import Any, Dict, Optional, Union

class TestStep:
    """Represents a single step in a test case."""

    def __init__(
        self,
        action: str,
        target: Optional[Union[str, Dict[str, Any]]] = None,
        args: Optional[Dict[str, Any]] = None,
        expected_result: Optional[Any] = None,
        step_id: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        Initializes a TestStep.

        Args:
            action: The action to perform (e.g., 'click', 'fill', 'navigate').
            target: The target of the action (e.g., CSS selector, visual reference).
            args: Additional arguments for the action (e.g., {'value': 'test'}).
            expected_result: The expected outcome after performing the step.
            step_id: Unique identifier for the step. Generated if None.
            description: Human-readable description of the step.
        """
        self.step_id = step_id if step_id is not None else str(uuid.uuid4())
        self.action = action
        self.target = target
        self.args = args if args is not None else {}
        self.expected_result = expected_result
        self.description = description
        self.status: Optional[str] = None # 'pending', 'running', 'passed', 'failed', 'skipped'
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TestStep to a dictionary."""
        return {
            "step_id": self.step_id,
            "action": self.action,
            "target": self.target,
            "args": self.args,
            "expected_result": self.expected_result,
            "description": self.description,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestStep":
        """Creates a TestStep from a dictionary."""
        return cls(
            step_id=data.get("step_id"),
            action=data["action"],
            target=data.get("target"),
            args=data.get("args"),
            expected_result=data.get("expected_result"),
            description=data.get("description"),
        )

    def __repr__(self) -> str:
        return f"TestStep(action='{self.action}', target={self.target}, description='{self.description}')"
