"""Extensions to Python's import machinery to support more than just regular Python
files. Currently includes support for the following formats.

- :code:`.ipynb`: Jupyter Notebooks
"""
import importlib.util as imutil
import logging
import os
import pathlib
from importlib.abc import Loader
from importlib.abc import MetaPathFinder

import nbformat
from IPython.core.interactiveshell import InteractiveShell

logger = logging.getLogger(__name__)

# Notebook implementation based on
# https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html


def _find_notebook(fullname, path=None):
    """Converts a.b.c into a valid filepath and checks to see if it exists."""

    name = fullname.rsplit(".", 1)[-1]

    if path is None:
        path = [""]

    if isinstance(path, str):
        path = [path]

    logger.debug("path: %s", path)

    for dir in path:
        nb_path = os.path.join(dir, name + ".ipynb")
        logger.debug("Trying %s", nb_path)

        if os.path.isfile(nb_path):
            return nb_path

        nb_path = nb_path.replace("_", " ")
        logger.debug("Trying %s", nb_path)

        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(Loader):
    """This does the legwork of importing a notebook."""

    # Note: It's not currently clear when all the various loaders should be used so
    # sticking with a vanilla Loader for now.

    def __init__(self, path=None):
        self.path = path
        self.shell = InteractiveShell.instance()
        self.shell.enable_gui = lambda x: False

    def exec_module(self, module):
        module.__file__ = _find_notebook(module.__name__, self.path)

        with open(module.__file__, "r", encoding="utf-8") as f:
            # Read notebook using v4 of the spec
            notebook = nbformat.read(f, 4)
            module.__notebook__ = notebook

        for cell in notebook.cells:
            if cell.cell_type == "code":

                # Transform any magics into python code.
                src = cell.source
                code = self.shell.input_transformer_manager.transform_cell(src)
                exec(code, module.__dict__)

    @classmethod
    def fromfile(cls, filepath: str):
        """Import a Jupyter Notebook directly from a filepath."""
        nbpath = pathlib.Path(filepath)
        logger.debug("Importing notebook: %s", filepath)

        if not nbpath.exists():
            raise FileNotFoundError(nbpath)

        nbname = nbpath.stem.replace(" ", "_")
        loader = cls(str(nbpath.parent))

        spec = imutil.spec_from_file_location(nbname, str(nbpath), loader=loader)
        module = imutil.module_from_spec(spec)

        logger.debug("--> spec: %s", spec)
        logger.debug("--> module: %s", module)

        spec.loader.exec_module(module)

        return module


class NotebookFinder(MetaPathFinder):
    """Responsible for checking a path to see if it "looks like a notebook"."""

    # Note: It's not currently clear what the difference is between MetaPathFinder and
    # PathEntryFinder, currently implementing the MetaPathFinder interface since it
    # seems to work correctly.

    def __init__(self):
        self.loaders = {}

    def find_spec(self, fullname, path, target=None):

        nb_path = _find_notebook(fullname, path)
        if not nb_path:
            return

        key = os.path.sep.join(path) if path else path
        logger.debug("key: %s", key)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)

        loader = self.loaders[key]
        return imutil.spec_from_loader(fullname, loader)
