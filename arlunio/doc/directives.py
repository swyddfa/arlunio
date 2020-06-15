from typing import List

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.statemachine import StringList
from sphinx.util import logging
from sphinx.util import nested_parse_with_titles


logger = logging.getLogger(__name__)


class nbtutorial(nodes.General, nodes.Element):
    pass


def visit_nbtutorial(self, node):
    pass


def depart_nbtutorial(self, node):
    pass


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
