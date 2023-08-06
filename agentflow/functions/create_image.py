"""
This module contains a class for creating an image from a description using OpenAI's API. It generates a unique image name based on the prompt and the current time, downloads the image, and saves it to a specified output path.
"""

import hashlib
import time

import openai
import requests

from agentflow.function import BaseFunction


class CreateImage(BaseFunction):
    """
    This class inherits from the BaseFunction class. It defines a function for creating an image from a description using OpenAI's API.
    """

    def definition(self) -> dict:
        """
        Returns a dictionary that defines the function. It includes the function's name, description, and parameters.

        :return: A dictionary that defines the function.
        :rtype: dict
        """
        return {
            "name": "create_image",
            "description": "Create an image from a description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt that describes the image. Be specific and detailed about the content and style of the image.",
                    }
                },
                "required": ["prompt"],
            },
        }

    def execute(self, prompt: str, n: int = 1, size: str = "1024x1024") -> str:
        """
        Creates an image from a description using OpenAI's API, generates a unique image name based on the prompt and the current time, downloads the image, and saves it to a specified output path.

        :param prompt: The prompt that describes the image.
        :type prompt: str
        :param n: The number of images to generate. Defaults to 1. Currently, only 1 is supported.
        :type n: int, optional
        :param size: The size of the image. Defaults to "1024x1024". Currently, only "1024x1024" is supported.
        :type size: str, optional
        :return: The name of the image file.
        :rtype: str
        """
        image_name = self._generate_image_name(prompt)
        image_url = self._create_image(prompt, n, size)
        self._download_and_save_image(image_url, image_name)
        return image_name

    def _generate_image_name(self, prompt: str) -> str:
        """
        Generates a unique image name based on the prompt and the current time.

        :param prompt: The prompt that describes the image.
        :type prompt: str
        :return: The name of the image file.
        :rtype: str
        """
        timestamp = str(time.time())
        return hashlib.sha256((prompt + timestamp).encode()).hexdigest() + ".png"

    def _create_image(self, prompt: str, n: int, size: str) -> str:
        """
        Creates an image from a description using OpenAI's API.

        :param prompt: The prompt that describes the image.
        :type prompt: str
        :param n: The number of images to generate.
        :type n: int
        :param size: The size of the image.
        :type size: str
        :return: The URL of the image.
        :rtype: str
        """
        response = openai.Image.create(prompt=prompt, n=n, size=size)
        return response["data"][0]["url"]

    def _download_and_save_image(self, image_url: str, image_name: str) -> None:
        """
        Downloads the image and saves it to a specified output path.

        :param image_url: The URL of the image.
        :type image_url: str
        :param image_name: The name of the image file.
        :type image_name: str
        """
        image_path = f"{self.output.output_path}/{image_name}"
        image_data = requests.get(image_url).content
        with open(image_path, "wb") as handler:
            handler.write(image_data)
