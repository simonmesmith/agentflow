import os
import re
from unittest.mock import patch

from agentflow.functions.create_image import CreateImage
from agentflow.output import Output


@patch("openai.Image.create")
def test_execute(mock_create):
    mock_create.return_value = {"data": [{"url": "https://mockurl.com/mock_image.jpg"}]}

    output = Output("test_create_image_execute")
    create_image = CreateImage(output)
    result = create_image.execute("a white siamese cat", 1, "1024x1024")

    # Check that the returned image name is a valid SHA-256 hash followed by ".png"
    assert re.match(r"[0-9a-f]{64}\.png$", result) is not None

    os.remove(f"{output.output_path}/{result}")
    os.rmdir(output.output_path)
