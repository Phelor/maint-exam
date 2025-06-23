import sys
import argparse
from manager import TaskManager 
from storage import JsonStorageBackend

def main():
    """Main entry point for the task CLI application."""
    storage = JsonStorageBackend("tasks.json")
    manager = TaskManager(storage)

    parser = argparse.ArgumentParser(description="Task manager de fou là")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="Add new task")
    parser_add.add_argument("description", type=str, help="Task description")

    parser_remove = subparsers.add_parser("remove", help="Remove a task by ID")
    parser_remove.add_argument("id", type=int, help="Task ID")

    parser_list = subparsers.add_parser("list", help="List all tasks")

    parser_find = subparsers.add_parser("find", help="Find tasks by id")
    parser_find.add_argument("keyword", type=str, help="id to search")

    args = parser.parse_args()

    # if len(sys.argv) < 2:
    #     print("Usage: python sample_app.py [add|remove|list|find] [args]")
    #     return

    action = args.command

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
