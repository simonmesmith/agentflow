import json
import os

from flow import Flow


def test_flow():
    name = "test"
    data = {
        "system_message": "Test system message.",
        "tasks": [
            {
                "action": "Test action 1",
                "settings": {
                    "model": "gpt-4",
                    "function_call": "test_function_call_1",
                    "temperature": 0.5,
                },
            },
            {
                "action": "Test action 2",
            },
        ],
    }
    path = os.path.join(os.path.dirname(__file__), "flows", f"{name}.json")
    json.dump(data, open(path, "w"))
    flow = Flow(name)
    assert flow.name == name
    assert flow.system_message == data["system_message"]
    assert len(flow.tasks) == len(data["tasks"])
    for i, task in enumerate(flow.tasks):
        assert task.action == data["tasks"][i]["action"]
        if "settings" in data["tasks"][i]:
            assert task.settings.model == data["tasks"][i]["settings"]["model"]
            assert (
                task.settings.function_call
                == data["tasks"][i]["settings"]["function_call"]
            )
            assert (
                task.settings.temperature == data["tasks"][i]["settings"]["temperature"]
            )
    os.remove(path)


def test_file_not_found():
    try:
        _ = Flow("file_not_found")
    except FileNotFoundError:
        assert True
    else:
        assert False
