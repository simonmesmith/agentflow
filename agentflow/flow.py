import json
import os
import re

from agentflow.llm import Settings


class Task:
    def __init__(self, action: str, settings: Settings = None):
        self.action = action
        self.settings = settings if settings else Settings()


class Flow:
    def __init__(self, name: str, variables: dict = None):
        base_path = os.path.join(os.path.dirname(__file__), "flows")
        file_path = f"{base_path}/{name}.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}.")

        with open(file_path, "r") as file:
            data = json.load(file)

        self.name = name
        self.system_message = data.get("system_message")
        self.tasks = [
            Task(task["action"], Settings(**task.get("settings", {})))
            if "settings" in task
            else Task(task["action"])
            for task in data.get("tasks", [])
        ]

        self._validate_and_format_messages(variables)

    def _validate_and_format_messages(self, variables: dict):
        if not variables:
            variables = {}

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

        if self.system_message:
            self.system_message = (
                self.system_message.format(**variables)
                .replace("{{", "{")
                .replace("}}", "}")
            )
        for task in self.tasks:
            if task.action:
                task.action = (
                    task.action.format(**variables)
                    .replace("{{", "{")
                    .replace("}}", "}")
                )
