#!/usr/bin/env python
"""A custom script that does what the :code:`sphinx-apidoc` command does, but this gives
us more control over the output.
"""
import os
from os import path

import argparse
import pathlib

RST_TEMPLATE="""

.. {reference}:

{title}

.. automodule:: {module}
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:

"""


RST_INDEX="""
API Reference
=============

.. toctree::

   {}
"""


def format_title(name):
    """Given a module name, format it as an rst header.

    :param name: The module name
    :type name: str
    """

    underline = "="*len(name)
    title = ".".join(s.capitalize() for s in name.split("."))

    return "{0}\n{1}".format(title, underline)


def format_rst(name):
    """Given the module name, format the rst contents that will be written to file.

    :param name: The module name
    :type name: str
    """

    context = {
        'title': format_title(name),
        'module': name,
        'reference': "_" + name.replace(".", "_")
    }

    return RST_TEMPLATE.format(**context)


def find_modules(module_dir):
    """Given a folder, recursively find all the module files to right the documentation
    for.

    :param module_dir: The folder to start the search in
    :type module_dir: str
    """

    root = pathlib.Path(module_dir)
    modules = []

    for path in root.glob("**/*.py"):

        if path.name == "__init__.py":
            path = path.parent

        module = str(path).replace(".py", "").replace("/", ".")
        modules.append(module)

    return modules


def write_rst(root, name, rst, index):
    """Write the given rst to file."""

    fname = name.replace(".", "_").replace("__", "_")
    index.append(fname)

    filename = path.join(root, fname) + ".rst"

    dir = pathlib.Path(filename).parent

    if not dir.exists():
        os.mkdir(dir)

    with open(filename, 'w') as f:
        f.write(rst)

    print("\t{}.".format(name))


def write_index(out, index):

    entries = "\n   ".join(index)

    with open(path.join(out, "index.rst"), 'w') as f:
        f.write(RST_INDEX.format(entries))


def process_arguments():

    parser = argparse.ArgumentParser(prog="apidoc.py")

    parser.add_argument('-o, --output', nargs=1, type=str, dest="output",
                        help="the folder to write the rst files to.")

    parser.add_argument("-m, --module", nargs=1, type=str, dest="module",
                        required=True,
                        help="the module to document.")

    return parser.parse_args()


def main():

    args = process_arguments()
    out = args.output[0]

    modules = find_modules(args.module[0])
    index = []

    print("Writing API Reference:")

    for module in modules:

        rst = format_rst(module)
        write_rst(out, module, rst, index)

    write_index(out, sorted(index))


if __name__ == '__main__':
    main()


