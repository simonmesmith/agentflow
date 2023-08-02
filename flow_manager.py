import json
import os


class Flow(dict):
    def __init__(self, name: str):
        self.name = name
        self.load()

    def load(self):
        path = os.path.join(os.path.dirname(__file__), "flows", f"{self.name}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"The flow {self.name} doesn't exist.")
        with open(path, "r") as f:
            data = json.load(f)
            self.update(data)
