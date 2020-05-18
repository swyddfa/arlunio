# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os

# -- Project information -----------------------------------------------------

project = "Arlunio"
copyright = "2017-, Swyddfa Developers"
author = "Swyddfa Developers"

# The full version, including alpha/beta/rc tags
version = None

if "VERSION" in os.environ:
    version = os.environ["VERSION"]

if version is None:
    try:
        import arlunio

        version = arlunio.__version__
    except Exception:
        version = "latest"

release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "arlunio.doc",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "_definitions.rst"]

basedir = os.path.dirname(__file__)

with open(os.path.join(basedir, "_definitions.rst")) as f:
    rst_epilog = f.read()

# -- Internationalisation ----------------------------------------------------

# "Primary" language
language = "en"

# Translated text will be stored in this folder
locale_dirs = ["locale/"]
gettext_compact = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

# -- Extension Configuration -------------------------------------------------
autodoc_member_order = "groupwise"
autodoc_default_options = {"members": True}

linkcheck_ignore = ["https://crontab.guru/#"]

intersphinx_mapping = {
    "pillow": ("https://pillow.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
}

napoleon_use_rtype = False
