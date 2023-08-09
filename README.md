# Agentflow: Complex LLM Workflows from Simple JSON

![Python lint and test](https://github.com/simonmesmith/agentflow/actions/workflows/build.yml/badge.svg)

Agentflow is a powerful yet user-friendly tool to run workflows powered by LLMs. You can:

* **Write workflows in plain English** in human-readable JSON files.
* **Use variables for dynamic outputs** that change based on user input.
* **Build and execute custom functions** to go beyond text generation.

## Why Agentflow?

Agentflow fills the gap between chat and autonomous interfaces:

* **Chat (e.g. ChatGPT) can't run workflows** because they're conversational.
* **Autonomous (e.g. Auto-GPT) run them unreliably** because they have too much freedom.

Agentflow offers a balanced solution: Workflows that LLMs follow step-by-step.

## Install and Use

Agentflow is currently in development. To try it:

1. Sign up for the [OpenAI API](https://platform.openai.com/overview) and get an [API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)
2. Clone or download this repository.
3. Create a `.env` file from [example.env](https://github.com/simonmesmith/agentflow/blob/main/example.env) and add your OpenAI API key.
4. Run `pip install -r requirements.txt` to install dependencies.

Now you can run flows from the command line, like this:
```bash
python -m run --flow=example
```

### Optional Arguments

#### Use `variables` to pass variables to your flow

```bash
python -m run --flow=example_with_variables --variables 'market=college students' 'price_point=$50'
```

#### Use `v` (verbose) to see task completion in real-time

```bash
python -m run --flow=example -v
```

## Create New Flows

Copy [example.json](https://github.com/simonmesmith/agentflow/blob/main/agentflow/flows/example.json) or [example_with_variables.json](https://github.com/simonmesmith/agentflow/blob/main/agentflow/flows/example_with_variables.json) or create a flow from scratch in this format:

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

## Create New Functions

Copy [save_file.py](https://github.com/simonmesmith/agentflow/blob/main/agentflow/functions/save_file.py) and modify it, or follow these instructions (replace "function_name" with your function name):

1. **Create `function_name.py` in the [functions](https://github.com/simonmesmith/agentflow/tree/main/agentflow/functions) folder**.
2. **Create a class within called `FunctionName`** that inherits from `BaseFunction`.
3. **Add `get_definition()` and `execute()` in the class**. See descriptions of these in `BaseFunction`.

That's it! You can now use your function in `function_call` as shown above. However, you should probably:

4. **Add tests in [tests](https://github.com/simonmesmith/agentflow/tree/main/tests)**! Then you'll know if workflows are failing because of your function.

## License

Agentflow is licensed under the [MIT License](https://github.com/simonmesmith/agentflow/blob/main/LICENSE).
