import pytest
from arlunio.doc.builder import Notebook, NotebookCell, NotebookTranslator
from docutils.core import Publisher
from docutils.io import StringInput
from docutils.parsers.rst import Parser
from docutils.readers.standalone import Reader


class TestNotebook:
    """Tests for the :code:`Notebook` class."""

    def test_to_json(self):
        """Ensure that we can convert a :code:`Notebook` instance into a valid
        notebook."""

        expected = {
            "nbformat": 4,
            "nbformat_minor": 2,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": ["\n"],
                },
                {"cell_type": "markdown", "metadata": {}, "source": ["\n"]},
            ],
        }

        code = NotebookCell.code()
        markdown = NotebookCell.markdown()
        nb = Notebook.fromcells([code, markdown])

        assert expected == nb.json


PARAGRAPH_RST = "Here is a simple line of text"
PARAGRAPH_CELLS = [NotebookCell.markdown("\nHere is a simple line of text\n")]

MULTI_PARAGRAPH_RST = """\
Here is an extended example that involves more text than what can fit inside a single
paragraph of text. This is to ensure that when the translator encounters mutliple
paragraphs - unlike the code blocks it does not split the paragraph into multiple cells.

Instead this should be combined into a single paragraph with the appropriate spacing
between the lines so that they are formatted accordingly.
"""
MULTI_PARAGRAPH_CELLS = [NotebookCell.markdown("\n" + MULTI_PARAGRAPH_RST)]


@pytest.mark.parametrize(
    "rst,cells",
    [(PARAGRAPH_RST, PARAGRAPH_CELLS), (MULTI_PARAGRAPH_RST, MULTI_PARAGRAPH_CELLS)],
)
def test_notebook_translator(rst, cells):
    """A series of tests to ensure that the notebook translator can correctly convert an
    rst doctree into the correct notebook representation."""

    # Getting `docutils` to generate the doctree for us appears to require
    # some gymnastics... perhaps there is a better way?
    parser = Parser()
    publisher = Publisher()
    opts = publisher.setup_option_parser()

    settings = opts.get_default_values()
    settings.tab_width = 0
    settings.pep_references = 0
    settings.rfc_references = 0

    reader = Reader()
    doctree = reader.read(StringInput(rst), parser, settings)

    # Now for the actual test.
    notebook = Notebook.fromcells(cells)
    expected = notebook.json

    translator = NotebookTranslator(doctree)
    doctree.walkabout(translator)

    assert expected == translator.asdict()
