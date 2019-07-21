from stylo.doc.builder import Notebook, NotebookCell


class TestNotebook:
    """Tests for the :code:`Notebook` class."""

    def test_to_json(self):
        """Ensure that we can convert a :code:`Notebook` instance into a valid
        notebook."""

        expected = {
            "nbformat": 4,
            "nbformat_minor": 2,
            "metadata": {},
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [],
                }
            ],
        }

        cell = NotebookCell.code()
        nb = Notebook.fromcells([cell])

        assert expected == nb.json
