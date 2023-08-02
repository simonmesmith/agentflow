import argparse

import openai
from flow_manager import Flow
from output_manager import Output

import json

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        messages.append(
            {"role": "assistant", "content": response["choices"][0].message.content}
        )
    output.save("messages.json", messages)


if __name__ == "__main__":
    main()
