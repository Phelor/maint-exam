import os
import pytest
import sys
from cli import launch_cli
from storage import JsonStorageBackend
from models import Task

@pytest.fixture
def test_manager():
    class Test_Task:
        def __init__(self, id, description):
            self.id = id
            self.description = description

    class Test_Manager:
        def __init__(self):
            self.tasks = [
                Test_Task(1, "foo"),
                Test_Task(2, "toto"),
                Test_Task(3, "tota"),
            ]
        def add_task(self, description):
            return Test_Task(12,description)
        def remove_task(self, task_id):
            return task_id == 1
        def list_tasks(self):
            return self.tasks
        def find_tasks(self, keyword):
            return [t for t in self.tasks if keyword in t.description]
    return Test_Manager()

# CLI test 
def run_cli_with_args(args, monkeypatch, mocker, test_manager):
    monkeypatch.setattr(sys, "argv", ["prog"] + args)
    mocker.patch("cli.TaskManager", return_value=test_manager)
    mocker.patch("cli.JsonStorageBackend")
    outputs = []
    monkeypatch.setattr("builtins.print", outputs.append)
    launch_cli()
    return outputs

def test_cli_add(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["add", "nouvelle tâche"], monkeypatch, mocker, test_manager)
    assert any("Added task" in str(o) for o in outputs)

def test_cli_remove_success(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["remove", "1"], monkeypatch, mocker, test_manager)
    assert any("Removed task 1." in str(o) for o in outputs)

def test_cli_remove_fail(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["remove", "12"], monkeypatch, mocker, test_manager)
    assert any("not found" in str(o) for o in outputs)

def test_cli_list(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["list"], monkeypatch, mocker, test_manager)
    assert any("foo" in str(o) for o in outputs)
    assert any("toto" in str(o) for o in outputs)

def test_cli_find(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["find", "to"], monkeypatch, mocker, test_manager)
    assert any("toto" in str(o) for o in outputs)
    assert any("tota" in str(o) for o in outputs)

def test_cli_find_inexistant(monkeypatch, mocker, test_manager):
    outputs = run_cli_with_args(["find", "alo"], monkeypatch, mocker, test_manager)
    assert any("Aucune tâche" in str(o) for o in outputs)

def test_cli_misspelling(monkeypatch, mocker, test_manager):
    try:
        run_cli_with_args(["found","to"], monkeypatch, mocker, test_manager)
        assert False, "La commande invalide àn'as pas provoqué d'erreur"
    except SystemExit as error:
        assert error.code !=0

# Test non CLI
def test_json_writting(tmp_path):
    json_file = tmp_path / "test_tasks.json"
    backend = JsonStorageBackend(str(json_file))
    tasks = [Task(id=1, description="tortue1"), Task(id=2, description="tortue2")]

    backend.save_tasks(tasks)
    loaded = backend.load_tasks()

    assert len(loaded) == 2
    assert loaded[0].description == "tortue1"
    assert loaded[1].id == 2
    assert os.path.exists(json_file)

def test_json_corrupted(tmp_path):
    json_file = tmp_path / "corrupted.json"
    json_file.write_text("{larry: larry a corrompu ce fichier")
    backend = JsonStorageBackend(str(json_file))
    tasks = backend.load_tasks()
    assert not tasks
