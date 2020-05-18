import string
import textwrap
import traceback

from typing import List, Tuple

import arlunio.lib.image as img

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import StringList
from PIL.Image import Image
from sphinx.util import logging, nested_parse_with_titles

logger = logging.getLogger(__name__)


ERROR_TEMPLATE = """\
.. error::

${message}

${traceback}
"""

PREVIEW_TEMPLATE = """\
.. raw:: html

   <figure>
     <img alt="${alt_tag}"
          src="data:image/png;base64,${img_data}"
          style="border: solid 1px #ddd"/>
     <figcaption style="margin: 10px;text-align:center">
       <small style="font-style:italic">${alt_tag}</small>
     </figcaption>
   </figure>

"""

IMAGE_TEMPLATE = string.Template(
    """\
<figure style="border: solid 1px #ddd;margin:auto">
  <img style="image-rendering:$rendering;width:100%"
       src="data:image/png;base64,$data"></img>
</figure>
"""
)


class nbtutorial(nodes.General, nodes.Element):
    pass


def visit_nbtutorial(self, node):
    pass


def depart_nbtutorial(self, node):
    pass


def format_error(message: str, err: str) -> StringList:
    """Given an error message format it as an error."""

    indent = " " * 3
    msg = textwrap.indent(message + "::", indent)
    err_msg = textwrap.indent(err, indent * 2)

    template = string.Template(ERROR_TEMPLATE)
    error = template.safe_substitute({"message": msg, "traceback": err_msg})

    return StringList(error.split("\n"), source="")


def parse_content(state, content: StringList) -> List[nodes.Node]:
    """Given a reStructured text representation of some content format parse it
    into a list of nodes."""

    section = nodes.section()
    section.document = state.document
    nested_parse_with_titles(state, content, section)

    return section.children


def render_image(
    src: str, smooth: bool = True, location: Tuple[str, int] = None
) -> List[nodes.Node]:
    """Given the source code for an image return a doctree that when rendered by
    Sphinx will insert that image into a HTML page.

    Parameters
    ----------
    src:
        The source code that produces the image.
    smooth:
        If :code:`True` (default) allow the browser to scale the image using an
        algorithm that smooths out the edges of the image.
    """
    doctree = []
    environment = {}

    try:
        code = compile(src, "<string>", "exec")
        exec(code, environment)
    except Exception:
        tback = traceback.format_exc()

        # Flag the issue to the user to the issue in the log
        logger.warning("Unable to render image\n%s", tback, location=location)

        # But also make the error obvious in the docs.
        message = nodes.Text("Unable to render image: Error in code")
        err = nodes.literal_block("", tback)
        doctree.append(nodes.error("", message, err))

        return doctree

    image = None

    for obj in environment.values():
        if isinstance(obj, Image):
            image = obj

    if image is not None:
        context = {
            "data": img.encode(image).decode("utf-8"),
            "rendering": "auto" if smooth else "crisp-edges",
        }
        html = IMAGE_TEMPLATE.safe_substitute(context)
        doctree.append(nodes.raw("", html, format="html"))

    return doctree


class NBTutorialDirective(rst.Directive):
    def run(self):
        return [nbtutorial("")]


class nbsolution(nodes.General, nodes.Element):
    pass


def visit_nbsolution(self, node):
    self.body.append('<details class="admonition note">\n')
    self.body.append(
        '<summary class="admonition-title">Solution (click to expand)</summary>\n'
    )


def depart_nbsolution(self, node):
    self.body.append("</details>\n")


class NBSolutionDirective(BaseAdmonition):

    has_content = True
    node_class = nbsolution

    def run(self):
        (soln,) = super().run()
        return [soln]


class ArlunioImageDirective(rst.Directive):
    """Given some code that produces an image, render it in the page."""

    has_content = True

    option_spec = {
        "include-code": rst.directives.unchanged,
        "disable-smoothing": rst.directives.flag,
    }

    def run(self):

        src = "\n".join(self.content)
        smooth = not ("disable-smoothing" in self.options.keys())

        location = self.state_machine.get_source_and_line(self.lineno)
        nodelist = render_image(src, smooth, location=location)

        if "include-code" in self.options.keys():

            code_block = nodes.literal_block("", src)
            code_block["language"] = "python"

            if self.options["include-code"] == "before":
                nodelist.insert(0, code_block)
            else:
                nodelist.append(code_block)

        return nodelist
