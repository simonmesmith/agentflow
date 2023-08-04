from unittest.mock import patch

from llm import LLM, Settings


@patch.object(
    LLM, "respond", return_value={"role": "assistant", "content": "Yes, I am here!"}
)
def test_respond(mock_respond):
    llm = LLM()
    settings = Settings()
    messages = [{"role": "user", "content": "This is a test. Are you there?"}]
    response = llm.respond(settings, messages)
    assert response is not None
    mock_respond.assert_called_once_with(settings, messages)
