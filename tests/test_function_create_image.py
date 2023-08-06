"""
This module contains a test for the CreateImage class in the agentflow.functions.create_image module. It uses the unittest.mock library to mock the OpenAI and requests APIs, and checks that the image creation process works correctly.
"""

import os
import re
from unittest.mock import MagicMock, patch

from agentflow.functions.create_image import CreateImage
from agentflow.output import Output


@patch("openai.Image.create")
@patch("requests.get")
def test_execute(mock_get, mock_create):
    """
    Tests the execute method of the CreateImage class. It mocks the OpenAI and requests APIs, and checks that the image creation process works correctly.

    :param mock_get: A mock for the requests.get function.
    :type mock_get: MagicMock
    :param mock_create: A mock for the openai.Image.create function.
    :type mock_create: MagicMock
    """
    # Mock the openai.Image.create call to return a mock response with a mock image URL
    mock_create.return_value = {"data": [{"url": "https://mockurl.com/mock_image.jpg"}]}

    # Mock the requests.get call to return a mock response with mock image content
    mock_response = MagicMock()
    mock_response.content = b"mock image content"
    mock_get.return_value = mock_response

    output = Output("test_create_image_execute")
    create_image = CreateImage(output)
    result = create_image.execute("a white siamese cat", 1, "1024x1024")

    # Check that the returned image name is a valid SHA-256 hash followed by ".png"
    assert re.match(r"[0-9a-f]{64}\.png$", result) is not None

    # Check that the image file was created with the correct content
    with open(f"{output.output_path}/{result}", "rb") as f:
        assert f.read() == b"mock image content"

    # Clean up the test environment by removing the created file and directory
    os.remove(f"{output.output_path}/{result}")
    os.rmdir(output.output_path)
