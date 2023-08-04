import os

from functions.save_file import SaveFile
from output import Output


def test_execute():
    output = Output("test_save_file_execute")
    save_file = SaveFile(output)
    result = save_file.execute("test.txt", "Hello, world!")
    assert result == f"{output.output_path}/test.txt"
    os.remove(result)
    os.rmdir(output.output_path)
