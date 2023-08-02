import json
import os

from flow_manager import Flow


def test_load():
    name = "test"
    data = {
        "tasks": [
            {"action": "Test action", "function": "test_function"},
        ]
    }
    path = os.path.join(os.path.dirname(__file__), "flows", f"{name}.json")
    json.dump(data, open(path, "w"))
    flow = Flow("test")
    assert flow == data
    os.remove(path)


def test_load_file_not_found():
    try:
        flow = Flow("test_missing")
    except FileNotFoundError:
        assert True
    else:
        assert False
