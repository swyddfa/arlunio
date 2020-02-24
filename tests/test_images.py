import arlunio as ar
import numpy as np


def test_colorramp_defaults():
    """Ensure that the colorramp method chooses sensible defaults."""

    values = np.array([[0.0, 0.5], [0.75, 1.0]])
    img = ar.colorramp(values)

    pix = np.array(
        [[[0, 0, 0], [127, 127, 127]], [[191, 191, 191], [255, 255, 255]]],
        dtype=np.uint8,
    )

    assert (np.asarray(img) == pix).all()


def test_colorramp():
    """Ensure that the colorramp parses the colors it is given."""

    values = np.array([[0.0, 0.5], [0.75, 1.0]])
    img = ar.colorramp(values, start="#f00", stop="#0f0")

    pix = np.array(
        [[[255, 0, 0], [127, 127, 0]], [[63, 191, 0], [0, 255, 0]]], dtype=np.uint8
    )

    assert (np.asarray(img) == pix).all()


def test_fill_defaults():
    """Ensure that the fill method chooses sensible defaults."""

    mask = np.array([[False, True], [True, False]])
    img = ar.fill(mask)

    pix = np.array(
        [[[255, 255, 255], [0, 0, 0]], [[0, 0, 0], [255, 255, 255]]], dtype=np.uint8
    )

    assert (np.asarray(img) == pix).all()


def test_fill():
    """Ensure that the fill method parses colors that it is given."""

    mask = np.array([[False, True], [True, False]])
    img = ar.fill(mask, color="#f00", background="#0f0")

    pix = np.array(
        [[[0, 255, 0], [255, 0, 0]], [[255, 0, 0], [0, 255, 0]]], dtype=np.uint8
    )

    assert (np.asarray(img) == pix).all()
