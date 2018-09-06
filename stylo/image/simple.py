from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import PIL as P


class Image(ABC):
    def __call__(self, width, height, filename=None):

        image = self._render(width, height)

        if filename is not None:
            self._save(image, filename)
            return

        return plt.imshow(image)

    def _save(self, image, filename):

        width, height, _ = image.shape

        pil_image = P.Image.frombuffer(
            "RGB", (width, height), image, "raw", "RGB", 0, 1
        )

        with open(filename, "wb") as f:
            pil_image.save(f)

    @abstractmethod
    def _render(self, width, height):
        pass


class SimpleImage(Image):
    def __init__(self, domain, shape, color):

        self.domain = domain
        self.shape = shape
        self.color = color

    def _render(self, width, height):
        return (width, height) >> self.domain >> self.shape >> self.color
