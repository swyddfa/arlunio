"""Import utilities.

This module defines a number of classes that allow us to extend Python's import
machinery to support more than just regular Python files. Currently this includes
support for the following formats.

- .ipynb - Jupyter Notebooks

Note: The code that adds support for Jupyter Notebooks is heavily based on code
originally found in the documentation.

https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html
"""
import logging
import os

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader

import nbformat

from IPython.core.interactiveshell import InteractiveShell

logger = logging.getLogger(__name__)


def find_notebook(fullname, path=None):
    """Converts a.b.c into a valid filepath and checks to see if it exists."""

    name = fullname.rsplit(".", 1)[-1]
    path = [""] if not path else path

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
    """This does the legwork of importing a notebook.

    Note: It's not currently clear when all the various loaders should be used so we're
    sticking with a vanilla Loader for now.
    """

    def __init__(self, path=None):
        self.path = path
        self.shell = InteractiveShell.instance()
        self.shell.enable_gui = lambda x: False

    def exec_module(self, module):
        module.__file__ = find_notebook(module.__name__, self.path)

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


class NotebookFinder(MetaPathFinder):
    """Responsible for checking a path to see if it "looks like a notebook".

    If we think we can handle a given path then we should return a loader capable of
    processing it.

    Note: It's not currently clear what the difference is between MetaPathFinder and
    PathEntryFinder, currently implementing the MetaPathFinder interface since it seems
    to work correctly.
    """

    def __init__(self):
        self.loaders = {}

    def find_spec(self, fullname, path, target=None):

        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = os.path.sep.join(path) if path else path
        logger.debug("key: %s", key)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)

        loader = self.loaders[key]
        return spec_from_loader(fullname, loader)
