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
    functions = []
    for task in flow.tasks:
        if task.settings.function_call is not None:
            function = Function(task.settings.function_call, output)
            functions.append(function.definition)

    for task in flow.tasks:
        print("Flow:", task.action)
        print("Function:", task.settings.function_call)
        messages.append({"role": "user", "content": task.action})

        task.settings.function_call = (
            "none"
            if task.settings.function_call is None
            else {"name": task.settings.function_call}
        )

        message = llm.respond(task.settings, messages, functions)

        if message.content:
            print("Assistant: ", message.content)
            messages.append({"role": "assistant", "content": message.content})

        elif message.function_call:
            function = Function(message.function_call.name, output)
            function_content = function.execute(message.function_call.arguments)
            messages.append(
                {
                    "role": "function",
                    "content": function_content,
                    "name": message.function_call.name,
                }
            )
            task.settings.function_call = "none"
            message = llm.respond(task.settings, messages, functions)
            messages.append({"role": "assistant", "content": message.content})
            print("Assistant: ", message.content)
    output.save("messages.json", messages)
    print(f"Find outputs at {output.output_path}")


if __name__ == "__main__":
    main()
