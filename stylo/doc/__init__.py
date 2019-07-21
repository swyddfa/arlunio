import typing

import stylo
from sphinx.application import Sphinx

from .directives import AutoShapeDirective  # noqa: F401


def setup(app: Sphinx) -> typing.Dict[str, typing.Any]:
    app.add_directive("autoshape", AutoShapeDirective)

    return {"version": stylo.__version__, "parallel_read_safe": True}
