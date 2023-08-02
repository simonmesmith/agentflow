import os
from datetime import datetime
import json


class Output:
    def __init__(self, flow_name: str):
        self.base_path = os.path.join(os.path.dirname(__file__), "outputs")
        self.timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.output_path = f"{self.base_path}/{flow_name}_{self.timestamp}"
        os.mkdir(self.output_path)

    def save(self, file_name, file_contents):
        if type(file_contents) == str:
            with open(f"{self.output_path}/{file_name}", "w") as f:
                f.write(file_contents)
        elif type(file_contents) in (list, dict):
            with open(f"{self.output_path}/{file_name}", "w") as f:
                json.dump(file_contents, f, indent=4)