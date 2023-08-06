"""
This module contains a test for the SaveFile class in the agentflow.functions.save_file module. It checks that the file saving process works correctly.
"""

import os

from agentflow.functions.save_file import SaveFile
from agentflow.output import Output


def test_execute():
    """
    Tests the execute method of the SaveFile class. It checks that the file saving process works correctly.
    """
    output = Output("test_save_file_execute")
    save_file = SaveFile(output)
    result = save_file.execute("test.txt", "Hello, world!")

    # Check that the returned file path is correct
    assert result == f"{output.output_path}/test.txt"

    # Clean up the test environment by removing the created file and directory
    os.remove(result)
    os.rmdir(output.output_path)
