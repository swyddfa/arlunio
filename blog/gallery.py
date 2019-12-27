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

import arlunio
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
class ImageContext:
    """Represents the values needed to render the individual image template."""

    author: t.Any
    """Information about the image's author"""

    baseurl: str
    """The base url the site is being hosted on"""

    date: str
    """A string representing the time the site was built"""

    slug: str
    """The machine friendly name of the image."""

    title: str
    """The human friendly name of the image."""

    thumburl: str = ""
    """The url to the image's thumbnail"""

    url: str = ""
    """The url to the full size image"""

    @classmethod
    def fromnb(cls, nb, gallery, config):
        """Create a context from the notebook representing the image."""
        filename = pathlib.Path(nb.__file__).stem
        slug = filename.lower().replace(" ", "-")
        meta = nb.__notebook__.metadata.arlunio
        dimensions = meta.dimensions

        # TODO: Make this smarter
        images = [v for v in nb.__dict__.values() if isinstance(v, arlunio.Canvas)]
        image = images[0]

        # Render the thumbnail for the main gallery page
        thumb = image(250, 250)
        thumbfile = pathlib.Path(config.output, "gallery", "thumb", slug + ".png")
        thumb.save(thumbfile, mkdirs=True)
        thumburl = "thumb/{}.png".format(slug)

        # Render the fullsize image
        full = image(*dimensions)
        fullfile = pathlib.Path(config.output, "gallery", "image", slug + ".png")
        full.save(fullfile, mkdirs=True)
        url = "image/{}.png".format(slug)

        return cls(
            author=meta.author,
            baseurl=gallery.baseurl,
            date=gallery.date,
            slug=slug,
            thumburl=thumburl,
            url=url,
            title=filename,
        )

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class GalleryContext:
    """Represents the values needed to render the main gallery template."""

    baseurl: str
    """The base url the site is being hosted on"""

    date: str
    """A string representing the time the site was built"""

    images: t.List[str] = attr.Factory(list)
    """Represents the images that are included in the gallery"""

    @classmethod
    def new(cls, config, local):
        baseurl = config.baseurl

        if local:
            baseurl = "http://localhost:8000/"

        date = datetime.now().strftime("%d %B %Y -- %H:%M:%S")
        return cls(baseurl=baseurl, date=date)

    def prepare_notebooks(self, notebooks, config):
        """Given the notebooks that represent an image, prepare them."""

        for nb in notebooks:
            image = ImageContext.fromnb(nb, self, config)
            self.images.append(image)

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class Site:

    config: str
    local: bool

    def build(self, destination):
        env = j2.Environment(loader=j2.FileSystemLoader(self.config.templates))
        gallery_template = env.get_template("gallery.html")
        image_template = env.get_template("image.html")

        index = os.path.join(self.config.output, "gallery", "index.html")
        notebooks = load_notebooks(self.config.notebooks)

        context = GalleryContext.new(self.config, self.local)
        context.prepare_notebooks(notebooks, self.config)

        # Render the main index page
        write_file(index, gallery_template.render(context.as_dict()))

        # For each image, render its detail page.
        for image in context.images:
            filename = os.path.join(self.config.output, "gallery", image.slug + ".html")
            write_file(filename, image_template.render(image.as_dict()))


def write_file(filepath, content):
    path = pathlib.Path(filepath)
    logger.debug("Writing file: %s", path)

    if not path.parent.exists():
        logger.debug("Creating dir: %s", path.parent)
        path.parent.mkdir(parents=True)

    with open(str(path), "w") as f:
        f.write(content)


def load_notebooks(notebooks):
    """Discover and load each of the notebooks that represent images."""
    logger.info("Loading notebooks")

    nbdir = pathlib.Path(notebooks)
    loader = NotebookLoader(str(nbdir))

    modules = []

    for nbpath in nbdir.glob("*.ipynb"):
        nbname = nbpath.stem.replace(" ", "_")

        spec = imutil.spec_from_file_location(nbname, str(nbpath), loader=loader)
        module = imutil.module_from_spec(spec)

        logger.debug("--> spec  : %s", spec)
        logger.debug("--> module: %s", module)

        spec.loader.exec_module(module)
        modules.append(module)

    return modules


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
