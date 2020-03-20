import unittest.mock as mock

import py.test
import nbformat.v4 as nbf

from arlunio.doc.builder import Notebook, NotebookCell, NotebookTranslator

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
            "metadata": {},
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


def _get_mock_settings() -> mock.Mock:
    """Return a mock that can pretend to be the settings object needed to parse rst
    source.

    It's not clear what these settings should be but it appears to be enough to get the
    tests to run.
    """
    settings = mock.Mock()

    # The following settings were obtained by running the following code and inspecting
    # the resulting settings object, so their values should be fairly sensible
    #
    # >>> from docutils.core import Publisher
    #
    # >>> publisher = Publisher()
    # >>> opts = publisher.setup_option_parser()
    # >>> settings = opts.get_default_values()

    settings.halt_level = 4
    settings.id_prefix = ""
    settings.language_code = "en"
    settings.report_level = 2

    # I'm assuming these settings are extras introduced by Sphinx since they were not
    # created as part of the defaults. I haven't currently tracked down the source of
    # truth of these so there's a good chance these values are **not** representative.

    settings.tab_width = 2

    return settings


BARE_LINK_RST = """
Link here: `<https://docs.python.org/3.7/>`_
"""

BARE_LINK_CELLS = [
    nbf.new_markdown_cell(
        "\nLink here: [https://docs.python.org/3.7/](https://docs.python.org/3.7/)\n"
    )
]

BOLD_RST = """
Here is some **bold** text
"""

BOLD_CELLS = [nbf.new_markdown_cell(BOLD_RST)]

BULLET_LIST_RST = """
- Item one
- Item two, for reasons it has been decided to make this item much longer than
  the other items to ensure that we can cover the case where the items contiain longer
  content
- Item three
"""

BULLET_LIST_MD = """
- Item one
- Item two, for reasons it has been decided to make this item much longer than
the other items to ensure that we can cover the case where the items contiain longer
content
- Item three
"""

BULLET_LIST_CELLS = [nbf.new_markdown_cell(BULLET_LIST_MD)]


@py.test.mark.parametrize(
    "rst,cells",
    [
        (BARE_LINK_RST, BARE_LINK_CELLS),
        (BOLD_RST, BOLD_CELLS),
        (BULLET_LIST_RST, BULLET_LIST_MD),
    ],
)
def test_notebook_translator(rst, cells):
    """Ensure that the notebook translator can correctly convert an rst doctree into
    the correct sequence of notebook cells."""

    # Getting docutils to generate a doctree for us appears to require some gymnastics
    # perhaps there is a better way?
    parser = Parser()
    settings = _get_mock_settings()

    reader = Reader()
    doctree = reader.read(StringInput(rst), parser, settings)

    # Now for the actual test
    notebook = nbf.new_notebook(cells=cells)
    expected = nbf.writes(notebook)

    translator = NotebookTranslator(doctree)
    doctree.walkabout(translator)

    assert expected == nbf.writes(translator.asnotebook())
