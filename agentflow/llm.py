"""
This module provides a class for interacting with OpenAI's LLMs. It includes a dataclass for settings and a class for managing the interaction.
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import openai
from dotenv import load_dotenv
from tenacity import retry, wait_exponential


@dataclass
class Settings:
    """
    This dataclass holds the settings for interacting with OpenAI's LLMs.
    """

    model: str = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4")
    function_call: Optional[str] = None
    temperature: float = 1.0
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None


class LLM:
    """
    This class is responsible for managing the interaction with OpenAI's LLMs.
    """

    def __init__(self):
        """
        Initializes the LLM object by loading the environment variables and setting the OpenAI API key.
        """
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def respond(
        self,
        settings: Settings,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict[str, str]]] = None,
    ) -> Any:
        """
        Sends a request to OpenAI's LLM API and returns the response.

        :param settings: The settings for the interaction.
        :type settings: Settings
        :param messages: The messages to be processed by the language model.
        :type messages: List[Dict[str, str]]
        :param functions: The functions to be processed by the language model.
        :type functions: Optional[List[Dict[str, str]]]
        :return: The response from the language model.
        :rtype: Any
        """
        openai_args = {k: v for k, v in vars(settings).items() if v is not None}
        openai_args["messages"] = messages
        if functions:
            openai_args["functions"] = functions
        response = openai.ChatCompletion.create(**openai_args)
        return response.choices[0].message
