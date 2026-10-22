"""Only implemented foundation commands are exposed."""

import argparse
import sys
from collections.abc import Sequence

from credit_risk.config import ConfigError, load_config


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Credit default research foundation utilities.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    validate = subcommands.add_parser(
        "validate-config", help="Validate foundation YAML configuration"
    )
    validate.add_argument("path", help="Path to a YAML configuration file")
    args = parser.parse_args(argv)
    try:
        load_config(args.path)
    except ConfigError as exc:
        print(f"Invalid configuration: {exc}", file=sys.stderr)
        return 1
    print("Configuration valid (foundation schema only; no data or model evaluated).")
    return 0
