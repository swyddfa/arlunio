"""This script automatically writes the example sections in the documentation."""
import os

import argparse
import pathlib
from importlib import import_module
import sys

EXAMPLE_TEMPLATE = """
.. {reference}:

{title}

.. image:: {imgpath}
   :width: 75%
   :align: center

{description}

.. literalinclude:: ../../..{srcpath}
   :language: python
   :start-after: # <example>
   :end-before: # </example>
   :dedent: 4
"""

INDEX_TEMPLATE = """
.. {reference}:

{title}

.. toctree::

   {files}

"""


def format_title(title):
    underline = "=" * len(title)
    return "{}\n{}".format(title, underline)


def write_index(index):

    for type, items in index.items():

        if len(items) == 0:
            continue

        files = "\n   ".join(items)
        index_file = "docs/{}/examples/index.rst".format(type)

        context = {
            "files": files,
            "title": format_title("Examples"),
            "reference": "_{}_examples".format(type),
        }
        rst = INDEX_TEMPLATE.format(**context)

        with open(index_file, "w") as f:
            f.write(rst)

        # print("Wrote {} index.".format(type))


def write_example_page(root, example, index):

    info = example.example_info
    srcpath = example.__file__.replace(root, "")
    reference = "_" + info["type"] + "_example_" + info["name"]

    # print("\t{}".format(info["name"]))

    # Update the index
    index[info["type"]].append(info["name"])

    context = {
        "title": format_title(info["name"].capitalize()),
        "imgpath": "/_static/examples/" + info["name"] + ".png",
        "description": example.__doc__,
        "srcpath": srcpath,
        "reference": reference,
    }

    rst = EXAMPLE_TEMPLATE.format(**context)

    dirname = pathlib.Path("docs/" + info["type"] + "/examples/")

    if not dirname.exists():
        os.mkdir(str(dirname))

    filename = os.path.join(str(dirname), info["name"] + ".rst")
    with open(filename, "w") as f:
        f.write(rst)


def find_examples(path):
    """Find the examples and import them."""

    dir = pathlib.Path(path)
    examples = []

    for example_path in dir.glob("*.py"):

        if example_path.name == "__init__.py":
            continue

        module_name = str(example_path).replace("/", ".").replace(".py", "")
        examples.append(import_module(module_name))

    return examples


def parse_arguments():

    parser = argparse.ArgumentParser(prog="exampledoc.py")
    parser.add_argument(
        "-e, --examples",
        nargs=1,
        type=str,
        dest="examples",
        required=True,
        help="the folder containing the example tests.",
    )

    return parser.parse_args()


def main():

    root = os.path.abspath(".")

    # Fix the path so that the test files can be imported.
    sys.path.insert(0, root)

    args = parse_arguments()
    index = {"using": [], "extending": [], "contributing": []}

    examples = find_examples(args.examples[0])

    print("Found {} examples".format(len(examples)))

    for example in examples:
        write_example_page(root, example, index)

    write_index(index)


if __name__ == "__main__":
    main()
