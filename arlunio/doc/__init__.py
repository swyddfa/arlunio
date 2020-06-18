import inspect
import textwrap
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from sphinx.application import Sphinx

import arlunio
from .image import register as register_image
from .notebook import register as register_notebook

# fmt: off
TEMPLATE = [
    ".. list-table::",
    "   :widths: 5 20",
    "   :header-rows: 0",
    "",
]
# fmt: on


def _document_inputs(defn: arlunio.Defn, lines: List[str]):
    """Given a definition, document any inputs."""

    inputs = []

    for name, value in defn.inputs().items():
        dtype = value.dtype

        if hasattr(value.dtype, "__name__"):
            dtype = dtype.__name__

        inputs.append(f":code:`{name}: {dtype}`")

    if len(inputs) > 0:
        lines.append(textwrap.indent("* - **Inputs:**", " " * 3))
        lines.append(textwrap.indent(" ".join(inputs), " " * 5 + "- "))


def _document_bases(defn: arlunio.Defn, lines: List[str]):
    """Given a definition, document any definitions it is derived from."""

    defns = []

    for name, value in defn.bases().items():

        name = value.__name__
        mod = value.__module__

        defns.append(f":class:`{name} <{mod}.{name}>`")

    if len(defns) > 0:
        lines.append(textwrap.indent("* - **Bases:**", " " * 3))
        lines.append(textwrap.indent(" ".join(defns), " " * 5 + "- "))


def _document_produces(defn: arlunio.Defn, lines: List[str]):
    """Given a definition and it declares with it produces, document it."""

    if defn.produces() == Any:
        return

    result = defn.produces()

    name = result.__name__
    mod = result.__module__

    lines.append(textwrap.indent("* - **Produces:**", " " * 3))
    lines.append(textwrap.indent(f":class:`{name} <{mod}.{name}>`", " " * 5 + "- "))


def _document_inheritance(defn: arlunio.Defn) -> Optional[List[str]]:
    """Given a definition, link back to any definitions it derives from."""

    lines = []

    _document_inputs(defn, lines)
    _document_bases(defn, lines)
    _document_produces(defn, lines)

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

    app.setup_extension("sphinx.ext.autodoc")
    app.connect("autodoc-process-docstring", _process_docstring)

    register_image(app)
    register_notebook(app)

    return {"version": arlunio.__version__, "parallel_read_safe": True}
