import pathlib

import nbformat.v4 as nbf
import py.test

from arlunio.doc.builder import NotebookTranslator


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
def test_notebook_translator(testdata, parse_rst, name):
    """Ensure that the notebook translator can correctly convert an rst doctree into
    the correct sequence of notebook cells."""

    rst = testdata(pathlib.Path("doc", "nbtutorial", name + ".rst")).decode("utf8")
    json = testdata(pathlib.Path("doc", "nbtutorial", name + ".ipynb")).decode("utf8")
    nb = nbf.reads(json)

    doctree = parse_rst(rst)

    translator = NotebookTranslator(doctree)
    doctree.walkabout(translator)

    actual = nbf.writes(translator.asnotebook())
    expected = nbf.writes(nb)
    assert expected == actual
