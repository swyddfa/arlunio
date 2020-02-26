import argparse
import collections
import logging
import sys
import textwrap
import traceback

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
    root.setLevel(conf.level)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(conf.fmt))

    if not others:
        console.addFilter(logging.Filter("arlunio"))

    root.addHandler(console)


def build_dummy_command_parser(
    name: str, parent: argparse._SubParsersAction, err
) -> None:
    """Build a dummy command to report an error encountered while loading the real
    one."""

    e_type, e_val, tb = err

    message = "Command unavailable: " + str(e_val)
    parser = parent.add_parser(name, help=message)
    parser.add_argument("collector", nargs=argparse.REMAINDER)

    header = f"\nCommand Unavailable: {name}\n\n"

    body = """\
    This is either because your environment does not have the dependencies
    available required by this command or there is an issue with the command
    itself.\n
    """
    body = textwrap.dedent(body)

    body += f"\t{e_type.__name__}: {e_val}\n"

    if issubclass(e_type, ImportError):
        extra = """\

        Since this is an import error it's probably an issue with your environment
        please make sure you have all the required libraries installed.
        """
        body += textwrap.dedent(extra)

    message = header + body

    def run(args: argparse.Namespace):
        logger.info(message)
        logger.debug("\n%s", "\n".join(traceback.format_exception(e_type, e_val, tb)))

    parser.set_defaults(run=run)


def _register_commands(parent: argparse._SubParsersAction, entry_point: str):
    """Given the name of an entrypoint expose all the commands under the given parent.

    In the case where a command cannot be loaded, this function will put a dummy command
    in its place so that we can gracefully handle it and inform the user.
    """
    commands = sorted(
        list(pkg_resources.iter_entry_points(entry_point)), key=lambda c: c.name
    )
    for cmd in commands:
        try:
            command = cmd.load()
            build_command_parser(cmd.name, command, parent)
        except Exception:
            info = sys.exc_info()
            build_dummy_command_parser(cmd.name, parent, info)


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

    if hasattr(args, "run"):
        _setup_logging(args.verbose, args.quiet)
        return args.run(args)

    _cli.print_help()
    return 0
