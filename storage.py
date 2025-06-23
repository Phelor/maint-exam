from typing import List, Protocol
import json

from models import Task

class StorageBackend(Protocol):
    def load_tasks(self) -> List[Task]:
        ...
    def save_tasks(self, tasks: List[Task]) -> None:
        ...

class JsonStorageBackend:
    def __init__(self, filename: str):
        self.filename = filename

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as f:
            try:
                data = json.load(f)
                return [Task.from_dict(t) for t in data]
            except Exception:
                return []

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2)