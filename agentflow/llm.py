import os
from dataclasses import dataclass
from typing import Any

import openai
from dotenv import load_dotenv


@dataclass
class Settings:
    model: str | None = "gpt-4"
    function_call: str | None = None
    temperature: float | None = 1.0
    top_p: float | None = None
    max_tokens: int | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None


class LLM:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.environ["OPENAI_API_KEY"]

    def respond(self, settings: Settings, messages: list[dict[str, str]], functions: list[dict[str, str]] | None = None) -> Any:
        openai_args = {
            k: v for k, v in settings.__dict__.items() if v not in (None, [])
        }
        openai_args["messages"] = messages
        if functions:
            openai_args["functions"] = functions
        response = openai.ChatCompletion.create(**openai_args)
        return response.choices[0].message
