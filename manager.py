"""
Manager it's like a controller for Task Control. 
Working logical separated from interface and data structure
"""
from storage import StorageBackend, List
from models import Task

TASK_FILE = "tasks.json"

class TaskManager:
    """
    Main function : 
        add_task(description)      -- Add new task
        remove_task(task_id)       -- Delete Task with id
        list_tasks()               -- return List of task
        find_tasks(keyword)        -- Find task with keyword
    """
    def __init__(self, storage: StorageBackend):
        """
        Initialize the TaskManager and load existing tasks from file. 
        StorageBackend load empty list or existing task.json
        """
        self.storage = storage
        self.tasks = self.storage.load_tasks()

    def add_task(self, description: str) -> Task:
        """Add a new task with the given description."""
        new_id = max((t.task_id for t in self.tasks), default=0) + 1
        new_task = Task(task_id=new_id, description=description)
        new_tasks = [*self.tasks, new_task]
        self._update_tasks(new_tasks)
        return new_task

    def remove_task(self, task_id: int) -> bool:
        """Remove the task with the specified ID."""
        new_tasks = [t for t in self.tasks if t.task_id != task_id]
        if len(new_tasks) < len(self.tasks):
            self._update_tasks(new_tasks)
            return True
        return False

    def _update_tasks(self, new_tasks: List[Task]) -> None:
        self.tasks = new_tasks
        self.storage.save_tasks(self.tasks)

    def list_tasks(self) -> List[Task]:
        """Return the list of all tasks."""
        return self.tasks[:]

    def find_tasks(self, keyword: str) -> List[Task]:
        """Find all tasks containing the keyword in their description."""
        return list(filter(lambda t: keyword.lower() in t.description.lower(), self.tasks))
