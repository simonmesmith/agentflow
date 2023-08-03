import os

from output import Output


def test_init():
    output = Output("test_output_init")
    assert os.path.exists(output.output_path)
    os.rmdir(output.output_path)


def test_save():
    output = Output("test")

    output.save("test.txt", "test_output_save")
    assert os.path.exists(output.output_path + "/test.txt")
    os.remove(output.output_path + "/test.txt")

    output.save("test.json", [{"test": "test1"}, {"test": "test2"}])
    assert os.path.exists(output.output_path + "/test.json")
    os.remove(output.output_path + "/test.json")

    os.rmdir(output.output_path)
