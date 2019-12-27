"""This file is responsible for rendering the gallery.

Once this matures it might be an interesting exercise to make it a tool built into
arlunio itself.
"""
import argparse
import collections
import importlib.util as imutil
import logging
import os
import pathlib
import sys
import traceback
import typing as t

from datetime import datetime

import attr
import jinja2 as j2
import tomlkit as toml

from arlunio.imp import NotebookLoader

# from importlib import import_module
logger = logging.getLogger(__name__)

_LogConfig = collections.namedtuple("LogConfig", "level,fmt")
_LOG_LEVELS = [
    _LogConfig(level=logging.INFO, fmt="%(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s]: %(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s][%(name)s]: %(message)s"),
]


def setup_logging(verbose: int, quiet: bool) -> None:
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
        console.addFilter(logging.Filter(__name__))

    root.addHandler(console)


class UserContext:
    def __init__(self, pkg):
        self.pkg = pkg

    def __enter__(self):
        return self

    def __exit__(self, err_type, err, tback):

        if err is None:
            return

        print()
        traceback.print_exception(err_type, err, tback)
        print("\nUnable to load module: {}".format(self.pkg))

        sys.exit(1)


@attr.s(auto_attribs=True)
class Config:
    """Represents site configuration."""

    baseurl: str
    output: str
    notebooks: str
    templates: str

    @classmethod
    def fromfile(cls, filepath):

        with open(filepath) as f:
            config = toml.parse(f.read())

        baseurl = config["site"]["baseurl"]
        templates = config["site"]["templates"]
        output = config["site"]["output"]

        notebooks = config["gallery"]["images"]

        return cls(
            baseurl=baseurl, templates=templates, output=output, notebooks=notebooks
        )


@attr.s(auto_attribs=True)
class Context:
    """Represents values to pass to a context"""

    baseurl: str
    date: str
    images: t.List[str] = []

    @classmethod
    def new(cls, config, local):
        baseurl = config.baseurl

        if local:
            baseurl = "http://localhost:8000/"

        date = datetime.now().strftime("%d %B %Y -- %H:%M:%S")
        return cls(baseurl=baseurl, date=date)

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class Site:

    config: str
    local: bool

    def build(self, destination):
        env = j2.Environment(loader=j2.FileSystemLoader(self.config.templates))
        template = env.get_template("gallery.html")

        index = os.path.join(self.config.output, "index.html")
        context = Context.new(self.config, self.local)

        load_notebooks(self.config.notebooks)

        with open(index, "w") as f:
            f.write(template.render(context.as_dict()))


def load_notebooks(notebooks):
    """Discover and load each of the notebooks that represent images."""
    logger.info("Loading notebooks")

    nbdir = pathlib.Path(notebooks)
    loader = NotebookLoader(str(nbdir))

    for nbpath in nbdir.glob("*.ipynb"):
        nbname = nbpath.stem.replace(" ", "_")
        spec = imutil.spec_from_file_location(nbname, str(nbpath), loader=loader)
        module = imutil.module_from_spec(spec)

        logger.debug("--> spec  : %s", spec)
        logger.debug("--> module: %s", module.__file__)

        spec.loader.exec_module(module)
        logger.info(module.image)


cli = argparse.ArgumentParser(description="Gallery builder for the arlunio blog.")
cli.add_argument("-c", "--config", help="path to config file", default="config.toml")
cli.add_argument(
    "-l",
    "--local",
    help="switch to indicate when building locally",
    action="store_true",
)
cli.add_argument(
    "-o", "--output", help="folder to render results to", default="public/"
)
cli.add_argument(
    "-q", "--quiet", help="disable all console output", action="store_true"
)
cli.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="increase output verbosity, repeatable e.g. -v, -vv, -vvv, ...",
)

if __name__ == "__main__":

    args = cli.parse_args()
    setup_logging(args.verbose, args.quiet)

    config = Config.fromfile(args.config)

    site = Site(config, args.local)
    site.build(args.output)
