from agentflow.function import BaseFunction


class SaveFile(BaseFunction):
    def definition(self) -> dict:
        return {
            "name": "save_file",
            "description": "Save a file to the output directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file, including its extension. For example, test.txt.",
                    },
                    "file_contents": {
                        "type": "string",
                        "description": "The contents of the file.",
                    },
                },
                "required": ["file_name", "file_contents"],
            },
        }

    def execute(self, file_name: str, file_contents: str) -> str:
        return self.output.save(file_name, file_contents)
