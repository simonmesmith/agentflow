import json
import os

import pytest

from agentflow.flow import Flow


@pytest.fixture
def flow_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    flows_dir = os.path.join(root_dir, "agentflow", "agentflow", "flows")
    return os.path.join(flows_dir, "test.json")


def test_flow_no_variables(flow_path):
    data = {
        "system_message": "Test system message.",
        "tasks": [
            {"action": "Test action 1"},
            {"action": "Test action 2"},
        ],
    }

    with open(flow_path, "w") as f:
        json.dump(data, f)

    flow = Flow("test")
    assert flow.system_message == data["system_message"]
    assert all(
        task.action == data["tasks"][i]["action"] for i, task in enumerate(flow.tasks)
    )

    os.remove(flow_path)


def test_flow_with_variables_correct_values(flow_path):
    data = {
        "system_message": "Test system message with {variable}.",
        "tasks": [
            {"action": "Test action 1 with {variable}"},
            {"action": "Test action 2"},
        ],
    }

    with open(flow_path, "w") as f:
        json.dump(data, f)

    flow = Flow("test", {"variable": "value"})
    assert flow.system_message == data["system_message"].format(variable="value")
    assert flow.tasks[0].action == data["tasks"][0]["action"].format(variable="value")
    assert flow.tasks[1].action == data["tasks"][1]["action"]

    os.remove(flow_path)


def test_flow_with_variables_extra_values(flow_path):
    data = {
        "system_message": "Test system message.",
        "tasks": [
            {"action": "Test action 1"},
            {"action": "Test action 2"},
        ],
    }

    with open(flow_path, "w") as f:
        json.dump(data, f)

    with pytest.raises(ValueError, match="Extra variables provided"):
        _ = Flow("test", {"variable": "value"})

    os.remove(flow_path)


def test_flow_with_variables_missing_values(flow_path):
    data = {
        "system_message": "Test system message with {variable}.",
        "tasks": [
            {"action": "Test action 1 with {variable}"},
            {"action": "Test action 2"},
        ],
    }

    with open(flow_path, "w") as f:
        json.dump(data, f)

    with pytest.raises(ValueError, match="Missing variable values for"):
        _ = Flow("test")

    os.remove(flow_path)


def test_flow_with_escaped_curly_braces(flow_path):
    data = {
        "system_message": "Test system message with {{escaped}} braces.",
        "tasks": [
            {"action": "Test action 1 with {{escaped}} braces"},
            {"action": "Test action 2"},
        ],
    }

    with open(flow_path, "w") as f:
        json.dump(data, f)

    flow = Flow("test")
    assert flow.system_message == data["system_message"].replace("{{", "{").replace(
        "}}", "}"
    )
    assert flow.tasks[0].action == data["tasks"][0]["action"].replace(
        "{{", "{"
    ).replace("}}", "}")
    assert flow.tasks[1].action == data["tasks"][1]["action"]

    os.remove(flow_path)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        _ = Flow("file_not_found")
