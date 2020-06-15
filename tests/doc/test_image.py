import pathlib
import unittest.mock as mock

import py.test
from docutils import nodes

import arlunio.image as image
from arlunio.doc.image import arlunio_image


class TestArlunioImageDirective:
    """Tests around the arlunio-image directive.

    In order for the .. arlunio-image:: directive to be implemented and not throw
    an error the implementation must be registered with docutils. This has been done
    as part of the :code:`parse_rst` fixture declared in :code:`conftest.py`
    """

    @py.test.mark.parametrize(
        "name,messages",
        [
            ("syntax-error", ["Traceback", "SyntaxError"]),
            ("runtime-error", ["Traceback", "ZeroDivisionError"]),
            (
                "missing-image",
                ["Traceback", "ValueError", "did not produce a valid image"],
            ),
        ],
    )
    def test_handles_error(self, read_rst, name, messages):
        """Ensure that the directive is able to handle errors with the user's code."""

        with mock.patch("arlunio.doc.image.image.save") as m_save:
            rst = read_rst(pathlib.Path("doc", "arlunio_image", name + ".rst"))

        m_save.assert_not_called()

        error = rst.children[0]
        assert isinstance(error, nodes.error), "Expecting a single error node."

        message, tback = error.children

        assert isinstance(message, nodes.Text)
        assert isinstance(tback, nodes.literal_block)

        assert "Unable to render image" in message.astext()

        for msg in messages:
            assert msg in tback.astext()

    @py.test.mark.parametrize(
        "name,opts",
        [
            ("no-options", {}),
            ("fig-align", {"figure": {"align": "right"}}),
            ("fig-width", {"figure": {"width": "50%"}}),
            ("img-alt", {"image": {"alt": "Example alt text."}}),
            ("img-height", {"image": {"height": "500"}}),
            ("img-scale", {"image": {"scale": 50}}),
            ("img-width", {"image": {"width": "75%"}}),
        ],
    )
    def test_directive_no_code(self, read_rst, name, opts):
        """Ensure that the directive handles the case where the user doesn't ask for the
        code to be included."""

        with mock.patch("arlunio.doc.image.image.save") as m_save:
            rst = read_rst(pathlib.Path("doc", "arlunio_image", name + ".rst"))

        print(rst)

        # Ensure the image produced by the code was saved to disk
        m_save.assert_called_once()
        (img, path), _ = m_save.call_args

        assert isinstance(img, image.Image), "Expected image instance."
        assert path == pathlib.Path("/project/docs/_images", name + ".png")

        # Now ensure the correct doctree was produced
        node = rst.children[0]
        assert isinstance(node, arlunio_image), "Expected arlunio image node."

        figure = node.children[0]
        assert isinstance(figure, nodes.figure), "Expected figure node."

        for k, v in opts.get("figure", {}).items():
            assert figure[k] == v

        imgnode = figure.children[0]

        assert isinstance(imgnode, nodes.image), "Expected image node."
        assert imgnode["uri"] == "/_images/" + name + ".png"

        for k, v in opts.get("image", {}).items():
            assert imgnode[k] == v

    def test_directive_target(self, read_rst):
        """Ensure that the directive handles the case where the user includes the
        :target: option."""

        with mock.patch("arlunio.doc.image.image.save") as m_save:
            rst = read_rst(pathlib.Path("doc", "arlunio_image", "img-target.rst"))

        # Ensure the image produced by the code was saved to disk
        m_save.assert_called_once()
        (img, path), _ = m_save.call_args

        assert isinstance(img, image.Image), "Expected image instance."
        assert path == pathlib.Path("/project/docs/_images/img-target.png")

        # Now ensure the correct doctree was produced
        node = rst.children[0]
        assert isinstance(node, arlunio_image), "Expected arlunio image node."

        print(rst)
        figure = node.children[0]
        assert isinstance(figure, nodes.figure), "Expected figure node."

        ref = figure.children[0]
        assert isinstance(ref, nodes.reference), "Expected reference node."
        assert ref["refuri"] == "https://www.arlun.io/gallery/"

        imgnode = ref.children[0]

        assert isinstance(imgnode, nodes.image), "Expected image node."
        assert imgnode["uri"] == "/_images/img-target.png"
