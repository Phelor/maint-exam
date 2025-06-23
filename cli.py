"""argparse, CLI lib"""
import argparse
from manager import TaskManager
from storage import JsonStorageBackend

def launch_cli():
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
        task = manager.add_task(args.description)
        print(f"Added task {task.id}: {task.description}")
    elif action == "remove":
        success = manager.remove_task(args.id)
        if success:
            print(f"Removed task {args.id}.")
        else:
            print(f"Task {args.id} not found.")
    elif action == "list":
        tasks = manager.list_tasks()
        for task in tasks:
            print(f"{task.id}: {task.description}")
    elif action == "find":
        matches = manager.find_tasks(args.keyword)
        for task in matches:
            print(f"{task.id}: {task.description}")
