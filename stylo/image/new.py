import numpy as np
from stylo.image.base import ImageFactory


_factory = ImageFactory()


@_factory.variable
def x(width, height, *, x0=0, x1=1):
    xs = np.linspace(x0, x1, width)
    xs = np.array([xs for _ in range(height)])

    return xs


@_factory.variable
def y(width, height, *, y0=0, y1=1):
    ys = np.linspace(y1, y0, height)
    ys = np.array([ys for _ in range(width)])
    ys = ys.transpose()

    return ys


@_factory.render
def render(width, height, image):

    image_data = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)
    args = set([arg for shape, _ in image._layers for arg in shape.args])

    variables = image._domain(width, height, varnames=args)

    for shape, color in image._layers:
        vars_ = {k: v for k, v in variables.items() if k in shape.args}
        mask = shape(**vars_)
        image_data = color(mask, image_data=image_data)

    return image_data


StandardImage = _factory.construct()
