import numpy as np
from PIL import Image


def new_image(width, height, alpha=False):
    """
    Create a new numpy ndarray of width x height where each entry is
    either 3 (RGB) for 4 (RGBA) uint8's
    """

    n = 4 if alpha else 3

    return np.zeros((height, width, n), dtype=np.uint8)


def imgmap(img, f):
    """
    Given a function f which takes the values i, j
    representing the percentage the respective x and y
    coordinates are in the domain and apply it to the
    image
    """

    jmax, imax, _ = img.shape

    for i in range(imax):

        # Calculate the percentage the x coordinate is accross the
        # image
        I = i / imax

        for j in range(jmax):

            # Calculate the percentage the y coordinate is accross the
            # image
            J = j / jmax

            res = f(I, J)

            if res is not None:
                img[j, i] = res

    return img


def save_image(img, filepath):
    """
    Given a numpy ndarray like those obtained from new_image
    save an image to disk at filepath
    """

    _, _, n = img.shape

    if n == 4:
        imgdata = Image.frombuffer('RGBA', img.shape[0:2], img, 'raw', 'RGBA', 0, 1)
    else:
        imgdata = Image.frombuffer('RGB', img.shape[0:2], img, 'raw', 'RGB', 0, 1)

    with open(filepath, 'wb') as f:
        imgdata.save(f)


def make_img(width, height, f, filename):
    """
    Convenience function which automates the simple new -> map -> save
    workflow, it also returns the generated image so you can modify it further
    """

    img = new_image(width, height)
    img = imgmap(img, f)
    save_image(img, filename)

    return img
