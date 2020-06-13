import string
import textwrap
from typing import List

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import StringList
from sphinx.util import logging
from sphinx.util import nested_parse_with_titles


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
