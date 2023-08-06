"""
This module contains tests for the Flow class.
"""

import os
from types import SimpleNamespace
from typing import Dict, List, Optional
from unittest.mock import patch

import pytest

from agentflow.flow import Flow
from agentflow.llm import Settings


def mock_llm_respond(
    settings: Settings,
    messages: List[Dict[str, str]],
    functions: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """
    This function is used as a dynamic response function for testing purposes.
    :param settings: The settings for the interaction.
    :type settings: Settings
    :param messages: The messages to be processed by the mocked language model.
    :type messages: List[Dict[str, str]]
    :param functions: The functions to be processed by the mocked language model.
    :type functions: Optional[List[Dict[str, str]]]
    """
    last_message_content = messages[-1]["content"]
    return SimpleNamespace(
        role="assistant", content=f"Response to {last_message_content}"
    )


@pytest.fixture
def flows_path():
    """
    Fixture that returns the path to the test flows folder.
    """
    return os.path.dirname(os.path.abspath(__file__))


def test_file_not_found(flows_path):
    """
    Tests the initialization of the Flow object with a nonexistent flow file.
    """
    with pytest.raises(FileNotFoundError):
        _ = Flow("file_not_found", flows_path=flows_path)


def test_flow_basic(flows_path):
    """
    Tests the initialization and running of a Flow object with a basic flow file.
    """

    # Load the flow
    flow = Flow("test_flow_basic", flows_path=flows_path)

    # Ensure we're loading the system message and all tasks
    assert flow.system_message == "Test system message.", "System message is incorrect."
    assert len(flow.tasks) == 3, "Number of tasks is incorrect."

    # Ensure we're loading the correct settings for each task
    default_settings = Settings()
    assert flow.tasks[0].settings == default_settings, "Settings are incorrect."

    # Test running the flow
    with patch("agentflow.flow.LLM") as MockLLM:
        mock_llm = MockLLM.return_value
        mock_llm.respond.side_effect = mock_llm_respond
        flow.run()

        # Ensure we're poperly instantiating the LLM and calling the respond method
        assert MockLLM.call_count == 1, "LLM was not instantiated exactly once."
        assert mock_llm.respond.call_count > 0, "The respond method was not called."

        # Ensure we're passing the correct messages to the LLM
        last_call = mock_llm.respond.call_args
        last_messages = last_call[0][1]
        assert (
            last_messages[-1]["content"]
            == f"Response to {last_messages[-2]['content']}"
        ), "The LLM respond method is not working as intended."


# def test_flow_no_variables(flow_path):
#     """
#     Tests the initialization of the Flow object with no variables.
#     """
#     data = {
#         "system_message": "Test system message.",
#         "tasks": [
#             {"action": "Test action 1"},
#             {"action": "Test action 2"},
#         ],
#     }

#     with open(flow_path, "w") as f:
#         json.dump(data, f)

#     flow = Flow("test")
#     assert flow.system_message == data["system_message"]
#     assert all(
#         task.action == data["tasks"][i]["action"] for i, task in enumerate(flow.tasks)
#     )

#     os.remove(flow_path)


# def test_flow_with_variables_correct_values(flow_path):
#     """
#     Tests the initialization of the Flow object with correct variable values.
#     """
#     data = {
#         "system_message": "Test system message with {variable}.",
#         "tasks": [
#             {"action": "Test action 1 with {variable}"},
#             {"action": "Test action 2"},
#         ],
#     }

#     with open(flow_path, "w") as f:
#         json.dump(data, f)

#     flow = Flow("test", {"variable": "value"})
#     assert flow.system_message == data["system_message"].format(variable="value")
#     assert flow.tasks[0].action == data["tasks"][0]["action"].format(variable="value")
#     assert flow.tasks[1].action == data["tasks"][1]["action"]

#     os.remove(flow_path)


# def test_flow_with_variables_extra_values(flow_path):
#     """
#     Tests the initialization of the Flow object with extra variable values.
#     """
#     data = {
#         "system_message": "Test system message.",
#         "tasks": [
#             {"action": "Test action 1"},
#             {"action": "Test action 2"},
#         ],
#     }

#     with open(flow_path, "w") as f:
#         json.dump(data, f)

#     with pytest.raises(ValueError, match="Extra variables provided"):
#         _ = Flow("test", {"variable": "value"})

#     os.remove(flow_path)


# def test_flow_with_variables_missing_values(flow_path):
#     """
#     Tests the initialization of the Flow object with missing variable values.
#     """
#     data = {
#         "system_message": "Test system message with {variable}.",
#         "tasks": [
#             {"action": "Test action 1 with {variable}"},
#             {"action": "Test action 2"},
#         ],
#     }

#     with open(flow_path, "w") as f:
#         json.dump(data, f)

#     with pytest.raises(ValueError, match="Missing variable values for"):
#         _ = Flow("test")

#     os.remove(flow_path)


# def test_flow_with_escaped_curly_braces(flow_path):
#     """
#     Tests the initialization of the Flow object with escaped curly braces in the system message and tasks.
#     """
#     data = {
#         "system_message": "Test system message with {{escaped}} braces.",
#         "tasks": [
#             {"action": "Test action 1 with {{escaped}} braces"},
#             {"action": "Test action 2"},
#         ],
#     }

#     with open(flow_path, "w") as f:
#         json.dump(data, f)

#     flow = Flow("test")
#     assert flow.system_message == data["system_message"].replace("{{", "{").replace(
#         "}}", "}"
#     )
#     assert flow.tasks[0].action == data["tasks"][0]["action"].replace(
#         "{{", "{"
#     ).replace("}}", "}")
#     assert flow.tasks[1].action == data["tasks"][1]["action"]

#     os.remove(flow_path)
