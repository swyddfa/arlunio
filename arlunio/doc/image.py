import pathlib
import textwrap
import traceback
from typing import List
from typing import Optional

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure
from docutils.statemachine import StringList
from sphinx.util import logging
from sphinx.util.nodes import nested_parse_with_titles

import arlunio.image as image


class Count:
    def __init__(self):
        self.i = 0

    def __call__(self):
        self.i += 1
        return self.i


class arlunio_image(nodes.General, nodes.Element):
    pass


def visit_arlunio_image(self, node):
    pass


def depart_arlunio_image(self, node):
    pass


def parse_content(state, content: StringList) -> List[nodes.Node]:
    """Given a reStructured text representation of some content format parse it
    into a list of nodes."""

    section = nodes.section()
    section.document = state.document
    nested_parse_with_titles(state, content, section)

    return section.children


def reformat_content(
    caption: str, code: str, include_code: Optional[str]
) -> StringList:
    """Reformat the content of the arlunio-image directive so that it's compatible with
    the standard figure directive."""

    count = Count()
    src = "<arlunio_image>"
    indent = "   "

    content = StringList()
    content.append(caption, src, count())
    content.append("", src, count())

    if include_code is not None:
        level = 0

        if include_code == "solution":
            content.append(".. nbsolution::", src, count())
            content.append("", src, count())

            level += 1

        codeblock = textwrap.indent(".. code-block:: python", indent * level)
        content.append(codeblock, src, count())
        content.append("", src, count())

        level += 1

        for line in code.splitlines():
            line = textwrap.indent(line, indent * level)
            content.append(line, src, count())

    return content


def find_caption(doctree: List[nodes.Node]) -> str:
    """Given the doctree representing the content of the arlunio-image directive
    find and return the text representing the caption (if any)."""

    logger = logging.getLogger(__name__)
    text = ".."

    if len(doctree) > 0 and isinstance(doctree[0], nodes.paragraph):
        text = doctree[0].astext()
        logger.debug("[arlunio-image]: Found caption text '%s'", text)

    return text


def find_code(doctree: List[nodes.Node]) -> str:
    """Given the doctree representing the content of the arlunio-image directive
    find and return the source code for the image (if any)."""

    logger = logging.getLogger(__name__)
    logger.debug("[arlunio-image] doctree: %s", doctree)
    candidates = [n for n in doctree if isinstance(n, nodes.literal_block)]

    if len(candidates) == 0:
        raise ValueError("Missing image code.")

    if len(candidates) > 1:
        raise ValueError("Multiple code blocks is not supported.")

    code = candidates[0].astext()
    logger.debug("[arlunio-image]: Found source code: %s...", code[: code.find("\n")])

    return code


def render_image(src: str, name: str, outdir: pathlib.Path) -> pathlib.Path:
    """Given the source code for an image, render it and save it to file.

    Parameters
    ----------
    src:
        The code that produces the image
    name:
        The name of the image
    outdir:
        Where the image should be saved.

    Return
    ------
    The path to the image, relative to the root of the Sphinx project
    """
    env = {}
    logger = logging.getLogger(__name__)

    code = compile(src, "<string>", "exec")
    exec(code, env)

    img = None

    for obj in env.values():
        if isinstance(obj, image.Image):
            img = obj

    if img is None:
        raise ValueError("Code did not produce a valid image.")

    outfile = pathlib.Path("_images", name + ".png")
    logger.debug("[arlunio-image] Saving image to: %s", outfile)

    image.save(img, pathlib.Path(outdir, outfile), mkdirs=True)

    return outfile


class ArlunioImageDirective(Figure):
    """Given some code that produces an image, render it in the page."""

    has_content = True
    final_argument_whitespace = True

    def inccode(arg):
        arg = "" if arg is None else arg
        return directives.choice(arg, ("", "solution"))

    option_spec = Figure.option_spec.copy()
    option_spec["gallery"] = directives.unchanged
    option_spec["include-code"] = inccode

    def run(self):

        logger = logging.getLogger(__name__)

        imgname = self.arguments[0]
        imgpath = imgname.lower().replace(" ", "-")

        logger.debug("[arlunio-image]: Rendering: %s", imgname)
        include_code = self.options.pop("include-code", None)

        # First we will process the content of the directive in order to produce an
        # image on disk. We will then defer to the default behavior of the Figure
        # directive to handle the rest.
        app = self.state.document.settings.env.app

        doctree = parse_content(self.state, self.content)
        caption = find_caption(doctree)

        try:
            src = find_code(doctree)
            imguri = render_image(src, imgpath, app.confdir)
        except Exception:
            tback = traceback.format_exc()

            # Flag the issue to the user to the issue in the log
            location = self.state_machine.get_source_and_line(self.lineno)
            logger.warning("Unable to render image\n%s", tback, location=location)

            # But also make the error obvious in the docs.
            message = nodes.Text("Unable to render image:")
            err = nodes.literal_block("", tback)

            return [nodes.error("", message, err)]

        # Rewrite the arguments list to contain the reference to the image file
        self.arguments[0] = "/" + str(imguri)

        # Rewrite the content according to the given options.
        content = reformat_content(caption, src, include_code)

        self.content_offset = 0
        self.content = content

        # Now defer to the standard figure implementation.
        (figure,) = Figure.run(self)
        logger.debug("[arlunio-image]: Figure: %s", figure)

        opts = {k: v for k, v in self.options.items() if k in ("gallery",)}
        opts["source"] = src
        opts["name"] = imgname
        opts["caption"] = caption

        return [arlunio_image("", figure, **opts)]


def register(app):

    app.add_node(
        arlunio_image,
        html=(visit_arlunio_image, depart_arlunio_image),
        latex=(visit_arlunio_image, depart_arlunio_image),
        text=(visit_arlunio_image, depart_arlunio_image),
    )

    app.add_directive("arlunio-image", ArlunioImageDirective)
