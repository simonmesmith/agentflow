"""
This module defines the Flow and Task classes which are used to load and execute a series of tasks defined in a JSON file.
Each task is processed by the LLM (Large Language Model) and the results are saved in a JSON file.
"""

import json
import os
import re

from agentflow.function import Function
from agentflow.llm import LLM, Settings
from agentflow.output import Output


class Task:
    """
    Represents a task to be processed by the LLM.

    :param action: The action to be performed by the task.
    :type action: str
    :param settings: Settings for the task. Defaults to an empty Settings object.
    :type settings: Settings, optional
    """

    def __init__(self, action: str, settings: Settings = None):
        self.action = action
        self.settings = settings if settings else Settings()


class Flow:
    """
    Represents a flow of tasks loaded from a JSON file.

    :param name: The name of the flow.
    :type name: str
    :param variables: Variables to be used in the flow. Defaults to an empty dictionary.
    :type variables: dict, optional
    """

    def __init__(self, name: str, variables: dict = None):
        self.name = name
        self._load_flow(name)
        self._validate_and_format_messages(variables or {})

    def _load_flow(self, name: str) -> None:
        """
        Load flow from a JSON file.

        :param name: The name of the flow.
        :type name: str
        :raises FileNotFoundError: If the JSON file does not exist.
        """
        base_path = os.path.join(os.path.dirname(__file__), "flows")
        file_path = f"{base_path}/{name}.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}.")

        with open(file_path, "r") as file:
            data = json.load(file)

        self.system_message = data.get("system_message")
        self.tasks = [
            Task(task["action"], Settings(**task.get("settings", {})))
            for task in data.get("tasks", [])
        ]

    def _validate_and_format_messages(self, variables: dict) -> None:
        """
        Validate and format messages with provided variables.

        :param variables: Variables to be used in the flow.
        :type variables: dict
        :raises ValueError: If there are extra or missing variables.
        """
        all_messages = [self.system_message] + [task.action for task in self.tasks]
        all_variables = set(
            match.group(1)
            for message in all_messages
            if message
            for match in re.finditer(
                r"{([^{}]+)}", message.replace("{{", "").replace("}}", "")
            )
        )

        extra_variables = set(variables.keys()) - all_variables
        if extra_variables:
            raise ValueError(f"Extra variables provided: {extra_variables}")

        missing_variables = all_variables - set(variables.keys())
        if missing_variables:
            raise ValueError(f"Missing variable values for: {missing_variables}")

        self._format_messages(variables)

    def _format_messages(self, variables: dict) -> None:
        """
        Format messages with provided variables.

        :param variables: Variables to be used in the flow.
        :type variables: dict
        """
        if self.system_message:
            self.system_message = self._format_message(self.system_message, variables)
        for task in self.tasks:
            if task.action:
                task.action = self._format_message(task.action, variables)

    @staticmethod
    def _format_message(message: str, variables: dict) -> str:
        """
        Format a single message with provided variables.

        :param message: The message to be formatted.
        :type message: str
        :param variables: Variables to be used in the flow.
        :type variables: dict
        :return: The formatted message.
        :rtype: str
        """
        return message.format(**variables).replace("{{", "{").replace("}}", "}")

    def run(self):
        """
        Run the flow.

        The flow is processed by the LLM and the results are saved in a JSON file.
        """
        llm = LLM()
        output = Output(self.name)
        messages = self._get_initial_messages()
        functions = self._get_functions(output)

        for task in self.tasks:
            self._process_task(task, llm, messages, functions, output)

        output.save("messages.json", messages)
        print(f"Find outputs at {output.output_path}")

    def _get_initial_messages(self) -> list:
        """
        Get initial system and user messages.

        :return: A list of initial messages.
        :rtype: list
        """
        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        return messages

    def _get_functions(self, output: Output) -> list:
        """
        Get function definitions for tasks with function calls.

        :param output: The output object.
        :type output: Output
        :return: A list of function definitions.
        :rtype: list
        """
        return [
            Function(task.settings.function_call, output).definition
            for task in self.tasks
            if task.settings.function_call is not None
        ]

    def _process_task(
        self, task: Task, llm: LLM, messages: list, functions: list, output: Output
    ):
        """
        Process a single task.

        :param task: The task to be processed.
        :type task: Task
        :param llm: The LLM object.
        :type llm: LLM
        :param messages: A list of messages.
        :type messages: list
        :param functions: A list of function definitions.
        :type functions: list
        :param output: The output object.
        :type output: Output
        """
        print("Flow:", task.action)
        print("Function:", task.settings.function_call)
        messages.append({"role": "user", "content": task.action})

        task.settings.function_call = (
            "none"
            if task.settings.function_call is None
            else {"name": task.settings.function_call}
        )

        message = llm.respond(task.settings, messages, functions)

        if message.content:
            self._process_message(message, messages)
        elif message.function_call:
            self._process_function_call(message, task, llm, messages, functions, output)

    @staticmethod
    def _process_message(message, messages: list) -> None:
        """
        Process a message from the assistant.

        :param message: The message from the assistant.
        :type message: Message
        :param messages: A list of messages.
        :type messages: list
        """
        print("Assistant: ", message.content)
        messages.append({"role": "assistant", "content": message.content})

    def _process_function_call(
        self,
        message,
        task: Task,
        llm: LLM,
        messages: list,
        functions: list,
        output: Output,
    ) -> None:
        """
        Process a function call from the assistant.

        :param message: The message from the assistant.
        :type message: Message
        :param task: The task to be processed.
        :type task: Task
        :param llm: The LLM object.
        :type llm: LLM
        :param messages: A list of messages.
        :type messages: list
        :param functions: A list of function definitions.
        :type functions: list
        :param output: The output object.
        :type output: Output
        """
        function = Function(message.function_call.name, output)
        function_content = function.execute(message.function_call.arguments)
        messages.append(
            {
                "role": "function",
                "content": function_content,
                "name": message.function_call.name,
            }
        )
        task.settings.function_call = "none"
        message = llm.respond(task.settings, messages, functions)
        self._process_message(message, messages)
