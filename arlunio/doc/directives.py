import importlib
import string
import textwrap
import traceback

from typing import List

import arlunio as ar
import attr

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

IMAGE_TEMPLATE = string.Template(
    """\
<figure style="border: solid 1px #ddd;width: 75%;margin:auto">
  <img style="image-rendering:crisp-edges;width:100%"
       src="data:image/png;base64,$data"></img>
</figure>
"""
)


class nbtutorial(nodes.General, nodes.Element):
    pass


def visit_nbtutorial(self, node):
    pass


def depart_nbtutorial(self, node):
    pass


def load_shape(object_spec: str) -> (ar.Shape, str):
    """Given a classpath e.g. :code:`arlunio.lib.basic.Circle` load it.

    There is an issue(?) currently with shapes defined with the :code:`@shape` decorator
    where the shape's module is reported as the module where the :code:`@shape`
    decorator is defined (:code:`arlunio._shapes`) rather than the module where the
    shape is defined (:code:`arlunio.lib.basic`). So this function also returns the true
    module name::

       >>> from arlunio.doc.directives import load_shape

       >>> load_shape("arlunio.lib.basic.Circle")
       (<class 'arlunio._shapes.Circle'>, 'arlunio.lib.basic')

    If the module is not found then a :code:`MoudleNotFoundError` will be raised::

       >>> load_shape("arlunio.notfound.Circle")
       Traceback (most recent call last):
          ...
       ModuleNotFoundError: No module named 'arlunio.notfound'

    If the class within the module cannot be found then an :code:`AttributeError` will
    be raised::

       >>> load_shape("arlunio._shapes.Circle")
       Traceback (most recent call last):
          ...
       AttributeError: module 'arlunio._shapes' has no attribute 'Circle'

    Finally if the given class is not a shape then a :code:`TypeError` will be raised::

       >>> load_shape("arlunio.doc.directives.AutoShapeDirective")
       Traceback (most recent call last):
          ...
       TypeError: 'arlunio.doc.directives.AutoShapeDirective' is not a shape
    """

    *obj_path, obj_name = object_spec.split(".")
    obj_path = ".".join(obj_path)

    logger.debug(f"[autoshape]: Looking for shape: {obj_name} in {obj_path}")

    module = importlib.import_module(obj_path)
    shape = getattr(module, obj_name)

    if not issubclass(shape, ar.Shape):
        raise TypeError(f"'{object_spec}' is not a shape")

    return shape, module.__name__


def document_properties(shape: ar.Shape) -> str:
    """Given a shape's definitio, document all of its properties."""
    template = string.Template(PROPS_TEMPLATE)
    prop_tpl = string.Template(PROP_TEMPLATE)

    properties = []

    for prop in sorted(attr.fields(shape), key=lambda p: p.name):

        ptype = "" if prop.type is None else f"({str(prop.type)})"
        context = {"name": prop.name, "default": prop.default, "type": ptype}

        properties.append(prop_tpl.safe_substitute(context))

    return template.safe_substitute({"props": "\n".join(properties)})


def generate_preview(shape_ins: ar.Shape) -> str:
    """Given an instance of the shape, generate a preview of it."""
    template = string.Template(PREVIEW_TEMPLATE)
    image = shape_ins(1920, 1080)
    name = shape_ins.__class__.__name__

    context = {
        "img_data": image.encode().decode("utf-8"),
        "alt_tag": f"Example instance of the {name} shape",
    }

    return template.safe_substitute(context)


def document_shape(shape: ar.Shape, module_name: str) -> StringList:
    """Given a shape definition, automatically write the reference documentation
    for it.
    """
    default = shape()
    indent = " " * 3
    template = string.Template(SHAPE_TEMPLATE)
    docstring = "" if shape.__doc__ is None else shape.__doc__

    context = {
        "shape_name": shape.__name__ + "\n" + "-" * len(shape.__name__),
        "shape_path": f"{module_name}.{shape.__name__}",
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


def render_image(src: str) -> List[nodes.Node]:
    """Given the source code for an image return a doctree that when rendered by
    Sphinx will insert that image into a HTML page.

    :param src: The source code that produces the image.
    """
    doctree = []

    try:
        code = compile(src, "<string>", "exec")
    except Exception:
        message = nodes.Text("Unable to render image: Invalid code")
        err = nodes.literal_block("", traceback.format_exc())
        doctree.append(nodes.error("", message, err))

        return doctree

    environment = {}

    try:
        exec(code, environment)
    except Exception:
        message = nodes.Text("Unable to render image: Error in code")
        err = nodes.literal_block("", traceback.format_exc())
        doctree.append(nodes.error("", message, err))

        return doctree

    # Look to see if the code produced an image object for us.
    image = None

    for obj in environment.values():
        if isinstance(obj, ar.Image):
            image = obj

    if image is not None:
        context = {"data": image.encode().decode("utf-8")}
        html = IMAGE_TEMPLATE.safe_substitute(context)
        doctree.append(nodes.raw("", html, format="html"))

    return doctree


class AutoShapeDirective(rst.Directive):
    """Given the a shape definition automatically generate its documentation."""

    required_arguments = 1
    optional_arguments = 0
    add_index = False

    def run(self) -> List[nodes.Node]:

        shape_name = self.arguments[0]

        try:
            shape, module_name = load_shape(shape_name)

        except Exception:
            err = traceback.format_exc()
            message = f"**AutoShape:** Unable to load shape: :code:`{shape_name}`"
            content = format_error(message, err)

            return parse_content(self.state, content)

        content = document_shape(shape, module_name)

        section = nodes.section()
        section.document = self.state.document
        nested_parse_with_titles(self.state, content, section)

        return section.children


class NBTutorialDirective(rst.Directive):
    def run(self):
        return [nbtutorial("")]


class ArlunioImageDirective(rst.Directive):
    """Given some code that produces an image, render it in the page."""

    has_content = True

    def run(self):

        src = "\n".join(self.content)
        return render_image(src)
