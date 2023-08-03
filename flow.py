import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Settings:
    model: str | None = "gpt-4"
    function_call: str | None = None
    temperature: float | None = 1.0


@dataclass
class Task:
    action: str
    settings: Settings = field(default_factory=Settings)


@dataclass
class Flow:
    name: str
    system_message: str | None = None
    tasks: List[Task] = field(default_factory=list)

    def __init__(self, name: str):
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
