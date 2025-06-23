import sys
import json

TASK_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        """Initialize the TaskManager and load existing tasks from file."""
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file into memory."""
        try:
            with open(TASK_FILE, "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        """Save current tasks to the JSON file."""
        with open(TASK_FILE, "w") as f:
            json.dump(self.tasks, f)

    def add_task(self, description):
        """Add a new task with the given description."""
        task = {"id": len(self.tasks) + 1, "description": description}
        self.tasks.append(task)
        self.save_tasks()
        return task

    def remove_task(self, task_id):
        """Remove the task with the specified ID."""
        for idx, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(task_id)
                self.save_tasks()
                return True
        return False

    def list_tasks(self):
        """Return the list of all tasks."""
        return self.tasks

    def find_tasks(self, keyword):
        """Find all tasks containing the keyword in their description."""
        result = []
        for task in self.tasks:
            if keyword.lower() in task["description"].lower():
                result.append(task)
        return result


def main():
    """Main entry point for the task CLI application."""
    manager = TaskManager()
    if len(sys.argv) < 2:
        print("Usage: python sample_app.py [add|remove|list|find] [args]")
        return

    action = sys.argv[1]
    if action == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description.")
            return
        task = manager.add_task(sys.argv[2])
        print(f"Added task {task['id']}: {task['description']}")
    elif action == "remove":
        if len(sys.argv) < 3:
            print("Please provide the task ID to remove.")
            return
        try:
            tid = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID.")
            return
        success = manager.remove_task(tid)
        if success:
            print(f"Removed task {tid}.")
        else:
            print(f"Task {tid} not found.")
    elif action == "list":
        tasks = manager.list_tasks()
        for task in tasks:
            print(f"{task['id']}: {task['description']}")
    elif action == "find":
        if len(sys.argv) < 3:
            print("Please provide a keyword to search.")
            return
        matches = manager.find_tasks(sys.argv[2])
        for task in matches:
            print(f"{task['id']}: {task['description']}")
    else:
        print("Unknown action.")


if __name__ == "__main__":
    main()
