"""This file is responsible for rendering the gallery.

Once this matures it might be an interesting exercise to make it a tool built into
arlunio itself.
"""
import argparse
import collections
import logging
import pathlib
import random
import shutil
import subprocess
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

import arlunio
import arlunio.image as image
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

    try:
        return datetime.fromisoformat(isotime)
    except ValueError as err:
        logger.debug("Unable to parse datetime, %s", err)
        return datetime.now()


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
        contents = ""

        if type == "code":
            contents = highlight(cell.source, PythonLexer(), HtmlFormatter())

        if type == "markdown":
            contents = markdown(cell.source, extensions=["extra"])

        return cls(type=type, contents=contents, raw=cell.source)


def find_image(candidates: Dict[str, image.Image]) -> image.Image:
    """Try and find the image we should be pushing into the gallery.

    The process for discovering images is as follows:

    - If there is only a single image in the namespace then we'll use that.
    - If there is more than one image in the namespace, but there is one called
      'image' then we'll use that.
    """
    img = None

    if len(candidates) == 0:
        raise ValueError("Notebook did not produce a usable image.")

    if len(candidates) == 1:
        img = list(candidates.values())[0]

    if image is None and "image" in candidates:
        img = candidates["image"]

    if img is None:
        names = ", ".join("'" + k + "'" for k in candidates.keys())
        raise ValueError(f"Can't determine image object to use from namespace: {names}")

    return img


@attr.s(auto_attribs=True)
class ImageContext:
    """Represents the values needed to render the individual image template."""

    author: Any
    """Information about the image's author"""

    created: str
    """The date the image was created"""

    dimensions: Dict[str, int]
    """The dimensions of the image."""

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
    def fromnb(cls, nb, config):
        """Create a context from the notebook representing the image."""
        filename = pathlib.Path(nb.__file__).stem
        slug = filename.lower().replace(" ", "-")

        meta = nb.__notebook__.metadata.arlunio
        created = get_date_added(nb.__file__)
        num_revisions = get_num_revisions(nb.__file__)

        cells = [NbCell.fromcell(cell) for cell in nb.__notebook__.cells]
        code = "\n".join([cell.raw for cell in cells if cell.type == "code"])
        sloc = code.count("\n")

        candidates = {
            k: v for k, v in nb.__dict__.items() if isinstance(v, image.Image)
        }

        img = find_image(candidates)
        dimensions = {"width": img.size[0], "height": img.size[1]}

        # Render the fullsize image
        fullfile = pathlib.Path(config.output, "gallery", "image", slug + ".png")
        image.save(img, fullfile, mkdirs=True)
        url = "image/{}.png".format(slug)

        # Create a scaled down version to use as a thumbnail on the main page
        thumb = img.copy()
        thumb.thumbnail((600, 600), PIL.Image.BICUBIC)
        thumbfile = pathlib.Path(config.output, "gallery", "thumb", slug + ".png")
        image.save(thumb, thumbfile, mkdirs=True)
        thumburl = "thumb/{}.png".format(slug)

        return cls(
            author=meta.author,
            cells=cells,
            created=created.strftime("%d %b %Y"),
            dimensions=dimensions,
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
class Site:

    baseurl: str
    """The base url the site will be hosted on."""

    notebooks: str
    """The path to the directory holding the notebooks."""

    output: str
    """The output directory to save the site to."""

    templates: str
    """The path to the directory containing the templates."""

    @classmethod
    def fromfile(cls, filepath):

        with open(filepath) as f:
            config = toml.parse(f.read())

        baseurl = config["site"]["baseurl"]
        templates = config["site"]["templates"]
        output = config["site"]["output"]

        notebooks = config["gallery"]["images"]

        return cls(
            baseurl=baseurl, notebooks=notebooks, output=output, templates=templates
        )

    def build(self, skip_failures=False, local=False):

        baseurl = "http://localhost:8001/" if local else self.baseurl

        env = j2.Environment(loader=j2.FileSystemLoader(self.templates))
        gallery_template = env.get_template("gallery.html")
        image_template = env.get_template("image.html")

        index = pathlib.Path(self.output, "gallery", "index.html")
        images = render_images(self.notebooks, self, skip_failures)

        context = {
            "site": {
                "arlunio_version": arlunio.__version__,
                "baseurl": baseurl,
                "date": datetime.now().strftime("%d/%m/%y %H:%M:%S"),
            }
        }

        # Shuffle the images so that the gallery is drawn in a random order
        # on each build.
        random.shuffle(images)

        # Render the main index page
        gallery = context.copy()
        gallery["images"] = images
        write_file(index, gallery_template.render(gallery))

        # For each image, render its detail page.
        for img in images:

            imgcontext = context.copy()
            imgcontext["image"] = img.as_dict()

            filename = pathlib.Path(self.output, "gallery", img.slug + ".html")
            write_file(filename, image_template.render(imgcontext))

        # Take the first image from the list as our example that can be linked from
        # the readme.
        example = pathlib.Path(self.output, "gallery", "image", images[0].slug + ".png")
        shutil.copy(example, example.parent / "_example.png")


def write_file(filepath, content):
    logger.debug("Writing file: %s", filepath)

    if not filepath.parent.exists():
        logger.debug("Creating dir: %s", filepath.parent)
        filepath.parent.mkdir(parents=True)

    with filepath.open("w") as f:
        f.write(content)


def render_images(nbdir, config, skip_failures=False) -> List[ImageContext]:
    """Discover and load and render each of the notebooks that represent images."""

    nbdir = pathlib.Path(nbdir)
    nbpaths = list(nbdir.glob("*.ipynb"))

    images = []
    errors = []

    print("Rendering Images ", end="", flush=True)
    for path in nbpaths:

        try:
            nb = NotebookLoader.fromfile(path)
            images.append(ImageContext.fromnb(nb, config))
            print(".", end="", flush=True)
        except Exception as err:

            if skip_failures:
                print("x", end="", flush=True)
                errors.append(f"{path} -- {err}")
                continue

            raise RuntimeError(f"Broken notebook {path}") from err

    print()

    if len(errors) > 0:
        print("Errors:", *errors, sep="\n")

    return images


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

    site = Site.fromfile(args.config)
    site.build(args.skip_failures)
