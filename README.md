# Agentflow

![Python lint and test](https://github.com/simonmesmith/agentflow/actions/workflows/lint_and_test_python.yml/badge.svg)

The goal is for Agentflow to be a powerful, easy-to-use tool to create and execute large language model (LLM)-powered workflows. It will allow you to:

* **Write workflows in plain English** (in JSON files).
* **Create custom functions** to expand capabilities.
* **Generate outputs autonomously** while retaining control.

## Why Agentflow?

Large language model (LLM) interfaces like ChatGPT and Bard enable turn-by-turn conversations. This is great for dialogue, but limits automation opportunities. Sometimes, you know the exact steps you want an LLM to take, and you just want it to execute those steps sequentially without your involvement.

Some tools out there, like AutoGPT and BabyAGI, attempt to solve this by giving LLMs autonomy to create and execute to-do lists. Unfortunately, current LLMs aren't quite capable yet of operating with such a huge degree of autonomy. There's no guarantee they'll actually do what you want, in the way that you want it.

Agentflow is a middle ground between turn-by-turn conversational interfaces like ChatGPT and Bard, and completely autonomous tools like AutoGPT and BabyAGI. You define workflows in human-readable JSON, and LLMs execute them step-by-step. Workflows can include functions that extend LLMs' capabilities, allowing you to execute complex processes with multiple steps.

## Installation

Agentflow is currently in development. To try it:

1. Clone this repository.
2. Install the dependencies in `requirements.txt`.
3. Run `python -m run --flow=example` to run the example flow.

## License

Agentflow is licensed under the [MIT License](https://github.com/simonmesmith/agentflow/blob/main/LICENSE).
