import textwrap

from arlunio.doc.directives import format_error, render_image
from docutils import nodes
from docutils.statemachine import StringList


class TestRenderImage:
    """Tests for the :code:`render_image` function."""

    def test_handles_syntax_error(self):
        """Ensure that if there is an error when compiling the code we can
        handle it."""

        src = "x 1 + 2"
        doctree = render_image(src)

        assert len(doctree) == 1
        assert isinstance(doctree[0], nodes.error), "Expected error node."

        error = doctree[0]
        assert len(error.children) == 2, "Expected two content nodes."

        text, trace = error.children

        assert isinstance(text, nodes.Text), "Expected text node."
        assert "Unable to render image" in text.astext()

        assert isinstance(trace, nodes.literal_block)
        assert "Traceback" in trace.astext()
        assert "SyntaxError" in trace.astext()

    def test_handles_runtime_error(self):
        """Ensure that if there is an error when executing the code we can handle it."""

        src = "x = 1 / 0"
        doctree = render_image(src)

        assert len(doctree) == 1
        assert isinstance(doctree[0], nodes.error), "Expected error node."

        error = doctree[0]
        assert len(error.children) == 2, "Expected two content nodes."

        text, trace = error.children

        assert isinstance(text, nodes.Text), "Expected text node."
        assert "Unable to render image" in text.astext()

        assert isinstance(trace, nodes.literal_block)
        assert "Traceback" in trace.astext()
        assert "ZeroDivisionError" in trace.astext()

    def test_image_provided(self):
        """Ensure that if the code provides an image we use that."""

        src = """\
        import arlunio as ar

        circle = ar.S.Circle()
        disk = circle(4,4)
        """
        doctree = render_image(textwrap.dedent(src))

        assert len(doctree) == 1
        assert isinstance(doctree[0], nodes.raw), "Expected raw node"


class TestFormatError:
    """Tests for the :code:`format_error` function."""

    def test_formatter(self):

        err = "\n".join(
            [
                "Traceback (most recent call last):",
                '   File "<stdin>", line 1, in <module>',
                "ZeroDivisionError: division by zero",
            ]
        )
        content = format_error("Unable to perform :code:`2 / 0`", err)

        assert isinstance(content, StringList)

        actual = list(content)
        expected = [
            ".. error::",
            "",
            "   Unable to perform :code:`2 / 0`::",
            "",
            "      Traceback (most recent call last):",
            '         File "<stdin>", line 1, in <module>',
            "      ZeroDivisionError: division by zero",
            "",
        ]

        assert expected == actual
