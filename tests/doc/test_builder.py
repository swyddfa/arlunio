import os
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


@py.test.mark.parametrize(
    "name",
    [
        "bare_link",
        "bold",
        "bullet_list",
        "comment",
        "doctest_no_output",
        "heading",
        "inline_code",
        "inline_link",
        "italic",
        "literal_block",
        "paragraphs",
        "note",
    ],
)
def test_notebook_translator(testdata, name):
    """Ensure that the notebook translator can correctly convert an rst doctree into
    the correct sequence of notebook cells."""

    rst = testdata(os.path.join("doc", name + ".rst")).decode("utf8")

    json = testdata(os.path.join("doc", name + ".ipynb")).decode("utf8")
    nb = nbf.reads(json)

    # Getting docutils to generate a doctree for us appears to require some gymnastics
    # perhaps there is a better way?
    parser = Parser()
    settings = _get_mock_settings()

    reader = Reader()
    doctree = reader.read(StringInput(rst), parser, settings)

    translator = NotebookTranslator(doctree)
    doctree.walkabout(translator)

    actual = nbf.writes(translator.asnotebook())
    expected = nbf.writes(nb)
    assert expected == actual
