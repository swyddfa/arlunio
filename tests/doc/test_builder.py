import unittest.mock as mock

import pytest
from arlunio.doc.builder import Notebook, NotebookCell, NotebookTranslator
from docutils.io import StringInput
from docutils.parsers.rst import Parser, directives
from docutils.readers.standalone import Reader
from sphinx.ext.doctest import DoctestDirective

# Register sphinx specific directives with docutils
directives.register_directive("doctest", DoctestDirective)


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


def _get_mock_settings() -> mock.Mock:
    """Return a mock that can pretend to be the settings object needed when parsing
    rst source.

    It's not clear what all these settings should be, but it appears to be good
    enough to get the tests to run.
    """

    settings = mock.Mock()

    # The following settings were obtained by running the following code and inspecting
    # the resulting settings object, so their values should be fairly representative.
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

    # I'm assuming these settings are extra configuration introduced by Sphinx
    # since they are not created as part of the docutils option parser. As of
    # writing I haven't tracked down the source of truth for them which means
    # there's a good chance these settings are *NOT* representative of a normal
    # build environment.

    settings.tab_width = 2

    return settings


BARE_LINK_RST = """
Link here: `<https://docs.python.org/3.7/>`_
"""
BARE_LINK_CELLS = [
    NotebookCell.markdown(
        "\nLink here: [https://docs.python.org/3.7/](https://docs.python.org/3.7/)\n"
    )
]

BOLD_RST = """
Here is some **bold** text
"""
BOLD_CELLS = [NotebookCell.markdown(BOLD_RST)]

BULLET_LIST_RST = """\
- Item one
- Item two, for reasons it has been decided to make this item be much longer than
  the other items to ensure that we can cover the case where the items contain longer
  lengths of content.
- Item three
"""
BULLET_LIST_MD = """\
- Item one
- Item two, for reasons it has been decided to make this item be much longer than
the other items to ensure that we can cover the case where the items contain longer
lengths of content.
- Item three
"""
BULLET_LIST_CELLS = [NotebookCell.markdown(BULLET_LIST_MD)]

DOCTEST_BLOCK_NO_OUTPUT_RST = """
.. doctest:: example-code

   >>> l = [1,2,3]
   >>> l.append(4)
"""
DOCTEST_BLOCK_NO_OUTPUT_CODE = """\
l = [1,2,3]
l.append(4)\
"""
DOCTEST_BLOCK_NO_OUTPUT_CELLS = [NotebookCell.code(DOCTEST_BLOCK_NO_OUTPUT_CODE)]

DOCTEST_NO_OUTPUT_RST = """
::

   >>> l = [1,2,3]
   >>> l.append(4)
"""
DOCTEST_NO_OUTPUT_CODE = """\
l = [1,2,3]
l.append(4)\
"""
DOCTEST_NO_OUTPUT_CELLS = [NotebookCell.code(DOCTEST_NO_OUTPUT_CODE)]

HEADINGS_RST = """
Heading 1
=========

Heading 2
---------

Heading 3
^^^^^^^^^

Heading 4
\"\"\"\"\"\"\"\"\"

Heading 5
'''''''''
"""
HEADINGS_MD = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5
"""
HEADINGS_CELLS = [NotebookCell.markdown(HEADINGS_MD)]

INLINE_CODE_RST = """
Here is some :code:`inline code`
"""
INLINE_CODE_CELLS = [NotebookCell.markdown("\nHere is some `inline code`\n")]

INLINE_LINK_RST = """
Check out the `documentation <https://docs.python.org/3.7/>`_
"""
INLINE_LINK_CELLS = [
    NotebookCell.markdown(
        "\nCheck out the [documentation](https://docs.python.org/3.7/)\n"
    )
]

ITALIC_RST = """
Here is some *italic* text
"""
ITALIC_CELLS = [NotebookCell.markdown(ITALIC_RST)]

LINK_REFERENCE_RST = """
Check out the `docs`_

.. _docs: https://docs.python.org/3.7/
"""
LINK_REFERENCE_CELLS = [
    NotebookCell.markdown("\nCheck out the [docs](https://docs.python.org/3.7/)\n")
]

LITERAL_BLOCK_RST = """
::

    squares = [n**2 for n in range(100)]
    total = sum(squares)
"""
LITERAL_BLOCK_CODE = """\
squares = [n**2 for n in range(100)]
total = sum(squares)\
"""
LITERAL_BLOCK_CELLS = [NotebookCell.code(LITERAL_BLOCK_CODE)]

PARAGRAPH_RST = """
Here is a simple line of text
"""
PARAGRAPH_CELLS = [NotebookCell.markdown(PARAGRAPH_RST)]

MULTI_PARAGRAPH_RST = """
Here is an extended example that involves more text than what can fit inside a single
paragraph of text. This is to ensure that when the translator encounters mutliple
paragraphs - unlike the code blocks it does not split the paragraph into multiple cells.

Instead this should be combined into a single paragraph with the appropriate spacing
between the lines so that they are formatted accordingly.
"""
MULTI_PARAGRAPH_CELLS = [NotebookCell.markdown(MULTI_PARAGRAPH_RST)]


@pytest.mark.parametrize(
    "rst,cells",
    [
        (BARE_LINK_RST, BARE_LINK_CELLS),
        (BOLD_RST, BOLD_CELLS),
        (BULLET_LIST_RST, BULLET_LIST_CELLS),
        (DOCTEST_BLOCK_NO_OUTPUT_RST, DOCTEST_BLOCK_NO_OUTPUT_CELLS),
        (DOCTEST_NO_OUTPUT_RST, DOCTEST_NO_OUTPUT_CELLS),
        (HEADINGS_RST, HEADINGS_CELLS),
        (INLINE_CODE_RST, INLINE_CODE_CELLS),
        (INLINE_LINK_RST, INLINE_LINK_CELLS),
        (ITALIC_RST, ITALIC_CELLS),
        # Some more thought needed to handle this case
        pytest.param(LINK_REFERENCE_RST, LINK_REFERENCE_CELLS, marks=pytest.mark.xfail),
        (LITERAL_BLOCK_RST, LITERAL_BLOCK_CELLS),
        (MULTI_PARAGRAPH_RST, MULTI_PARAGRAPH_CELLS),
        (PARAGRAPH_RST, PARAGRAPH_CELLS),
    ],
)
def test_notebook_translator(rst, cells):
    """A series of tests to ensure that the notebook translator can correctly convert an
    rst doctree into the correct notebook representation."""

    # Getting `docutils` to generate the doctree for us appears to require
    # some gymnastics... perhaps there is a better way?
    parser = Parser()
    settings = _get_mock_settings()

    reader = Reader()
    doctree = reader.read(StringInput(rst), parser, settings)

    # Now for the actual test.
    notebook = Notebook.fromcells(cells)
    expected = notebook.json

    translator = NotebookTranslator(doctree)
    doctree.walkabout(translator)

    assert expected == translator.asdict()
