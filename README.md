# Agentflow: Complex LLM Workflows from Simple JSON

![Python lint and test](https://github.com/simonmesmith/agentflow/actions/workflows/build.yml/badge.svg)

Agentflow is designed to be a powerful yet user-friendly tool for creating and executing workflows powered by large language models (LLMs). With Agentflow, you can:

* **Craft workflows in plain English**: Workflows are written in human-readable JSON files.
* **Develop custom functions**: Extend Agentflow's capabilities as per your needs.
* **Generate autonomous outputs**: Maintain control while allowing the system to work independently.

## Why Agentflow?

While LLM interfaces like ChatGPT and Bard facilitate turn-by-turn conversations, they limit automation possibilities. Tools like AutoGPT and BabyAGI aim to address this by empowering LLMs to autonomously create and execute to-do lists. However, these tools can't always guarantee the desired outcomes.

Agentflow offers a balanced solution. It allows you to define workflows in an easy-to-understand JSON format, which LLMs then execute step-by-step. You can include functions in your workflows to enhance the LLMs' capabilities, enabling the execution of complex multi-step processes.

## Installation and Use

Agentflow is currently in development. To try it:

1. Sign up for the [OpenAI API](https://platform.openai.com/overview) and get an [API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
2. Clone or download this repository.
3. Create a `.env` file from `example.env` and insert your OpenAI API key.
4. Install the necessary dependencies by running `pip install -r requirements.txt`.

Now, you're ready to run Agentflow:

* Run `python -m run --flow=example` to run a basic example flow.
* To try a workflow with variables, run `python -m run --flow=example_with_variables --variables 'market=college students' 'price_point=$50'`.

## Creating Your Own Flows

Creating flows is straightforward. You can use [example.json](https://github.com/simonmesmith/agentflow/blob/main/agentflow/flows/example.json) or [example_with_variables.json](https://github.com/simonmesmith/agentflow/blob/main/agentflow/flows/example_with_variables.json) as a starting point. If you prefer to create a flow from scratch, use the following format:

```json
{
    "system_message": "An optional message that guides the model's behavior.",
    "tasks": [
        {
            "action": "Instruct the LLM here!"
        },
        {
            "action": "Actions can have settings, including function calls and temperature, like so:",
            "settings": {
                "function_call": "save_file",
                "temperature": 0.5
            }
        },
        {
            "action": "..."
        }
    ]
}
```

## Creating Your Own Functions

You can extend Agentflow's capabilities by creating your own functions. To start, you can just copy a function file like [save_file.py](https://github.com/simonmesmith/agentflow/blob/main/agentflow/functions/save_file.py) and modify it.

Alternatively, you can create a new function from scratch. First, create a new file in the [functions](https://github.com/simonmesmith/agentflow/tree/main/agentflow/functions) directory. The file name will be the function name. For instance, `functions/save_file.py` creates a function called `save_file`. Next, create a function class in the format `FunctionName` that inherits from `BaseFunction`. If you do this, and use the correct JSON function definition, you can incorporate your new function into your workflows. 

Please note: It's a good idea to create tests for your functions, to make sure they behave the way you expect. Otherwise, you may not know whether you're getting errors from the LLM or from your function.

## License

Agentflow is licensed under the [MIT License](https://github.com/simonmesmith/agentflow/blob/main/LICENSE).
