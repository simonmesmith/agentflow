import os

from function import Function
from output import Output


def test_function():
    output = Output("test_function")
    function = Function("save_file", output)
    result = function.execute("test.txt", "Hello, world!")
    assert result == f"{output.output_path}/test.txt"
    os.remove(result)
    os.rmdir(output.output_path)
