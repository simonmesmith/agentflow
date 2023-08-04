import importlib
import json
from abc import ABC, abstractmethod


class BaseFunction(ABC):
    def __init__(self, output):
        self.output = output

    @property
    @abstractmethod
    def definition(self) -> dict:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> str:
        pass


class Function:
    def __init__(self, function_name, output):
        self.module = importlib.import_module(f"functions.{function_name}")
        self.function_class = getattr(
            self.module, function_name.replace("_", " ").title().replace(" ", "")
        )

        self.instance = self.function_class(output)

    @property
    def definition(self) -> dict:
        return self.instance.definition()

    def execute(self, args_json: str) -> str:
        args_dict = json.loads(args_json)
        return self.instance.execute(**args_dict)
