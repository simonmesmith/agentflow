import argparse

from agentflow.flow import Flow
from agentflow.function import Function
from agentflow.llm import LLM
from agentflow.output import Output


def main():
    parser = argparse.ArgumentParser(description="AgentFlow")
    parser.add_argument(
        "--flow",
        type=str,
        required=True,
        help="The name of the flow to run. (The part before .json.)",
        dest="flow_name",
    )
    parser.add_argument(
        "--variables",
        nargs="*",
        help="Variables to be used in the flow. Should be in the format key1=value1 key2=value2. Put key=value pairs in quotes if they contain space.",
        dest="variables",
    )
    args = parser.parse_args()
    variables = parse_variables(args.variables)
    run(args.flow_name, variables)


def parse_variables(variables):
    if not variables:
        return {}

    variable_dict = {}
    for variable in variables:
        key, value = variable.split("=")
        variable_dict[key] = value

    return variable_dict


def run(flow_name: str, variables: dict):
    llm = LLM()
    flow = Flow(flow_name, variables)
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
    print(f"Find outputs at {output.output_path}")


if __name__ == "__main__":
    main()
