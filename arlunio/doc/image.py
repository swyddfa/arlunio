import pathlib
import traceback

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Figure
from sphinx.util import logging

import arlunio.image as image


class arlunio_image(nodes.General, nodes.Element):
    pass


def visit_arlunio_image(self, node):
    pass


def depart_arlunio_image(self, node):
    pass


def render_image(src: str, name: str, outdir: pathlib.Path) -> pathlib.Path:
    """Given the source code for an image, render it and save it to file.

    Parameters
    ----------
    src:
        The code that produces the image
    name:
        The name of the image
    outdir:
        Where the image should be saved.

    Return
    ------
    The path to the image, relative to the root of the Sphinx project
    """
    env = {}
    logger = logging.getLogger(__name__)

    code = compile(src, "<string>", "exec")
    exec(code, env)

    img = None

    for obj in env.values():
        if isinstance(obj, image.Image):
            img = obj

    if img is None:
        raise ValueError("Code did not produce a valid image.")

    outfile = pathlib.Path("_images", name + ".png")
    logger.debug("[arlunio-image] Saving image to: %s", outfile)

    image.save(img, pathlib.Path(outdir, outfile), mkdirs=True)

    return outfile


class ArlunioImageDirective(Figure):
    """Given some code that produces an image, render it in the page."""

    has_content = True
    final_argument_whitespace = True

    def code(arg):
        return directives.choice(arg, ("above", "below"))

    option_spec = Figure.option_spec.copy()
    option_spec["include-code"] = code

    def run(self):

        logger = logging.getLogger(__name__)

        src = "\n".join(self.content)
        logger.debug("[arlunio-image: %s", type(self.content))
        imgname = self.arguments[0].lower().replace(" ", "-")
        include_code = self.options.pop("include-code", None)

        # First we will process the content of the directive in order to produce an
        # image on disk. We will then defer to the default behavior of the Figure
        # directive to handle the rest.
        app = self.state.document.settings.env.app

        try:
            # Rewrite the arguments list to contain the reference to the image file
            imguri = render_image(src, imgname, app.confdir)
            self.arguments[0] = "/" + str(imguri)
        except Exception:
            tback = traceback.format_exc()

            # Flag the issue to the user to the issue in the log
            location = self.state_machine.get_source_and_line(self.lineno)
            logger.warning("Unable to render image\n%s", tback, location=location)

            # But also make the error obvious in the docs.
            message = nodes.Text("Unable to render image:")
            err = nodes.literal_block("", tback)

            return [nodes.error("", message, err)]

        # Now defer to the standard figure implementation.
        self.content = None
        (figure,) = Figure.run(self)

        if include_code is None:
            return [arlunio_image("", figure)]

        code_block = nodes.literal_block("", src)
        code_block["language"] = "python"

        if include_code == "above":
            return [arlunio_image("", code_block, figure)]

        return [arlunio_image("", figure, code_block)]


def register(app):

    app.add_node(
        arlunio_image,
        html=(visit_arlunio_image, depart_arlunio_image),
        latex=(visit_arlunio_image, depart_arlunio_image),
        text=(visit_arlunio_image, depart_arlunio_image),
    )

    app.add_directive("arlunio-image", ArlunioImageDirective)
