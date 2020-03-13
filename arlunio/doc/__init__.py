import inspect

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


def _document_inheritance(defn: arlunio.Definition) -> Optional[str]:
    """Given a definition, link back to any definitions it derives from."""

    if not hasattr(defn, "definitions"):
        return None

    defs = []

    for name, value in defn.definitions.items():

        if value == inspect._empty:
            defs.append(name)
            continue

        name = value.__name__
        mod = value.__module__

        defs.append(f":class:`{name} <{mod}.{name}>`")

    return f"*Derives from:* {', '.join(defs)}"


def _process_docstring(
    app: Sphinx, what: str, name: str, obj: Any, options: Any, lines: List[str]
) -> None:

    if inspect.isclass(obj) and issubclass(obj, arlunio.Definition):
        inherits = _document_inheritance(obj)

        if inherits is not None:
            lines.insert(0, "")
            lines.insert(0, inherits)


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
