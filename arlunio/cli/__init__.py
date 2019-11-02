import argparse
import collections
import logging

import pkg_resources

from arlunio._version import __version__

from ._interface import build_command_parser

logger = logging.getLogger(__name__)

_LogConfig = collections.namedtuple("LogConfig", "level,fmt")
_LOG_LEVELS = [
    _LogConfig(level=logging.INFO, fmt="%(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s]: %(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s][%(name)s]: %(message)s"),
]


def _setup_logging(verbose: int, quiet: bool) -> None:
    """Setup the logging system according to the given args."""

    if quiet:
        return

    verbose = 0 if verbose < 0 else verbose

    try:
        conf = _LOG_LEVELS[verbose]
        others = False
    except IndexError:
        conf = _LOG_LEVELS[-1]
        others = True

    root = logging.getLogger()

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(conf.fmt))
    console.setLevel(conf.level)

    if not others:
        console.addFilter(logging.Filter("arlunio"))

    root.addHandler(console)


def _register_commands(parent: argparse._SubParsersAction, entry_point: str):
    """Given the name of an entrypoint expose all the commands under the given parent.

    In the case where a command cannot be loaded, this function will put a dummy command
    in its place so that we can gracefully handle it and inform the user.
    """
    for cmd in pkg_resources.iter_entry_points(entry_point):
        command = cmd.load()
        build_command_parser(cmd.name, command, parent)


# Top level command line parser
_cli = argparse.ArgumentParser(description="Arlunio's command line interface")
_cli.add_argument(
    "-q", "--quiet", help="disable all console output", action="store_true"
)
_cli.add_argument("--version", help="show version info and exit", action="store_true")
_cli.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="increase output verbosity, repeatable e.g. -v, -vv, -vvv, ...",
)

_commands = _cli.add_subparsers(title="commands")
_register_commands(_commands, "arlunio.cli.commands")


def main():
    args = _cli.parse_args()

    if args.version:
        logger.info("arlunio v%s", __version__)
        return 0

    _setup_logging(args.verbose, args.quiet)

    if hasattr(args, "run"):
        return args.run(args)

    _cli.print_help()
    return 0
