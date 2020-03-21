import unittest.mock as mock

import nbformat.v4 as nbf
import py.test

from arlunio.doc.builder import NotebookTranslator
from docutils.io import StringInput
from docutils.parsers.rst import Parser, directives
from docutils.readers.standalone import Reader
from sphinx.ext.doctest import DoctestDirective

# Register sphinx specific directives with docutils
directives.register_directive("doctest", DoctestDirective)


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

BULLET_LIST_MD = """\
- Item one
- Item two, for reasons it has been decided to make this item much longer than
the other items to ensure that we can cover the case where the items contiain longer
content
- Item three
"""

BULLET_LIST_CELLS = [nbf.new_markdown_cell(BULLET_LIST_MD)]

DOCTEST_DIRECTIVE_NO_OUTPUT_RST = """
.. doctest:: example-code

   >>> l = [1,2,3]
   >>> l.append(4)
"""

DOCTEST_DIRECTIVE_NO_OUTPUT_CODE = """\
l = [1,2,3]
l.append(4)\
"""

DOCTEST_DIRECTIVE_NO_OUTPUT_CELLS = [
    nbf.new_code_cell(DOCTEST_DIRECTIVE_NO_OUTPUT_CODE)
]

DOCTEST_NO_OUTPUT_RST = """
::

   >>> l = [1,2,3]
   >>> l.append(4)
"""

DOCTEST_NO_OUTPUT_CODE = """\
l = [1,2,3]
l.append(4)\
"""

DOCTEST_NO_OUTPUT_CELLS = [nbf.new_code_cell(DOCTEST_NO_OUTPUT_CODE)]

HEADING_RST = """
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

HEADING_MD = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5
"""

HEADING_CELLS = [nbf.new_markdown_cell(HEADING_MD)]

INLINE_CODE_RST = """
Here is some :code:`inline code`
"""

INLINE_CODE_CELLS = [nbf.new_markdown_cell("\nHere is some `inline code`\n")]

INLINE_LINK_RST = """
Check out the `documentation <https://docs.python.org/3.7/>`_
"""

INLINE_LINK_CELLS = [
    nbf.new_markdown_cell(
        "\nCheck out the [documentation](https://docs.python.org/3.7/)\n"
    )
]

ITALIC_RST = """
Here is some *italic* text
"""

ITALIC_CELLS = [nbf.new_markdown_cell(ITALIC_RST)]

LINK_REFERENCE_RST = """
Check out the `docs`_

.. _docs: https://docs.python.org/3.7/
"""

LINK_REFERENCE_CELLS = [
    nbf.new_markdown_cell("\nCheck out the [docs](https://docs.python.org/3.7/)\n")
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

LITERAL_BLOCK_CELLS = [nbf.new_code_cell(LITERAL_BLOCK_CODE)]

PARAGRAPH_RST = """
Here is a simple line of text
"""

PARAGRAPH_CELLS = [nbf.new_markdown_cell(PARAGRAPH_RST)]

MULTI_PARAGRAPH_RST = """
Here is an extended example that involves more text than what can fit inside a single
paragraph of text. This is to ensure that when the translator encounters mutliple
paragraphs - unlike the code blocks it does not split the paragraph into multiple cells.

Instead this should be combined into a single cell with the appropriate spacing
between the lines so that they are formatted accordingly.
"""
MULTI_PARAGRAPH_CELLS = [nbf.new_markdown_cell(MULTI_PARAGRAPH_RST)]


@py.test.mark.parametrize(
    "rst,cells",
    [
        (BARE_LINK_RST, BARE_LINK_CELLS),
        (BOLD_RST, BOLD_CELLS),
        (BULLET_LIST_RST, BULLET_LIST_CELLS),
        (DOCTEST_DIRECTIVE_NO_OUTPUT_RST, DOCTEST_DIRECTIVE_NO_OUTPUT_CELLS),
        (DOCTEST_NO_OUTPUT_RST, DOCTEST_NO_OUTPUT_CELLS),
        (HEADING_RST, HEADING_CELLS),
        (INLINE_CODE_RST, INLINE_CODE_CELLS),
        (INLINE_LINK_RST, INLINE_LINK_CELLS),
        (ITALIC_RST, ITALIC_CELLS),
        # Some thought needed to handle this case
        py.test.param(
            LINK_REFERENCE_RST, LINK_REFERENCE_CELLS, marks=py.test.mark.xfail
        ),
        (LITERAL_BLOCK_RST, LITERAL_BLOCK_CELLS),
        (PARAGRAPH_RST, PARAGRAPH_CELLS),
        (MULTI_PARAGRAPH_RST, MULTI_PARAGRAPH_CELLS),
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

    actual = nbf.writes(translator.asnotebook())
    assert expected == actual
