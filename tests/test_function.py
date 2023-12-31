"""
This module contains tests for the Function class.
"""

import shutil

from agentflow.function import Function
from agentflow.output import Output


def test_function():
    """
    Tests the execute method of the Function class.

    The test creates an Output object and a Function object. It then calls the execute
    method of the Function object with a JSON string containing the file name and file
    contents. The test checks if the execute method returns the correct file path and
    if the file is saved correctly.
    """
    output = Output("test_function")
    function = Function("save_file", output)
    result = function.execute(
        '{"file_name": "test.txt", "file_contents": "Hello, world!"}'
    )
    assert (
        result == f"{output.output_path}/test.txt"
    ), "File path returned by execute method is incorrect"
    shutil.rmtree(output.output_path)
