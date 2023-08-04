from unittest.mock import MagicMock, patch

from agentflow.llm import Settings


@patch("agentflow.llm.LLM")
def test_respond(mock_llm_class):
    mock_llm_instance = MagicMock()
    mock_llm_instance.respond.return_value = {
        "role": "assistant",
        "content": "Yes, I am here!",
    }
    mock_llm_class.return_value = mock_llm_instance

    llm = mock_llm_class()
    settings = Settings()
    messages = [{"role": "user", "content": "This is a test. Are you there?"}]
    response = llm.respond(settings, messages)
    assert response is not None
    mock_llm_instance.respond.assert_called_once_with(settings, messages)
