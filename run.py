import argparse

from agentflow.flow import Flow


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
    flow = Flow(args.flow_name, variables)
    flow.run()


def parse_variables(variables):
    if not variables:
        return {}

    variable_dict = {}
    for variable in variables:
        key, value = variable.split("=")
        variable_dict[key] = value

    return variable_dict


if __name__ == "__main__":
    main()
