import shutil
from unittest.mock import MagicMock, patch

import pytest

from agentflow.functions.summarize_text import SummarizeText
from agentflow.output import Output


@pytest.fixture
def output():
    flow = "test_summarize_text"
    output = Output(flow)
    yield output
    shutil.rmtree(output.output_path)


def test_get_definition(output):
    """
    Tests the get_definition method of the SummarizeText class. It checks that the definition of the function is correct.
    """
    summarizer = SummarizeText(output)
    definition = summarizer.get_definition()
    assert definition["name"] == "summarize_text"
    assert "text_to_summarize" in definition["parameters"]["properties"]


def test_truncate_text(output):
    """
    Tests the _truncate_text method of the SummarizeText class. It checks that the text is truncated correctly.
    """
    summarizer = SummarizeText(output)
    text = "a" * (summarizer.max_tokens * summarizer.chars_per_token + 10)
    truncated_text = summarizer._truncate_text(text)
    assert len(truncated_text) == summarizer.max_tokens * summarizer.chars_per_token


def test_prepare_messages(output):
    """
    Tests the _prepare_messages method of the SummarizeText class. It checks that the messages are prepared correctly.
    """
    summarizer = SummarizeText(output)
    messages = summarizer._prepare_messages("text", "instructions")
    assert messages[0]["content"] == "You are an AI summarizer. instructions"
    assert messages[1]["content"] == "Text to summarize: text"


def test_select_model_base(output):
    """
    Tests the _select_model method of the SummarizeText class. It checks that the correct model is selected for 4000 tokens or less.
    """
    summarizer = SummarizeText(output)
    # Constructing a message size that fits the base model
    messages = [{"content": "a" * (1000 * summarizer.chars_per_token)}]
    model, _ = summarizer._select_model(messages)
    assert model == "gpt-3.5-turbo"


def test_select_model_16k(output):
    """
    Tests the _select_model method of the SummarizeText class. It checks that the correct model is selected for more than 4000 tokens.
    """
    summarizer = SummarizeText(output)
    # Constructing a message size that requires the larger 16k model
    messages = [{"content": "a" * (5000 * summarizer.chars_per_token)}]
    model, _ = summarizer._select_model(messages)
    assert model == "gpt-3.5-turbo-16k"


def test_calculate_tokens(output):
    """
    Tests the _calculate_tokens method of the SummarizeText class. It checks that the number of tokens is calculated correctly.
    """
    summarizer = SummarizeText(output)
    tokens = summarizer._calculate_tokens([{"content": "a" * 1000}])
    assert tokens == 254


@patch("openai.ChatCompletion.create")
def test_execute(mock_create, output):
    """
    Tests the execute method of the SummarizeText class. It mocks the OpenAI API, and checks that the summarization process works correctly.
    """
    summarizer = SummarizeText(output)
    mock_create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="summary"))]
    )
    summary = summarizer.execute("text", "instructions")
    assert summary == "summary"


@patch("openai.ChatCompletion.create")
def test_execute_exception(mock_create, output):
    """
    Tests that we're handling exceptions in the execute method of the SummarizeText class.
    """
    summarizer = SummarizeText(output)
    mock_create.side_effect = Exception("OpenAI Error")
    try:
        summarizer.execute("text", "instructions")
    except Exception as e:
        assert str(e) == "Error summarizing text"
