import math

import py.test

from arlunio.imp import NotebookLoader


def test_notebook_loader_simple(testdata):
    """Ensure that we can load a simple notebook that only contains code cells"""

    nbpath = testdata("Add.ipynb", path_only=True)
    notebook = NotebookLoader.fromfile(nbpath)

    assert 3 == notebook.add(1, 2)


def test_notebook_loader(testdata):
    """Ensure that we can load a notebook that contains a mixture of cell types."""

    nbpath = testdata("Pythagoras.ipynb", path_only=True)
    notebook = NotebookLoader.fromfile(nbpath)

    assert 5 == math.sqrt(notebook.pythagoras(3, 4))


def test_notebook_loader_metadata(testdata):
    """Ensure that we can access a notebook's metadata"""

    nbpath = testdata("Metadata.ipynb", path_only=True)
    notebook = NotebookLoader.fromfile(nbpath)

    assert 6 == notebook.add(1, 2, 3)

    assert [1920, 1080] == notebook.__notebook__.metadata.arlunio.dimensions
    assert "Alex" == notebook.__notebook__.metadata.arlunio.author


def test_notebook_loader_checks_existance(testdata):
    """Ensure that the notebook loader checks to see if the given notebook exists,
    raising a helpful error if it doesn't."""

    with py.test.raises(FileNotFoundError) as err:
        NotebookLoader.fromfile("not-found.ipynb")

    assert "not-found.ipynb" in str(err.value)
