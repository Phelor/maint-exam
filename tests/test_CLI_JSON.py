import os
import pytest
import sys
from cli import launch_cli
from manager import TaskManager
from storage import JsonStorageBackend
from models import Task

@pytest.fixture
def test_manager():
    """
    Fake manager to test CLI without write in file
    """
    class TestTask:
        """
        Fake object structure for test
        """
        def __init__(self, id, description):
            self.id = id
            self.description = description

    class TestManager:
        """
        Fake task play roll + fake return function
        """
        def __init__(self):
            self.tasks = [
                TestTask(1, "foo"),
                TestTask(2, "toto"),
                TestTask(3, "tota"),
            ]
        def add_task(self, description):
            """CLI call this one instead of real manager"""
            return TestTask(12,description)
        def remove_task(self, task_id):
            """CLI call this one instead of real manager"""
            return task_id == 1
        def list_tasks(self):
            """CLI call this one instead of real manager"""
            return self.tasks
        def find_tasks(self, keyword):
            """CLI call this one instead of real manager"""
            return [t for t in self.tasks if keyword in t.description]
    return TestManager()

# CLI test
def run_cli_with_args(args, monkeypatch, mocker, test_manager):
    """CLI test have only for purpose to test CLI call make the good call"""
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    mocker.patch("cli.TaskManager", return_value=test_manager)
    mocker.patch("cli.JsonStorageBackend")
    outputs = []
    monkeypatch.setattr("builtins.print", outputs.append)
    launch_cli()
    return outputs

def test_cli_add(monkeypatch, mocker, test_manager):
    """test CLI add"""
    outputs = run_cli_with_args(["add", "nouvelle tâche"], monkeypatch, mocker, test_manager)
    assert any("Added task" in str(o) for o in outputs)

def test_cli_remove_success(monkeypatch, mocker, test_manager):
    """test CLI remove with sucess"""
    outputs = run_cli_with_args(["remove", "1"], monkeypatch, mocker, test_manager)
    assert any("Removed task 1." in str(o) for o in outputs)

def test_cli_remove_fail(monkeypatch, mocker, test_manager):
    """test CLI remove without sucess"""
    outputs = run_cli_with_args(["remove", "12"], monkeypatch, mocker, test_manager)
    assert any("not found" in str(o) for o in outputs)

def test_cli_list(monkeypatch, mocker, test_manager):
    """test CLI list Task"""
    outputs = run_cli_with_args(["list"], monkeypatch, mocker, test_manager)
    assert any("foo" in str(o) for o in outputs)
    assert any("toto" in str(o) for o in outputs)

def test_cli_find(monkeypatch, mocker, test_manager):
    """test CLI find existant"""
    outputs = run_cli_with_args(["find", "to"], monkeypatch, mocker, test_manager)
    assert any("toto" in str(o) for o in outputs)
    assert any("tota" in str(o) for o in outputs)

def test_cli_find_inexistant(monkeypatch, mocker, test_manager):
    """test CLI don't find inexistant"""
    outputs = run_cli_with_args(["find", "alo"], monkeypatch, mocker, test_manager)
    assert any("Aucune tâche" in str(o) for o in outputs)

def test_cli_misspelling(monkeypatch, mocker, test_manager):
    """test CLI miss spelling in call"""
    try:
        run_cli_with_args(["found","to"], monkeypatch, mocker, test_manager)
        assert False, "La commande invalide àn'as pas provoqué d'erreur"
    except SystemExit as error:
        assert error.code !=0

# Test non CLI
def test_json_manager(tmp_path):
    """test json writting and reading function with the manager"""
    json_file = tmp_path / "test_tasks.json"
    backend = JsonStorageBackend(str(json_file))

    manager = TaskManager(backend)
    manager.add_task("tortue1")
    manager.add_task("tortue2")
    manager.add_task("tortueMechante")
    manager.remove_task(3)

    loaded = manager.list_tasks()
    loaded_find = manager.find_tasks("2")

    assert len(loaded) == 2
    assert len(loaded_find) == 1
    assert loaded[0].description == "tortue1"
    assert loaded[0].task_id == 1
    assert loaded[1].task_id == 2
    assert os.path.exists(json_file)

def test_json_corrupted(tmp_path):
    """test if json is corrupted"""
    json_file = tmp_path / "corrupted.json"
    json_file.write_text("{larry: larry a corrompu ce fichier")
    backend = JsonStorageBackend(str(json_file))
    tasks = backend.load_tasks()
    assert not tasks
