import logging
import pkg_resources

import click

from .context import Context


LOG_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]
logger = logging.getLogger(__name__)


def init_logging(verbose):
    """Configure the logging system based on command line
    arguments."""

    verbose = 0 if verbose < 0 else verbose

    try:
        level = LOG_LEVELS[verbose]
        others = False
    except IndexError:
        level = logging.DEBUG
        others = True

    root = logging.getLogger()
    root.setLevel(level)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("[%(name)s][%(levelname)s]: %(message)s"))

    if not others:
        console.addFilter(logging.Filter("stylo"))

    root.addHandler(console)


@click.group()
@click.option("-v", "--version", count=True)
@click.pass_context
def cli(ctx, version):
    """Command line interface to stylo."""
    init_logging(version)
    context = Context.create()

    ctx.obj = context


# Register all the defined commands.
for cmd in pkg_resources.iter_entry_points("stylo.cli.commands"):
    register = cmd.load()
    register(cli, click)

if __name__ == "__main__":
    cli()
