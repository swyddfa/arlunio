from .image import Image


class LayeredImage:
    """
    This is a container for a number of images, with a number of conveniences
    for blending/merging them together - just as you would in GIMP/Photoshop
    etc.
    """

    def __init__(self, width=None, height=None, num_layers=4, imgs=None):

        if imgs is not None:

            # TODO: Do a check to make sure given images make sense
            self._layers = imgs
            self._width = imgs[0].width
            self._height = imgs[0].height

        else:
            self._layers = [Image(width, height, background=(0, 0, 0, 0))
                            for _ in range(num_layers)]

            self._width = width
            self._height = height

    def __repr__(self):
        return "%ix%i Layered Image with %i layers"\
                % (self.width, self.height, self.nlayers)

    def __getitem__(self, key):

        if isinstance(key, (int,)):
            return self._layers[key]

        else:
            return 'Other methods coming soon'

    @classmethod
    def fromlist(cls, imgs):
        return cls(imgs=imgs)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def nlayers(self):
        return len(self._layers)
