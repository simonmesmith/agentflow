import os
from dataclasses import dataclass, field
from typing import Any

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


@dataclass
class Settings:
    model: str | None = "gpt-4"
    functions: list[dict[str, str]] | None = field(default_factory=list)
    function_call: str | None = None
    temperature: float | None = 1.0
    top_p: float | None = None
    max_tokens: int | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None


class LLM:
    def __init__(self):
        pass

    def respond(self, settings: Settings, messages: list[dict[str, str]]) -> Any:
        settings_dict = {k:v for k,v in settings.__dict__.items() if v not in (None, [])}
        settings_dict["messages"] = messages
        response = openai.ChatCompletion.create(**settings_dict)
        return response.choices[0].message