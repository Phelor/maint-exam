"""
Models for the task, it's a structured data object
"""
from typing import Dict, Any

class Task:
    """
    Attributes:
        id (int): Unique identifier for the task.
        description (str): Text description of the task    
    """
    def __init__(self, task_id: int, description: str):
        self.task_id = task_id
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """data into dic"""
        return {"id": self.task_id, "description": self.description}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        """dic into task"""
        return Task(task_id=data["task_id"], description=data["description"])
