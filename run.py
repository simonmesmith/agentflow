"""
This module is used to run Agentflow flows. To run one, use the following command:

.. code-block:: bash

    python -m run --flow=<flow name> --variables '<variable>=<value>' '<variable>=<value>'

Optionally, use -v for verbose output.

"""

import argparse
import logging

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
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed output."
    )

    args = parser.parse_args()
    variables = parse_variables(args.variables)
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Verbose mode enabled.")

    flow = Flow(args.flow_name, variables)
    flow.run()


def parse_variables(variables: list[str]) -> dict[str, str]:
    """
    Parses the variables provided as command line arguments.

    :param variables: A list of strings where each string is a key-value pair in the format 'key=value'.
    :type variables: list[str]
    :return: A dictionary where the keys are the variable names and the values are the corresponding values.
    :rtype: dict[str, str]
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
