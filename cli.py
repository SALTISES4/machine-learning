#!/bin/env python3
import argparse

from src import run_server


def read_args() -> argparse.Namespace:
    command_choices = ("run-server",)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=command_choices,
        help="Command to run from:\n  {}".format("\n  ".join(command_choices)),
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Configuration file to use in the format "
        "config/`name`-config.yml",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = read_args()

    if args.command == "run-server":
        if args.config is None:
            raise ValueError(
                "A configuration file is needed for the command "
                f"{args.command}."
            )
        run_server(args.config)
