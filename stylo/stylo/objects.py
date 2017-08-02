import numpy as np

from math import floor, ceil, sqrt

from .coords import Drawable


class MetaSet(type):

    def __new__(cls, name, bases, attrs):

        tiles = [(key, val) for key, val in attrs.items()
                  if not key.startswith('_') and
                  isinstance(val, (Drawable,))]

        new_attrs = [(key, val) for key, val in attrs.items()
                      if (key, val) not in tiles]

        tile_list = []

        # For each tile
        for key, val in tiles:
            tile_list.append(val)

        # Add the list of tiles to the new class
        new_attrs.append(('_tiles', tile_list))

        return super().__new__(cls, name, bases, dict(new_attrs))


class TileSet(metaclass=MetaSet):
    """
    A tileset funnily enough is the counterpart to a tiled image,
    it's how you define what it is you are going to draw onto said
    image.

    NOTE: You do not use TileSet directly! Instead create a class
    which inherits from this one!
    """

    def __init__(self, FPS=25):
        self._FPS = FPS

    def __getitem__(self, key):

        if isinstance(key, (int,)):
            frame = key
            time = key / self._FPS

        if isinstance(key, (float,)):
            frame = floor(key * self._FPS)
            time = key

        layout = self.layout(frame, time)

        return (self._tiles, layout)

    def layout(self, frame, time):
        """
        This implements the default layout, which simply
        displays all available tiles in a grid
        """

        num_tiles = len(self._tiles)

        # Find out what the dimension of the grid will be
        N = ceil(sqrt(num_tiles))

        # Make that many Nones
        nones = [None for _ in range(N*N)]

        # Replace with the appropriate numbers
        nones[:num_tiles] = range(num_tiles)

        # Finally convert to numpy array and
        # make it 2D
        grid = np.array(nones, dtype='O')
        return grid.reshape(N, N)


def write(text, charset, font):
    """
    This is a VERY naive and basic implementation of taking a
    string and converting it to an appropriate drawable. It
    pays no attension to anything like text wrapping etc.

    Arguments:
    ----------

    text: str
        The text you actually want written.
    charset: str
        A string containing the characters which comprise
        of the alphabet your text is written in
    font: TileSet
        The class which defines the font the text is to
        be written in
    """

    chars = [charset.find(t) for t in text]

    def layout(frame, time):
        return np.array([chars])

    inscription = font()
    inscription.layout = layout

    return inscription
