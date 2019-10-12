import json
import os
import re
import typing

from pathlib import Path

import attr
import docutils.nodes as nodes
import docutils.writers as writers

from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .directives import nbtutorial

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class NotebookCell:
    """Represents a notebook cell."""

    CODE: typing.ClassVar[str] = "code"
    MARKDOWN: typing.ClassVar[str] = "markdown"

    cell_type: str
    execution_count: int = None
    metadata: typing.Dict[str, typing.Any] = attr.Factory(dict)
    outputs: typing.List[typing.Any] = attr.Factory(list)
    source: str = attr.Factory(str)

    @classmethod
    def code(cls):
        """Create a code cell type"""
        return cls(cls.CODE)

    @classmethod
    def markdown(cls):
        """Create a markdown cell"""
        return cls(cls.MARKDOWN)

    @property
    def json(self):
        cell = attr.asdict(self)
        cell["source"] = [line + "\n" for line in cell["source"].split("\n")]

        md_exclude = {"outputs", "execution_count"}

        def exclude(field):
            return self.cell_type == self.MARKDOWN and field in md_exclude

        return {k: v for k, v in cell.items() if not exclude(k)}


@attr.s(auto_attribs=True)
class Notebook:
    """Represents a notebook."""

    nbformat: int = 4
    nbformat_minor: int = 2
    metadata: typing.Dict[str, typing.Any] = attr.Factory(dict)
    cells: typing.List[NotebookCell] = attr.Factory(list)

    @classmethod
    def fromcells(cls, cells: typing.List[NotebookCell]):
        return cls(cells=cells)

    @property
    def json(self):
        notebook = attr.asdict(self)
        cells = [c.json for c in self.cells]

        notebook["cells"] = cells
        return notebook


class NotebookWriter(writers.Writer):
    """A class that walks a doctree converting it into a notebook."""

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    def translate(self):

        visitor = NotebookTranslator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.astext()


class NotebookTranslator(SphinxTranslator):
    """Converts rst nodes into their output representation."""

    def __init__(self, document, builder):
        super().__init__(document, builder)
        self.cells = []
        self.level = 0

    @property
    def current_cell(self):

        if len(self.cells) == 0:
            return None

        return self.cells[-1]

    def new_cell(self, cell_type: str) -> None:
        current = self.current_cell

        if current is None or current.cell_type != cell_type:
            cell = NotebookCell(cell_type=cell_type)
            self.cells.append(cell)

    def _log_visit(self, node: nodes.Node, surround: str = None) -> None:
        prefix = self.level * " " + "-> "
        name = node.__class__.__name__

        if surround is not None:
            name = surround + name + surround

        logger.debug(prefix + name)

    def _log_departure(self, node: nodes.Node) -> None:
        pass

    def astext(self):
        notebook = Notebook.fromcells(self.cells)
        return json.dumps(notebook.json, indent=2)

    def visit_section(self, node: nodes.section) -> None:
        self.level += 1
        self._log_visit(node)
        self.new_cell(NotebookCell.MARKDOWN)

    def depart_section(self, node: nodes.section) -> None:
        self.level -= 1
        self._log_departure(node)

    def visit_Text(self, node: nodes.Text) -> None:
        self._log_visit(node)

        if self.current_cell.cell_type == NotebookCell.MARKDOWN:
            self.current_cell.source += node.astext()
            return

        source = node.astext()

        if ">>>" not in source:
            self.current_cell.source += source
            return

        pattern = re.compile("^(>>>|\\.\\.\\.) ?")

        def clean_line(line):
            return pattern.sub("", line)

        cleaned_source = "\n".join(
            [clean_line(line) for line in source.split("\n") if pattern.match(line)]
        )

        self.current_cell.source += cleaned_source

    def depart_Text(self, node: nodes.Text) -> None:
        self._log_departure(node)

    def visit_title(self, node: nodes.title) -> None:
        self._log_visit(node)

        title = "#" * self.level
        self.current_cell.source += f"\n{title} "

    def depart_title(self, node: nodes.title) -> None:
        self._log_departure(node)
        self.current_cell.source += "\n"

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        self._log_visit(node)
        self.new_cell(NotebookCell.MARKDOWN)
        self.current_cell.source += "\n"

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        self._log_departure(node)
        self.current_cell.source += "\n"

    def visit_strong(self, node: nodes.strong) -> None:
        self._log_visit(node)
        self.current_cell.source += "**"

    def depart_strong(self, node: nodes.strong) -> None:
        self._log_departure(node)
        self.current_cell.source += "**"

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        self._log_visit(node)
        self.new_cell(NotebookCell.CODE)

    def depart_literal_block(self, node: nodes.literal_block) -> None:
        self._log_departure(node)

    def visit_literal(self, node: nodes.literal) -> None:
        self._log_visit(node)
        self.current_cell.source += "`"

    def depart_literal(self, node: nodes.literal) -> None:
        self.current_cell.source += "`"

    def visit_list_item(self, node: nodes.list_item) -> None:
        self.current_cell.source += "- "

    def visit_target(self, node: nodes.target) -> None:
        pass

    def visit_reference(self, node: nodes.reference) -> None:
        pass

    def depart_reference(self, node: nodes.reference) -> None:
        attrs = node.attributes

        if attrs["internal"]:
            ref = attrs["refuri"].split("#")[0]
            self.current_cell.source += f"({ref})"

    def visit_inline(self, node: nodes.inline) -> None:
        self.current_cell.source += "["

    def depart_inline(self, node: nodes.inline) -> None:
        self.current_cell.source += "]"

    def unknown_visit(self, node: nodes.Node):
        self._log_visit(node, surround="!")

    def unknown_departure(self, node):
        self._log_departure(node)


class NotebookTutorialBuilder(Builder):
    """Builder that can convert static tutorials into an interactive jupyer
    notebook."""

    name = "nbtutorial"
    format = "ipynb"

    def init(self) -> None:
        """Any initialization goes here."""
        logger.debug(f"[nbtutorial]: Outdir is: {self.outdir}")

    def get_outdated_docs(self) -> typing.Union[str, typing.Iterable[str]]:
        """Not too sure what we should do here yet."""

        return ""

    def get_target_uri(self, docname: str, typ: str = None) -> str:
        """Another method to figure out."""

        uri = docname + ".ipynb"

        logger.debug(f"[nbtutorial]: Target URI: {uri}")

        return uri

    def prepare_writing(self, docnames: typing.Set[str]) -> None:
        """A place we can add logic to?"""

        self.docwriter = NotebookWriter(self)

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        logger.debug(f"[nbtutorial]: Called on {docname}")

        # Determine if the document represents a tutorial.
        nodes = list(doctree.traverse(condition=nbtutorial))

        if len(nodes) == 0:
            return

        destination = StringOutput(encoding="utf-8")
        self.docwriter.write(doctree, destination)

        base, fname = os.path.split(docname)
        basedir = os.path.join(self.outdir, base)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

        Path(basedir, "__init__.py").touch()
        outfile = os.path.join(basedir, fname + ".ipynb")

        with open(outfile, "w") as f:
            f.write(self.docwriter.output)
