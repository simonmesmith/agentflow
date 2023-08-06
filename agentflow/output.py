"""
This module provides a class for managing output files. It creates a unique directory for each flow and allows saving files to that directory.
"""

import json
import os
from datetime import datetime
from typing import Union


class Output:
    """
    This class is responsible for managing output files. It creates a unique directory for each flow and provides a method to save files to that directory.
    """

    def __init__(self, flow_name: str):
        """
        Initializes the Output object with a unique directory for the flow.

        :param flow_name: The name of the flow.
        :type flow_name: str
        """
        self.base_path = os.path.join(os.path.dirname(__file__), "outputs")
        self.timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.output_path = os.path.join(self.base_path, f"{flow_name}_{self.timestamp}")
        os.makedirs(self.output_path, exist_ok=True)

    def save(self, file_name: str, file_contents: Union[str, list, dict]) -> str:
        """
        Saves the file contents to a file in the flow's directory.

        :param file_name: The name of the file.
        :type file_name: str
        :param file_contents: The contents of the file.
        :type file_contents: Union[str, list, dict]
        :return: The path to the saved file.
        :rtype: str
        """
        file_path = os.path.join(self.output_path, file_name)
        mode = "w"
        if isinstance(file_contents, str):
            data_to_write = file_contents
        elif isinstance(file_contents, (list, dict)):
            data_to_write = json.dumps(file_contents, indent=4)
        else:
            raise TypeError("file_contents must be of type str, list, or dict")

        with open(file_path, mode) as f:
            f.write(data_to_write)

        return file_path
