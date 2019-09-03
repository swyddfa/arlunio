import argparse
import logging
import sys

import pkg_resources

import arlunio.cli

from ._version import __version__

logger = logging.getLogger(__name__)

LOG_LEVELS = [
    (logging.INFO, "%(message)s"),
    (logging.DEBUG, "[%(levelname)s][%(name)s]: %(message)s"),
]


def init_logging(verbose: int, quiet: bool) -> None:
    """Configure the logging system based on the given verbosity."""

    if quiet:
        return

    verbose = 0 if verbose < 0 else verbose

    try:
        level, fmt = LOG_LEVELS[verbose]
        others = False
    except IndexError:
        level, fmt = LOG_LEVELS[-1]
        others = True

    root = logging.getLogger()
    root.setLevel(level)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(fmt))

    if not others:
        console.addFilter(logging.Filter("arlunio"))

    root.addHandler(console)


def show_version():
    print(f"arlunio v{__version__}")


# Top level command line parser for arlunio
cli = argparse.ArgumentParser(description="Command line interface to arlunio")
commands = cli.add_subparsers(title="commands")

# "Global" arguments that can apply to any command.
cli.add_argument(
    "-q", "--quiet", help="disable all console output", action="store_true"
)
cli.add_argument(
    "-V", "--version", help="show version info and exit", action="store_true"
)
cli.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="increase the verbosity of the output, can be repeated e.g. -v, -vv, ...",
)

# Register all the defined commands.
for cmd in pkg_resources.iter_entry_points("arlunio.cli.commands"):
    command = cmd.load()
    arlunio.cli.construct_parser(cmd.name, command, commands)


def main():
    args = cli.parse_args()

    if args.version:
        show_version()
        sys.exit(0)

    init_logging(args.verbose, args.quiet)

    if hasattr(args, "run"):
        args.run(args)
        return

    cli.print_help()


if __name__ == "__main__":
    main()
