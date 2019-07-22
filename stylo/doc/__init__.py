import typing

import stylo
from sphinx.application import Sphinx

from .builder import NotebookTutorialBuilder
from .directives import NBTutorialDirective  # noqa: F401
from .directives import AutoShapeDirective, nbtutorial


def setup(app: Sphinx) -> typing.Dict[str, typing.Any]:

    app.add_node(nbtutorial)
    app.add_builder(NotebookTutorialBuilder)

    app.add_directive("autoshape", AutoShapeDirective)
    app.add_directive("nbtutorial", NBTutorialDirective)

    return {"version": stylo.__version__, "parallel_read_safe": True}
