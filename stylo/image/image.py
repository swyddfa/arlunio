from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import PIL as P


class Image(ABC):
    def __call__(self, width, height, filename=None, plot_size=None):

        image = self._render(width, height)
        self.data = image

        if filename is not None:
            self._save(image, filename)
            return

        if plot_size is None:
            plot_size = 4

        fig, ax = plt.subplots(1, figsize=(plot_size, plot_size))
        ax.imshow(image)

        return fig

    def _save(self, image, filename):

        width, height, _ = image.shape

        pil_image = P.Image.frombuffer(
            "RGB", (width, height), image, "raw", "RGB", 0, 1
        )

        with open(filename, "wb") as f:
            pil_image.save(f)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @abstractmethod
    def _render(self, width, height):
        pass
