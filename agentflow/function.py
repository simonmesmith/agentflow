"""
This module provides classes for managing functions. It includes an abstract base class for functions and a class for managing function instances.
"""

import importlib
import json
from abc import ABC, abstractmethod

from agentflow.output import Output


class BaseFunction(ABC):
    """
    This abstract base class defines the interface for functions.
    """

    def __init__(self, output: Output):
        """
        Initializes the BaseFunction object with an output object.

        :param output: The output object.
        :type output: Output
        """
        self.output = output

    @abstractmethod
    def get_definition(self) -> dict:
        """
        Returns the definition of the function.

        :return: The definition of the function.
        :rtype: dict
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> str:
        """
        Executes the function with the given arguments.

        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :return: The result of the function execution.
        :rtype: str
        """
        pass


class Function:
    """
    This class is responsible for managing function instances.
    """

    def __init__(self, function_name: str, output: Output):
        """
        Initializes the Function object by importing the function module and creating an instance of the function class.

        :param function_name: The name of the function.
        :type function_name: str
        :param output: The output object.
        :type output: Output
        """
        self.module = importlib.import_module(f"agentflow.functions.{function_name}")
        function_class_name = function_name.replace("_", " ").title().replace(" ", "")
        self.function_class = getattr(self.module, function_class_name)
        self.instance = self.function_class(output)

    @property
    def definition(self) -> dict:
        """
        Returns the definition of the function instance.

        :return: The definition of the function instance.
        :rtype: dict
        """
        return self.instance.get_definition()

    def execute(self, args_json: str) -> str:
        """
        Executes the function instance with the given arguments.

        :param args_json: The arguments in JSON format as a string.
        :type args_json: str
        :return: The result of the function execution.
        :rtype: str
        """
        args_dict = json.loads(args_json)
        return self.instance.execute(**args_dict)
