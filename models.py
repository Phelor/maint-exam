from typing import Dict, Any

class Task:
    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "description": self.description}

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(id=data["id"], description=data["description"])
