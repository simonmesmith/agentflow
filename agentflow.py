import argparse
import json

import openai

from flow import Flow
from function import Function
from output import Output


def main():
    parser = argparse.ArgumentParser(description="AgentFlow")
    parser.add_argument(
        "--flow",
        type=str,
        required=True,
        help="The name of the flow to run. (The part before .json.)",
        dest="flow_name",
    )
    args = parser.parse_args()
    run(args.flow_name)


def run(flow_name: str):
    flow = Flow(flow_name)
    output = Output(flow.name)
    messages = []
    for task in flow["tasks"]:
        messages.append({"role": "user", "content": task["action"]})
        settings = {"model": "gpt-3.5-turbo", "messages": messages}
        if "settings" in task:
            if "function_call" in task["settings"]:
                function = Function(task["settings"]["function_call"])
                settings["functions"] = [function.definition]
                settings["function_call"] = task["settings"]["function_call"]
        response = openai.ChatCompletion.create(**settings)
        messages.append(
            {"role": "assistant", "content": response["choices"][0].message.content}
        )
    output.save("messages.json", messages)


if __name__ == "__main__":
    main()
