import os
import re
import textwrap

from pathlib import Path
from typing import Iterable, List, Set, Union

import docutils.nodes as nodes
import docutils.writers as writers
import nbformat.v4 as nbf

from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util import logging

from .directives import nbsolution, nbtutorial

logger = logging.getLogger(__name__)


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
    """Converts rst nodes into their output representation."""

    def __init__(self, document):
        super().__init__(document)
        self.cells = []
        self.level = 0
        self.prefix = None

    def asnotebook(self):
        return nbf.new_notebook(cells=self.cells)

    @property
    def current_cell(self):

        if len(self.cells) == 0:
            return None

        return self.cells[-1]

    def new_cell(self, cell_type: str) -> None:
        current = self.current_cell

        if current is not None and current.cell_type == cell_type:
            return

        types = {"markdown": nbf.new_markdown_cell, "code": nbf.new_code_cell}
        new_cell = types[cell_type]
        self.cells.append(new_cell())

    def append(self, text):

        if self.prefix is not None:
            text = text.replace("\n", "\n" + self.prefix)

            self.current_cell.source += text
            return

        self.current_cell.source += text

    def astext(self):
        notebook = nbf.new_notebook(cells=self.cells)
        return nbf.writes(notebook)

    # --------------------------- Visitors ------------------------------------

    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        self.new_cell("markdown")

    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        pass

    def visit_compound(self, node: nodes.compound) -> None:
        pass

    def depart_compound(self, node: nodes.compound) -> None:
        pass

    def visit_compact_paragraph(self, node) -> None:
        pass

    def depart_compact_paragraph(self, node) -> None:
        pass

    def visit_comment(self, node: nodes.comment) -> None:
        self.new_cell("markdown")

    def depart_comment(self, node: nodes.comment) -> None:
        pass

    def visit_document(self, node: nodes.document) -> None:
        pass

    def depart_document(self, node: nodes.document) -> None:
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
        self.append("- ")

    def depart_list_item(self, node: nodes.list_item) -> None:
        pass

    def visit_literal(self, node: nodes.literal) -> None:
        self.current_cell.source += "`"

    def depart_literal(self, node: nodes.literal) -> None:
        self.current_cell.source += "`"

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        self.new_cell("code")

    def depart_literal_block(self, node: nodes.literal_block) -> None:
        pass

    def visit_nbtutorial(self, node: nbtutorial) -> None:
        pass

    def depart_nbtutorial(self, node: nbtutorial) -> None:
        pass

    def visit_note(self, node: nodes.note) -> None:
        self.new_cell("markdown")
        self.append("> **Note**\n")
        self.prefix = "> "

    def depart_note(self, node: nodes.note) -> None:
        self.prefix = None

    def visit_paragraph(self, node: nodes.paragraph) -> None:
        self.new_cell("markdown")

        if isinstance(node.parent, nodes.list_item):
            return

        self.append("\n")

    def depart_paragraph(self, node: nodes.paragraph) -> None:
        self.append("\n")

    def visit_reference(self, node: nodes.reference) -> None:
        self.append("[")

    def depart_reference(self, node: nodes.reference) -> None:
        attrs = node.attributes

        url = attrs["refuri"]
        self.append(f"]({url})")

    def visit_section(self, node: nodes.section) -> None:
        self.level += 1
        self.new_cell("markdown")

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

        if isinstance(node.parent, nodes.comment):
            return

        if self.current_cell.cell_type == "markdown":
            self.append(node.astext())
            return

        source = node.astext()

        if ">>>" not in source:
            self.append(source)
            return

        pattern = re.compile("^(>>>|\\.\\.\\.) ?")

        def clean_line(line):
            return pattern.sub("", line)

        cleaned_source = "\n".join(
            [clean_line(line) for line in source.split("\n") if pattern.match(line)]
        )

        self.append(cleaned_source)

    def depart_Text(self, node: nodes.Text) -> None:
        pass

    def visit_title(self, node: nodes.title) -> None:
        title = "#" * self.level
        self.append(f"{title} ")

    def depart_title(self, node: nodes.title) -> None:
        self.append("\n")


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

    def _process_solutions(self, docname: str, solutions: List[nbsolution]) -> None:
        """Given the solutions for a given tutorial save them to the solutions dir.

        This also rewrites the doctree so that the solutions are replaced by cells
        the :code:`%load` magic so that the user can load the results in.
        """
        logger.debug("[nbtutorial]: Processing solutions for %s", docname)

        DIRNAME = "solutions"
        soln_dir = os.path.join(self.outdir, os.path.dirname(docname), DIRNAME)
        soln_name = os.path.basename(docname)

        if not os.path.exists(soln_dir):
            os.makedirs(soln_dir)

        for idx, soln in enumerate(solutions):
            soln_fname = f"{soln_name}-{idx + 1:02d}.py"
            soln_path = os.path.join(DIRNAME, soln_fname)

            # Convert the solution to a valid Python file
            translator = PythonTranslator(soln)
            soln.walkabout(translator)
            python_soln = translator.astext()

            # Insert a code block into the notebook that will load the solution
            soln.children = [codeblock(f"%load {soln_path}")]

            # Write the actual solution to the given file on disk
            soln_file = os.path.join(soln_dir, soln_fname)
            logger.debug("[nbtutorial]: --> %s", soln_path)

            with open(soln_file, "w") as f:
                f.write(python_soln)

    def prepare_writing(self, docnames: Set[str]) -> None:
        """A place we can add logic to?"""

        self.docwriter = NotebookWriter(self)

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        logger.debug(f"[nbtutorial]: Called on {docname}")

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
