import typing

import stylo
from sphinx.application import Sphinx

from .builder import NotebookTutorialBuilder
from .directives import (
    AutoShapeDirective,
    NBTutorialDirective,
    StyloImageDirective,
    depart_nbtutorial,
    nbtutorial,
    visit_nbtutorial,
)


def setup(app: Sphinx) -> typing.Dict[str, typing.Any]:

    app.add_node(
        nbtutorial,
        html=(visit_nbtutorial, depart_nbtutorial),
        latex=(visit_nbtutorial, depart_nbtutorial),
        text=(visit_nbtutorial, depart_nbtutorial),
    )
    app.add_builder(NotebookTutorialBuilder)

    app.add_directive("autoshape", AutoShapeDirective)
    app.add_directive("nbtutorial", NBTutorialDirective)
    app.add_directive("styloimage", StyloImageDirective)

    return {"version": stylo.__version__, "parallel_read_safe": True}
