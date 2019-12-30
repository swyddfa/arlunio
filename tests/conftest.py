import os

import py.test


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
