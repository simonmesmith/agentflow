import os

from function import Function
from output import Output


def test_function():
    output = Output("test_function")
    function = Function("save_file", output)
    result = function.execute('{"file_name": "test.txt", "file_contents": "Hello, world!"}')
    assert result == f"{output.output_path}/test.txt"
    os.remove(result)
    os.rmdir(output.output_path)
