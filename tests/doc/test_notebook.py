import pathlib
import tempfile

import docutils.nodes as nodes
import nbformat.v4 as nbf
import py.test

import arlunio.doc.notebook as notebook


def make_solution(src):

    soln = notebook.nbsolution()
    soln.children = [notebook.codeblock(src)]

    return soln


class TestProcessSolutions:
    """Tests for the process_solutions function."""

    @py.test.mark.parametrize(
        "docname",
        [
            pathlib.Path("users", "index"),
            pathlib.Path("getting-started"),
            pathlib.Path("users", "tutorial", "first-example"),
        ],
    )
    def test_make_resources_dir(self, docname):
        """Ensure that if the resources dir doesn't exist it gets created."""

        soln = make_solution('print("Hello, world!")')

        with tempfile.TemporaryDirectory() as outdir:
            notebook.process_solutions([soln], pathlib.Path(outdir), docname)
            assert pathlib.Path(outdir, docname.parent, "resources").exists()

    @py.test.mark.parametrize(
        "docname",
        [
            pathlib.Path("users", "index"),
            pathlib.Path("getting-started"),
            pathlib.Path("users", "tutorial", "first-example"),
        ],
    )
    def test_solution_fname(self, docname):
        """Ensure that an appropriate filename is chosen."""

        soln1 = make_solution('print("hello1")')
        soln2 = make_solution('print("hello2")')
        soln3 = make_solution('print("hello3")')

        with tempfile.TemporaryDirectory() as outdir:
            notebook.process_solutions(
                [soln1, soln2, soln3], pathlib.Path(outdir), docname
            )

            for i in range(1, 4):
                file = pathlib.Path(
                    outdir,
                    docname.parent,
                    "resources",
                    docname.name + f"-soln-{i:02d}.py",
                )

                with file.open() as f:
                    assert f.read() == f'print("hello{i}")'

    def test_rewrites_doctree(self):
        """Ensure that the doctree is rewritten to load the solution from disk."""

        soln = make_solution("print('Hello, world!')")

        with tempfile.TemporaryDirectory() as outdir:
            notebook.process_solutions(
                [soln], pathlib.Path(outdir), pathlib.Path("users")
            )
            path = pathlib.Path(outdir, "resources", "users-soln-01.py")

            write, load = soln.children

            assert isinstance(write, nodes.literal_block)
            assert write.astext() == "# Write your solution here...\n"

            assert isinstance(load, nodes.literal_block)
            expected = (
                "# Execute this cell to load the example solution\n"
                f"%load {path.relative_to(outdir)}"
            )
            assert load.astext() == expected


@py.test.mark.parametrize(
    "name",
    [
        "bare_link",
        "bold",
        "bullet_list",
        "comment",
        "doctest_no_output",
        "heading",
        "image",
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

    translator = notebook.NotebookTranslator(doctree)
    doctree.walkabout(translator)

    actual = nbf.writes(translator.asnotebook())
    expected = nbf.writes(nb)
    assert expected == actual
