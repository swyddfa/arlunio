import json
import os
import re
import textwrap
import typing

from pathlib import Path
from typing import Any, ClassVar, Dict, Iterable, List, Set, Union

import attr
import docutils.nodes as nodes
import docutils.writers as writers

from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util import logging

from .directives import nbsolution, nbtutorial

# from sphinx.util.docutils import SphinxTranslator


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class NotebookCell:
    """Represents a notebook cell."""

    CODE: ClassVar[str] = "code"
    MARKDOWN: ClassVar[str] = "markdown"

    cell_type: str
    execution_count: int = None
    metadata: Dict[str, Any] = attr.Factory(dict)
    outputs: List[Any] = attr.Factory(list)
    source: str = attr.Factory(str)

    @classmethod
    def code(cls, source=None):
        """Create a code cell type"""

        cell = cls(cls.CODE)

        if source is not None:
            cell.source = source

        return cell

    @classmethod
    def markdown(cls, source=None):
        """Create a markdown cell"""

        cell = cls(cls.MARKDOWN)

        if source is not None:
            cell.source = source

        return cell

    @property
    def json(self):
        cell = attr.asdict(self)
        cell["source"] = [line + "\n" for line in cell["source"].split("\n")]

        md_exclude = {"outputs", "execution_count"}

        def exclude(field):
            return self.cell_type == self.MARKDOWN and field in md_exclude

        return {k: v for k, v in cell.items() if not exclude(k)}


def notebook_metadata():
    """Return the default metadata for a notebook."""
    return {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }
    }


@attr.s(auto_attribs=True)
class Notebook:
    """Represents a notebook."""

    nbformat: int = 4
    nbformat_minor: int = 2
    metadata: Dict[str, Any] = attr.Factory(notebook_metadata)
    cells: List[NotebookCell] = attr.Factory(list)

    @classmethod
    def fromcells(cls, cells: List[NotebookCell]):
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

        visitor = NotebookTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()


class PythonTranslator(nodes.NodeVisitor):
    """Coverts an rst doctree into a valid python file.

    Currently only used to write tutorial solutions to a python file that can be
    imported via the `%load` magic in a jupyter notebook.
    """

    def __init__(self, document):
        super().__init__(document)
        self.is_code = False
        self.source = ""

    def astext(self):
        return self.source

    # ------------------------- Visitors --------------------------------------

    def visit_Text(self, node: nodes.Text) -> None:
        source = node.astext()
        self.source += textwrap.indent(source, "# " * self.is_code)

    def depart_Text(self, node: nodes.Text) -> None:
        pass

    def unknown_visit(self, node: nodes.Node) -> None:
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        pass


class NotebookTranslator(nodes.NodeVisitor):
    """Converts an rst doctree into our representation of a jupyter notebook."""

    def __init__(self, document):
        super().__init__(document)
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

    def asdict(self):
        notebook = Notebook.fromcells(self.cells)
        return notebook.json

    # ----------------------- Visitors ----------------------------------------

    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        self.new_cell(NotebookCell.MARKDOWN)

    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        pass

    def visit_emphasis(self, node: nodes.emphasis) -> None:
        self.current_cell.source += "*"

    def depart_emphasis(self, node: nodes.emphasis) -> None:
        self.current_cell.source += "*"

    def visit_inline(self, node: nodes.inline) -> None:
        self.current_cell.source += "["

    def depart_inline(self, node: nodes.inline) -> None:
        self.current_cell.source += "]"

    def visit_list_item(self, node: nodes.list_item) -> None:
        self.current_cell.source += "- "

    def depart_list_item(self, node: nodes.list_item) -> None:
        pass

    def visit_literal(self, node: nodes.literal) -> None:
        self.current_cell.source += "`"

    def depart_literal(self, node: nodes.literal) -> None:
        self.current_cell.source += "`"

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        self.new_cell(NotebookCell.CODE)

    def depart_literal_block(self, node: nodes.literal_block) -> None:
        pass

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        self.new_cell(NotebookCell.MARKDOWN)

        if isinstance(node.parent, nodes.list_item):
            return

        self.current_cell.source += "\n"

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        self.current_cell.source += "\n"

    def visit_reference(self, node: nodes.reference) -> None:
        self.current_cell.source += "["

    def depart_reference(self, node: nodes.reference) -> None:
        attrs = node.attributes

        url = attrs["refuri"]
        self.current_cell.source += f"]({url})"

    def visit_section(self, node: nodes.section) -> None:
        self.level += 1
        self.new_cell(NotebookCell.MARKDOWN)

    def depart_section(self, node: nodes.section) -> None:
        self.level -= 1

    def visit_strong(self, node: nodes.strong) -> None:
        self.current_cell.source += "**"

    def depart_strong(self, node: nodes.strong) -> None:
        self.current_cell.source += "**"

    def visit_target(self, node: nodes.target) -> None:
        pass

    def depart_target(self, node: nodes.target) -> None:
        pass

    def visit_Text(self, node: nodes.Text) -> None:

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
        pass

    def visit_title(self, node: nodes.title) -> None:
        title = "#" * self.level
        self.current_cell.source += f"\n{title} "

    def depart_title(self, node: nodes.title) -> None:
        self.current_cell.source += "\n"

    def unknown_visit(self, node: nodes.Node) -> None:
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        pass


def codeblock(source: str) -> nodes.literal_block:
    """Construct a valid code block."""

    block = nodes.literal_block()
    block.children = [nodes.Text(source)]

    return block


class NotebookTutorialBuilder(Builder):
    """Builder that can convert static tutorials into an interactive jupyer
    notebook."""

    name = "nbtutorial"
    format = "ipynb"

    def init(self) -> None:
        """Any initialization goes here."""
        logger.debug(f"[nbtutorial]: Outdir is: {self.outdir}")

    def get_outdated_docs(self) -> Union[str, Iterable[str]]:
        """Not too sure what we should do here yet."""

        return self.env.found_docs

    def get_target_uri(self, docname: str, type: str = None) -> str:
        """Another method to figure out."""

        uri = docname + ".ipynb"

        logger.debug(f"[nbtutorial]: Target URI: {uri}")

        return uri

    def prepare_writing(self, docnames: Set[str]) -> None:
        """A place we can add logic to?"""

        self.docwriter = NotebookWriter(self)

    def _process_solutions(self, docname: str, solutions: List[nbsolution]) -> None:
        """Given the solutions for a given tutorial save them to the solutions dir.

        This also rewrites the doctree so that the solutions are replace by cells
        the :code:`%load` magic so that the user can load the results in.
        """
        logger.debug(f"[nbtutorial]: Processing solutions for {docname}")

        DIRNAME = "solutions"
        soln_dir = os.path.join(self.outdir, os.path.dirname(docname), DIRNAME)
        soln_name = os.path.basename(docname)

        if not os.path.exists(soln_dir):
            os.makedirs(soln_dir)

        for idx, soln in enumerate(solutions):
            soln_fname = f"{soln_name}-{idx + 1:02d}.py"
            soln_path = f"{DIRNAME}/{soln_fname}"

            # Convert the solution to a valid python file
            translator = PythonTranslator(soln)
            soln.walkabout(translator)
            python_soln = translator.astext()

            # Insert a code block into the notebook that will load the solution
            soln.children = [codeblock(f"%load {soln_path}")]

            # Write the actual solution to the given file on disk.
            soln_file = os.path.join(soln_dir, soln_fname)
            logger.debug(f"[nbtutorial]: --> {soln_file}")

            with open(soln_file, "w") as f:
                f.write(python_soln)

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        logger.debug(f"[nbtutorial]: Processing {docname}")

        # Determine if the document represents a tutorial.
        nodes = list(doctree.traverse(condition=nbtutorial))

        if len(nodes) == 0:
            return

        # Find any solutions that it may constain.
        solutions = list(doctree.traverse(condition=nbsolution))
        self._process_solutions(docname, solutions)

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
