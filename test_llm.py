from llm import LLM, Settings


def test_respond():
    llm = LLM()
    settings = Settings()
    messages = [{"role": "user", "content": "This is a test. Are you there?"}]
    response = llm.respond(settings, messages)
    assert response is not None