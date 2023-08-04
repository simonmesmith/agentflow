import argparse

from flow import Flow
from function import Function
from llm import LLM
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
    llm = LLM()
    flow = Flow(flow_name)
    output = Output(flow.name)
    messages = []
    if flow.system_message:
        messages.append({"role": "system", "content": flow.system_message})
    for task in flow.tasks:
        print(task.action)
        if task.settings.function_call is not None:
            function = Function(task.settings.function_call, output)
            task.settings.function_call = {"name": task.settings.function_call}
            task.settings.functions = [function.definition]
        messages.append({"role": "user", "content": task.action})
        message = llm.respond(task.settings, messages)
        if message.content:
            messages.append({"role": "assistant", "content": message.content})
        elif message.function_call:
            function_content = function.execute(message.function_call.arguments)
            messages.append(
                {
                    "role": "function",
                    "content": function_content,
                    "name": message.function_call.name,
                }
            )
            message = llm.respond(task.settings, messages)
            if message.content:
                messages.append({"role": "assistant", "content": message.content})
    output.save("messages.json", messages)


if __name__ == "__main__":
    main()
