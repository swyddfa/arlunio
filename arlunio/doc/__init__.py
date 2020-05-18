import inspect
import textwrap

from typing import Any, Dict, List, Optional

import arlunio

from sphinx.application import Sphinx

from .builder import NotebookTutorialBuilder
from .directives import (
    ArlunioImageDirective,
    NBTutorialDirective,
    depart_nbtutorial,
    nbtutorial,
    visit_nbtutorial,
)

# fmt: off
TEMPLATE = [
    ".. list-table::",
    "   :widths: 5 20",
    "   :header-rows: 0",
    "",
]
# fmt: on


def _document_inheritance(defn: arlunio.Defn) -> Optional[List[str]]:
    """Given a definition, link back to any definitions it derives from."""

    lines = []
    inputs = []
    defns = []

    for name, value in defn.inputs().items():
        dtype = value.dtype

        if hasattr(value.dtype, "__name__"):
            dtype = dtype.__name__

        inputs.append(f":code:`{name}: {dtype}`")

    if len(inputs) > 0:
        lines.append(textwrap.indent("* - **Inputs:**", " " * 3))
        lines.append(textwrap.indent(", ".join(inputs), " " * 5 + "- "))

    for name, value in defn.bases().items():

        name = value.__name__
        mod = value.__module__

        defns.append(f":class:`{name} <{mod}.{name}>`")

    if len(defns) > 0:
        lines.append(textwrap.indent("* - **Bases:**", " " * 3))
        lines.append(textwrap.indent(", ".join(defns), " " * 5 + "- "))

    if len(lines) == 0:
        return None

    return list(TEMPLATE) + lines + ["", ""]


def _process_docstring(
    app: Sphinx, what: str, name: str, obj: Any, options: Any, lines: List[str]
) -> None:

    if inspect.isclass(obj) and issubclass(obj, arlunio.Defn):
        inherits = _document_inheritance(obj)

        if inherits is not None:

            for line in reversed(inherits):
                lines.insert(0, line)


def setup(app: Sphinx) -> Dict[str, Any]:

    app.add_node(
        nbtutorial,
        html=(visit_nbtutorial, depart_nbtutorial),
        latex=(visit_nbtutorial, depart_nbtutorial),
        text=(visit_nbtutorial, depart_nbtutorial),
    )
    app.add_builder(NotebookTutorialBuilder)

    app.setup_extension("sphinx.ext.autodoc")
    app.connect("autodoc-process-docstring", _process_docstring)

    app.add_directive("nbtutorial", NBTutorialDirective)
    app.add_directive("arlunio-image", ArlunioImageDirective)

    return {"version": arlunio.__version__, "parallel_read_safe": True}
