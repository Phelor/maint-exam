import sys
from manager import TaskManager 
from storage import JsonStorageBackend

def main():
    """Main entry point for the task CLI application."""
    storage = JsonStorageBackend("tasks.json")
    manager = TaskManager(storage)
    if len(sys.argv) < 2:
        print("Usage: python sample_app.py [add|remove|list|find] [args]")
        return

    action = sys.argv[1]
    if action == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description.")
            return
        task = manager.add_task(sys.argv[2])
        print(f"Added task {task.id}: {task.description}")
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
            print(f"{task.id}: {task.description}")
    elif action == "find":
        if len(sys.argv) < 3:
            print("Please provide a keyword to search.")
            return
        matches = manager.find_tasks(sys.argv[2])
        for task in matches:
            print(f"{task.id}: {task.description}")
    else:
        print("Unknown action.")


if __name__ == "__main__":
    main()
