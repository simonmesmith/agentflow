import hashlib
import time

import openai
import requests

from agentflow.function import BaseFunction


class CreateImage(BaseFunction):
    def definition(self) -> dict:
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
                    # We can add these later, perhaps:
                    # "n": {
                    #     "type": "integer",
                    #     "description": "The number of images to generate.",
                    # },
                    # "size": {
                    #     "type": "string",
                    #     "description": "The size of the image.",
                    # },
                },
                "required": ["prompt"],
            },
        }

    def execute(self, prompt: str, n: int = 1, size: str = "1024x1024") -> str:
        response = openai.Image.create(prompt=prompt, n=n, size=size)
        image_url = response["data"][0]["url"]

        # Generate a unique image name based on the prompt and the current time
        timestamp = str(time.time())
        image_name = hashlib.sha256((prompt + timestamp).encode()).hexdigest() + ".png"

        image_path = f"{self.output.output_path}/{image_name}"
        image_data = requests.get(image_url).content
        with open(image_path, "wb") as handler:
            handler.write(image_data)
        return image_name
