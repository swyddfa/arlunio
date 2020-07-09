import os
import pathlib
import re
import shutil
import textwrap
from typing import Iterable
from typing import List
from typing import Set
from typing import Union

import docutils.nodes as nodes
import docutils.writers as writers
import nbformat.v4 as nbf
from docutils.io import StringOutput
from docutils.parsers import rst
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from sphinx.builders import Builder
from sphinx.util import logging
from sphinx.util.docutils import new_document

import arlunio
from .image import arlunio_image

logger = logging.getLogger(__name__)
RESOURCE_DIR = "resources"


class nbtutorial(nodes.General, nodes.Element):
    pass


def visit_nbtutorial(self, node):
    pass


def depart_nbtutorial(self, node):
    pass


class nbsolution(nodes.General, nodes.Element):
    pass


def visit_nbsolution(self, node):
    self.body.append('<details class="admonition note">\n')
    self.body.append(
        '<summary class="admonition-title">Solution (click to expand)</summary>\n'
    )


def depart_nbsolution(self, node):
    self.body.append("</details>\n")


class NBTutorialDirective(rst.Directive):
    def run(self):
        return [nbtutorial("")]


class NBSolutionDirective(BaseAdmonition):

    has_content = True
    node_class = nbsolution

    def run(self):
        (soln,) = super().run()
        return [soln]


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

    def _no_op(self, node):
        pass

    no_op = _no_op, _no_op

    visit_arlunio_image, depart_arlunio_image = no_op
    visit_compound, depart_compound = no_op
    visit_compact_paragraph, depart_compact_paragraph = no_op
    visit_document, depart_document = no_op
    visit_figure, depart_figure = no_op
    visit_legend, depart_legend = no_op
    visit_nbtutorial, depart_nbtutorial = no_op

    def _italics(self, node):
        self.current_cell.source += "*"

    italics = _italics, _italics

    visit_emphasis, depart_emphasis = italics
    visit_caption, depart_caption = italics

    def visit_bullet_list(self, node: nodes.bullet_list) -> None:
        self.new_cell("markdown")
        self.current_cell.source += "\n"

    def depart_bullet_list(self, node: nodes.bullet_list) -> None:
        self.current_cell.source += "\n"

    def visit_comment(self, node: nodes.comment) -> None:
        self.new_cell("markdown")

    def depart_comment(self, node: nodes.comment) -> None:
        pass

    def visit_image(self, node: nodes.image) -> None:
        self.new_cell("markdown")

        path = pathlib.Path(RESOURCE_DIR, pathlib.Path(node["uri"]).name)
        self.current_cell.source += f"\n![]({path})\n"

    def depart_image(self, node: nodes.image) -> None:
        pass

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

    def visit_nbsolution(self, node: nbsolution) -> None:
        self.new_cell("code")

    def depart_nbsolution(self, node: nbsolution) -> None:
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


class NotebookGalleryBuilder(Builder):
    """Builder that exports gallery images from the docs as a folder of notebooks."""

    name = "nbgallery"
    format = "ipynb"

    def init(self) -> None:
        logger.debug("[nbgallery]: Outdir: %s", self.outdir)

        # Standard metadata for exported notebooks.
        self.nbmeta = {
            "author": {"name": self.app.config.author,},
            "version": arlunio.__version__,
        }

        if self.app.config.arlunio_github_author is not None:
            self.nbmeta["author"]["github"] = self.app.config.arlunio_github_author

    def get_outdated_docs(self) -> Union[str, Iterable[str]]:
        """Not too sure what should put here yet."""
        return self.env.found_docs

    def get_target_uri(self, docname: str, type: str = None) -> str:
        return docname + ".ipynb"

    def prepare_writing(self, docnames: Set[str]):
        self.docwriter = NotebookWriter(self)

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        """Write out any gallery images on the given page."""

        logger.debug("[nbgallery]: Processing: %s", docname)
        images = [
            n for n in doctree.traverse(condition=arlunio_image) if "gallery" in n
        ]

        for image in images:

            gallery = image["gallery"]
            name = image["name"]

            code = nbf.new_code_cell(source=image["source"])
            caption = nbf.new_markdown_cell(source=image["caption"])

            metadata = {"arlunio": self.nbmeta}
            notebook = nbf.new_notebook(metadata=metadata, cells=[caption, code])

            outpath = pathlib.Path(self.outdir, gallery, name + ".ipynb")
            outpath.parent.mkdir(exist_ok=True)

            with outpath.open(mode="w") as f:
                logger.debug("[nbgallery]: Writing: %s", outpath)
                f.write(nbf.writes(notebook))


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

    def _process_solutions(
        self, docname: pathlib.Path, solutions: List[nbsolution]
    ) -> None:
        """Given the solutions for a given tutorial save them to the resources dir.

        This also rewrites the doctree so that the solutions are replaced by cells
        the :code:`%load` magic so that the user can load the results in.
        """
        logger.debug("[nbtutorial]: Processing solutions for %s", docname)

        if len(solutions) == 0:
            return

        soln_dir = pathlib.Path(self.outdir, docname.parent, RESOURCE_DIR)
        soln_name = docname.stem

        if not soln_dir.exists():
            soln_dir.mkdir(parents=True)

        for idx, soln in enumerate(solutions):
            logger.debug("[nbtutorial]: %s", soln)

            soln_fname = f"{soln_name}-{idx + 1:02d}.py"
            soln_path = soln_dir / soln_fname

            # We need to wrap solutions inside a document for some reason
            doc = new_document("")
            doc += soln

            # Convert the solution to a valid Python file
            translator = PythonTranslator(doc)
            doc.walkabout(translator)
            python_soln = translator.astext()

            # Insert a code block into the notebook that will load the solution
            soln.children = [
                codeblock(f"%load {soln_path.relative_to(soln_dir.parent)}")
            ]

            # Write the actual solution to the given file on disk
            soln_file = os.path.join(soln_dir, soln_fname)
            logger.debug("[nbtutorial]: --> %s", soln_path)

            with open(soln_file, "w") as f:
                f.write(python_soln)

    def _process_images(self, docname: pathlib.Path, images: List[nodes.image]) -> None:
        """Given the images for a given tutorial, save them to the resources dir."""
        logger.debug("[nbtutorial]: Processing images for %s", docname)

        if len(images) == 0:
            return

        img_dir = pathlib.Path(self.outdir, docname.parent, RESOURCE_DIR)

        if not img_dir.exists():
            img_dir.mkdir(parents=True)

        for img in images:
            fname = pathlib.Path(img["uri"]).name

            source = pathlib.Path(self.app.confdir, img["uri"])
            destination = pathlib.Path(img_dir, fname)

            shutil.copy(source, destination)

    def prepare_writing(self, docnames: Set[str]) -> None:
        """A place we can add logic to?"""
        self.docwriter = NotebookWriter(self)

    def write_doc(self, docname: str, doctree: nodes.Node) -> None:
        logger.debug(f"[nbtutorial]: Called on {docname}")

        # Determine if the document represents a tutorial.
        tutorial = list(doctree.traverse(condition=nbtutorial))

        if len(tutorial) == 0:
            return

        docname = pathlib.Path(docname)

        base, fname = docname.parent, docname.stem
        logger.debug("[nbtutorial]: Base: %s, Filename: %s", base, fname)
        basedir = pathlib.Path(self.outdir, base)

        if not basedir.exists():
            basedir.mkdir(parents=True)

        # Find and write out any solutions.
        solutions = list(doctree.traverse(condition=nbsolution))
        self._process_solutions(docname, solutions)

        # Find and copy over any images
        images = list(doctree.traverse(condition=nodes.image))
        self._process_images(docname, images)

        destination = StringOutput(encoding="utf-8")
        self.docwriter.write(doctree, destination)

        outfile = os.path.join(basedir, fname + ".ipynb")

        with open(outfile, "w") as f:
            f.write(self.docwriter.output)


def register(app):

    app.add_node(
        nbtutorial,
        html=(visit_nbtutorial, depart_nbtutorial),
        latex=(visit_nbtutorial, depart_nbtutorial),
        text=(visit_nbtutorial, depart_nbtutorial),
    )

    app.add_node(nbsolution, html=(visit_nbsolution, depart_nbsolution))

    app.add_builder(NotebookGalleryBuilder)
    app.add_builder(NotebookTutorialBuilder)

    app.add_config_value("arlunio_github_author", None, "env")

    app.add_directive("nbsolution", NBSolutionDirective)
    app.add_directive("nbtutorial", NBTutorialDirective)
