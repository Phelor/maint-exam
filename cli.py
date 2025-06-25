"""argparse, CLI lib"""
import argparse
from manager import TaskManager
from storage import JsonStorageBackend

def launch_cli():
    """Main entry point for the task CLI application."""
    storage = JsonStorageBackend("tasks.json")
    manager = TaskManager(storage)

    args = parse_args()
    handle_command(args, manager)

def parse_args():
    """Parsing argument chain"""
    parser = argparse.ArgumentParser(description="Task manager de fou là")
    subparsers = parser.add_subparsers(dest="command", required=True)

    (subparsers
     .add_parser("add", help="Add new task")
     .add_argument("description", type=str, help="Task description")
    )
    (subparsers
     .add_parser("remove", help="Remove a task by ID")
     .add_argument("id", type=int, help="Task ID")
    )
    (subparsers
     .add_parser("list", help="List all tasks")
    )
    (subparsers
     .add_parser("find", help="Find tasks by keyword")
     .add_argument("keyword", type=str, help="Keyword")
    )

    return parser.parse_args()

def handle_command(args, manager: TaskManager):
    """list of CLI command"""
    if args.command == "add":
        task = manager.add_task(args.description)
        print(f"Added task {task.id}: {task.description}")
    elif args.command == "remove":
        success = manager.remove_task(args.id)
        print(f"Removed task {args.id}." if success else f"Task {args.id} not found.")
    elif args.command == "list":
        for task in manager.list_tasks():
            print(f"{task.id}: {task.description}")
    elif args.command == "find":
        found = manager.find_tasks(args.keyword)
        if not found:
            print("Aucune tâche")
        else:
            for task in found:
                print(f"{task.id}: {task.description}")
