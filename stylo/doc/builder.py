import os
import typing

import attr
from docutils.nodes import Node
from sphinx.builders import Builder
from sphinx.util import logging

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class NotebookCell:
    """Represents a notebook cell."""

    cell_type: str
    execution_count: int = None
    metadata: typing.Dict[str, typing.Any] = attr.Factory(dict)
    outputs: typing.List[typing.Any] = attr.Factory(list)
    source: typing.List[str] = attr.Factory(list)

    @classmethod
    def code(cls):
        """Create a code cell type"""
        return cls("code")


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
        return attr.asdict(self)


class NotebookTutorialBuilder(Builder):
    """Builder that can convert static tutorials into an interactive jupyer
    notebook."""

    name = "nbtutorial"
    format = "ipynb"

    def init(self) -> None:
        """Any initialization goes here."""
        logger.info(f"[nbtutorial]: Outdir is: {self.outdir}")

    def get_outdated_docs(self) -> typing.Union[str, typing.Iterable[str]]:
        """Not too sure what we should do here yet."""

        return ""

    def get_target_uri(self, docname: str, typ: str = None) -> str:
        """Another method to figure out."""

        uri = docname + ".ipynb"

        logger.info(f"[nbtutorial]: Target URI: {uri}")

        return uri

    def prepare_writing(self, docnames: typing.Set[str]) -> None:
        """A place we can add logic to?"""
        pass

    def write_doc(self, docname: str, doctree: Node) -> None:
        logger.info(f"[nbtutorial]: Called on {docname}")
        logger.info(f"[nbtutorial]: Has doctree {doctree}")

        base, fname = os.path.split(docname)
        basedir = os.path.join(self.outdir, base)
        outfile = os.path.join(basedir, fname + ".ipynb")

        if not os.path.exists(basedir):
            os.makedirs(basedir)

        with open(outfile, "w") as f:
            f.write("A file exists.")
