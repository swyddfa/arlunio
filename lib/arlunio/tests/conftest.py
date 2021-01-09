import os
import unittest.mock as mock

import py.test
from docutils.io import StringInput
from docutils.parsers.rst import directives
from docutils.parsers.rst import Parser
from docutils.readers.standalone import Reader
from sphinx.ext.doctest import DoctestDirective

from arlunio.doc.image import ArlunioImageDirective
from arlunio.doc.notebook import NBSolutionDirective


@py.test.fixture(scope="session")
def testdata():
    """Given the name of a file in the data/ folder return its contents.

    Alternatively if the :code:`path_only` option is set just return the full
    path to it.
    """

    basepath = os.path.join(os.path.dirname(__file__), "data")

    def loader(filename, path_only=False):

        filepath = os.path.join(basepath, filename)

        if path_only:
            return filepath

        with open(filepath, "rb") as f:
            return f.read()

    return loader


@py.test.fixture(scope="session")
def rst_mock_settings():
    """Return a mock that can pretend to be the settings object needed to parse rst
    source.

    It's not clear what these settings should be but it appears to be enough to get the
    tests to run.
    """
    settings = mock.Mock()

    # The following settings were obtained by running the following code and inspecting
    # the resulting settings object, so their values should be fairly sensible
    #
    # >>> from docutils.core import Publisher
    #
    # >>> publisher = Publisher()
    # >>> opts = publisher.setup_option_parser()
    # >>> settings = opts.get_default_values()

    settings.halt_level = 4
    settings.id_prefix = ""
    settings.language_code = "en"
    settings.report_level = 2

    # I'm assuming these settings are extras introduced by Sphinx since they were not
    # created as part of the defaults. I haven't currently tracked down the source of
    # truth of these so there's a good chance these values are **not** representative.

    settings.tab_width = 2

    # Fake some additional settings on the (Sphinx?) app object
    settings.env.app.confdir = "/project/docs"

    return settings


@py.test.fixture(scope="session")
def parse_rst(rst_mock_settings):
    """A fixture that attempts to produce a doctree from rst source in a representative
    environment"""

    # Register any extended directives with docutils.
    directives.register_directive("doctest", DoctestDirective)
    directives.register_directive("arlunio-image", ArlunioImageDirective)
    directives.register_directive("nbsolution", NBSolutionDirective)

    def parse(src):
        parser = Parser()
        settings = rst_mock_settings

        reader = Reader()
        return reader.read(StringInput(src), parser, settings)

    return parse


@py.test.fixture(scope="session")
def read_rst(testdata, parse_rst):
    """A fixture that automates the loading of test rst files and parsing them into a
    doctree."""

    def load(path):
        rst = testdata(path).decode("utf8")
        return parse_rst(rst)

    return load
