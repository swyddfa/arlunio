"""A custom `autoshape` directive used to automatically document shape definitions
in the spirit of the autodoc extension.
"""
import importlib
import string
import textwrap
import traceback
from typing import List

import attr
import stylo as st
from docutils import nodes
from docutils.parsers import rst
from docutils.statemachine import StringList
from sphinx.util import logging, nested_parse_with_titles

logger = logging.getLogger(__name__)


ERROR_TEMPLATE = """\
.. error::

${message}

${traceback}
"""

SHAPE_TEMPLATE = """\
${shape_name}

.. py:class:: ${shape_path}

${shape_image}

${shape_desc}

${shape_props}
"""

PROPS_TEMPLATE = """\
:Properties:

${props}
"""

PROP_TEMPLATE = """\
- **${name}** ${type} - Default: :code:`${default}`
"""

PREVIEW_TEMPLATE = """\
.. raw:: html

   <figure>
     <img alt="${alt_tag}"
          src="data:image/png;base64,${img_data}"
          style="border: solid 1px #ddd"/>
     <figcaption style="margin: 10px;text-align:center">
       <small style="font-style:italic">${alt_tag}</small>
     </figcaption>
   </figure>

"""


class nbtutorial(nodes.General, nodes.Element):
    pass


def load_shape(object_spec: str) -> st.Shape:
    """Given a classpath e.g. :code:`stylo.shapes.Circle` load it."""

    *obj_path, obj_name = object_spec.split(".")
    obj_path = ".".join(obj_path)

    logger.debug(f"[autoshape]: Looking for shape: {obj_name} in {obj_path}")

    module = importlib.import_module(obj_path)
    shape = getattr(module, obj_name)

    if not issubclass(shape, st.Shape):
        raise TypeError(f"{object_spec} is not a shape")

    return shape


def document_properties(shape: st.Shape) -> str:
    """Given a shape's definitio, document all of its properties."""
    template = string.Template(PROPS_TEMPLATE)
    prop_tpl = string.Template(PROP_TEMPLATE)

    properties = []

    for prop in sorted(attr.fields(shape), key=lambda p: p.name):

        ptype = "" if prop.type is None else f"({str(prop.type)})"
        context = {"name": prop.name, "default": prop.default, "type": ptype}

        properties.append(prop_tpl.safe_substitute(context))

    return template.safe_substitute({"props": "\n".join(properties)})


def generate_preview(shape_ins: st.Shape) -> str:
    """Given an instance of the shape, generate a preview of it."""
    template = string.Template(PREVIEW_TEMPLATE)
    image = shape_ins(1920, 1080)
    name = shape_ins.__class__.__name__

    context = {
        "img_data": image.encode().decode("utf-8"),
        "alt_tag": f"Example instance of the {name} shape",
    }

    return template.safe_substitute(context)


def document_shape(shape: st.Shape) -> StringList:
    """Given a shape definition, automatically write the reference documentation
    for it.
    """
    default = shape()
    indent = " " * 3
    template = string.Template(SHAPE_TEMPLATE)
    docstring = "" if shape.__doc__ is None else shape.__doc__

    context = {
        "shape_name": shape.__name__ + "\n" + "-" * len(shape.__name__),
        "shape_path": f"{shape.__module__}.{shape.__name__}",
        "shape_desc": textwrap.indent(docstring, indent),
        "shape_props": textwrap.indent(document_properties(shape), indent),
        "shape_image": textwrap.indent(generate_preview(default), indent),
    }

    documentation = template.safe_substitute(context)

    return StringList(documentation.split("\n"), source="")


def format_error(message: str, err: str) -> StringList:
    """Given an error message format it as an error."""

    indent = " " * 3
    msg = textwrap.indent(message + "::", indent)
    err_msg = textwrap.indent(err, indent * 2)

    template = string.Template(ERROR_TEMPLATE)
    error = template.safe_substitute({"message": msg, "traceback": err_msg})

    return StringList(error.split("\n"), source="")


def parse_content(state, content: StringList) -> List[nodes.Node]:
    """Given a reStructured text representation of some content format parse it
    into a list of nodes."""

    section = nodes.section()
    section.document = state.document
    nested_parse_with_titles(state, content, section)

    return section.children


class AutoShapeDirective(rst.Directive):
    """Given the a shape definition automatically generate its documentation."""

    required_arguments = 1
    optional_arguments = 0
    add_index = False

    def run(self) -> List[nodes.Node]:

        shape_name = self.arguments[0]

        try:
            shape = load_shape(shape_name)

        except Exception:
            err = traceback.format_exc()
            message = f"**AutoShape:** Unable to load shape: :code:`{shape_name}`"
            content = format_error(message, err)

            return parse_content(self.state, content)

        content = document_shape(shape)

        section = nodes.section()
        section.document = self.state.document
        nested_parse_with_titles(self.state, content, section)

        return section.children


class NBTutorialDirective(rst.Directive):
    def run(self):
        return [nbtutorial("")]
