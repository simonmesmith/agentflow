"""
This module is used to run Agentflow flows. To run one, use the following command:
python -m run --flow=<flow name> --variables '<variable>=<value>' '<variable>=<value>'
"""

import argparse

from agentflow.flow import Flow


def main() -> None:
    """
    The main function that parses command line arguments and runs the specified flow.
    """
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


def parse_variables(variables: list[str]) -> dict[str, str]:
    """
    Parses the variables provided as command line arguments.

    Args:
        variables (list[str]): A list of strings where each string is a key-value pair in the format 'key=value'.

    Returns:
        dict[str, str]: A dictionary where the keys are the variable names and the values are the corresponding values.
    """
    if not variables:
        return {}

    variable_dict = {}
    for variable in variables:
        key, value = variable.split("=")
        variable_dict[key] = value

    return variable_dict


if __name__ == "__main__":
    main()
