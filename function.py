import importlib
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
    def __init__(self, function_name):
        self.module = importlib.import_module(function_name)
        self.function_class = getattr(self.module, function_name.capitalize())

        self.instance = self.function_class()

    @property
    def definition(self):
        return self.instance.definition()

    def execute(self, *args, **kwargs):
        return self.instance.execute(*args, **kwargs)
