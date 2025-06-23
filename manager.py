from storage import StorageBackend
from models import Task
from storage import List

TASK_FILE = "tasks.json"

class TaskManager:
    def __init__(self, storage: StorageBackend):
        """Initialize the TaskManager and load existing tasks from file. StorageBackend load empty list or existing task.json"""
        self.storage = storage
        self.tasks = self.storage.load_tasks()

    def add_task(self, description: str) -> Task:
        """Add a new task with the given description."""
        new_id = max([t.id for t in self.tasks], default=0) + 1
        task = Task(id=new_id, description=description)
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task

    def remove_task(self, task_id):
        """Remove the task with the specified ID."""
        for idx, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[idx]
                self.storage.save_tasks(self.tasks)
                return True
        return False

    def list_tasks(self) -> List[Task]:
        """Return the list of all tasks."""
        return self.tasks

    def find_tasks(self, keyword: str) -> List[Task]:
        """Find all tasks containing the keyword in their description."""
        return [t for t in self.tasks if keyword.lower() in t.description.lower()]


