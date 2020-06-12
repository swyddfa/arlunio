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
import random
import subprocess
import sys
import traceback
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

import attr
import jinja2 as j2
import PIL
import tomlkit as toml
from markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from tqdm import tqdm

import arlunio
import arlunio.lib.image as img
from arlunio.imp import NotebookLoader

# from importlib import import_module
logger = logging.getLogger(__name__)

_LogConfig = collections.namedtuple("LogConfig", "level,fmt")
_LOG_LEVELS = [
    _LogConfig(level=logging.INFO, fmt="%(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s]: %(message)s"),
    _LogConfig(level=logging.DEBUG, fmt="[%(levelname)s][%(name)s]: %(message)s"),
]


def get_date_added(filepath: str) -> datetime:
    """Given a filepath, get the date the file was added."""

    cmd = ["git", "log", "--diff-filter=A", "--pretty=format:%aI", "--", filepath]
    logger.debug("Running command: %s", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True)
    isotime = result.stdout.decode("utf8")

    return datetime.fromisoformat(isotime)


def get_num_revisions(filepath: str) -> int:
    """Given a filepath, get the number of revisions made to it"""

    cmd = ["git", "log", "--pretty=format:%aI", "--", filepath]
    logger.debug("Running command: %s", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True)
    history = result.stdout.decode("utf8")

    return len(history.split("\n"))


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
class NbCell:

    contents: str
    """The contents of the cell"""

    raw: str
    """The raw content of the cell"""

    type: str
    """The type of the cell"""

    @classmethod
    def fromcell(cls, cell):
        """Converts the jupyter representation of a cell into one we can show in a
        webpage."""
        type = cell.cell_type

        if type == "code":
            contents = highlight(cell.source, PythonLexer(), HtmlFormatter())

        if type == "markdown":
            contents = markdown(cell.source, extensions=["extra"])

        return cls(type=type, contents=contents, raw=cell.source)


def find_image(candidates: Dict[str, img.Image]) -> img.Image:
    """Try and find the image we should be pushing into the gallery.

    The process for discovering images is as follows:

    - If there is only a single image in the namespace then we'll use that.
    - If there is more than one image in the namespace, but there is one called
      'image' then we'll use that.
    """
    image = None

    if len(candidates) == 0:
        raise ValueError("Notebook did not produce a usable image.")

    if len(candidates) == 1:
        image = list(candidates.values())[0]

    if image is None and "image" in candidates:
        image = candidates["image"]

    if image is None:
        names = ", ".join("'" + k + "'" for k in candidates.keys())
        raise ValueError(f"Can't determine image object to use from namespace: {names}")

    return image


@attr.s(auto_attribs=True)
class ImageContext:
    """Represents the values needed to render the individual image template."""

    author: Any
    """Information about the image's author"""

    arlunio_version: str
    """The version of arlunio used to build the site"""

    baseurl: str
    """The base url the site is being hosted on"""

    created: str
    """The date the image was created"""

    date: str
    """A string representing the time the site was built"""

    revision: int
    """Number of revisions made to the image."""

    sloc: int
    """Rough line of code count"""

    slug: str
    """The machine friendly name of the image."""

    title: str
    """The human friendly name of the image."""

    version: str
    """The version of arlunio used to originally make the image."""

    cells: List[NbCell] = attr.Factory(list)
    """The list of cells representing the notebook that defines the image."""

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
        created = get_date_added(nb.__file__)
        num_revisions = get_num_revisions(nb.__file__)

        cells = [NbCell.fromcell(cell) for cell in nb.__notebook__.cells]
        code = "\n".join([cell.raw for cell in cells if cell.type == "code"])
        sloc = code.count("\n")

        candidates = {k: v for k, v in nb.__dict__.items() if isinstance(v, img.Image)}

        image = find_image(candidates)

        # Render the fullsize image
        fullfile = pathlib.Path(config.output, "gallery", "image", slug + ".png")
        img.save(image, fullfile, mkdirs=True)
        url = "image/{}.png".format(slug)

        # Create a scaled down version to use as a thumbnail on the main page
        thumb = image.copy()
        thumb.thumbnail((250, 250), PIL.Image.BICUBIC)
        thumbfile = pathlib.Path(config.output, "gallery", "thumb", slug + ".png")
        img.save(thumb, thumbfile, mkdirs=True)
        thumburl = "thumb/{}.png".format(slug)

        return cls(
            author=meta.author,
            arlunio_version=gallery.arlunio_version,
            baseurl=gallery.baseurl,
            cells=cells,
            created=created.strftime("%d %b %Y"),
            date=gallery.date,
            revision=num_revisions,
            sloc=sloc,
            slug=slug,
            thumburl=thumburl,
            title=filename,
            url=url,
            version=meta.version,
        )

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class GalleryContext:
    """Represents the values needed to render the main gallery template."""

    arlunio_version: str
    """The version of arlunio used to build the site"""

    baseurl: str
    """The base url the site is being hosted on"""

    date: str
    """A string representing the time the site was built"""

    images: List[str] = attr.Factory(list)
    """Represents the images that are included in the gallery"""

    @classmethod
    def new(cls, config, local):
        baseurl = config.baseurl

        if local:
            baseurl = "http://localhost:8001/"

        date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        return cls(arlunio_version=arlunio.__version__, baseurl=baseurl, date=date)

    def prepare_notebooks(self, notebooks, config, skip_failures=False):
        """Given the notebooks that represent an image, prepare them."""

        # Shuffle the notebooks so that the gallery is drawn in a random order
        # on each build.
        random.shuffle(notebooks)

        for nb in tqdm(notebooks, desc="Rendering images"):

            try:
                image = ImageContext.fromnb(nb, self, config)
            except Exception as err:
                if skip_failures:
                    logger.warning(
                        "Skipping broken notebook: %s -- %s", nb.__file__, err
                    )
                    continue

                raise RuntimeError(f"Broken notebook {nb.__file__}") from err

            self.images.append(image)

    def as_dict(self):
        return attr.asdict(self)


@attr.s(auto_attribs=True)
class Site:

    config: str
    local: bool

    def build(self, destination, skip_failures=False):
        env = j2.Environment(loader=j2.FileSystemLoader(self.config.templates))
        gallery_template = env.get_template("gallery.html")
        image_template = env.get_template("image.html")

        index = os.path.join(self.config.output, "gallery", "index.html")
        notebooks = load_notebooks(self.config.notebooks, skip_failures)

        context = GalleryContext.new(self.config, self.local)
        context.prepare_notebooks(notebooks, self.config, skip_failures)

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


def load_notebooks(notebooks, skip_failures=False):
    """Discover and load each of the notebooks that represent images."""
    nbdir = pathlib.Path(notebooks)
    loader = NotebookLoader(str(nbdir))

    modules = []

    for nbpath in tqdm(list(nbdir.glob("*.ipynb")), desc="Loading notebooks"):
        nbname = nbpath.stem.replace(" ", "_")

        spec = imutil.spec_from_file_location(nbname, str(nbpath), loader=loader)
        module = imutil.module_from_spec(spec)

        logger.debug("--> spec  : %s", spec)
        logger.debug("--> module: %s", module)

        try:
            spec.loader.exec_module(module)
        except Exception as err:

            if skip_failures:
                logger.warning("Skipping broken notebook: %s -- %s", nbpath, err)
                continue

            raise RuntimeError(f"Broken notebook: {nbpath}") from err

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
    "-s",
    "--skip-failures",
    help="skip any notebooks that cause an exception",
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
    site.build(args.output, args.skip_failures)
