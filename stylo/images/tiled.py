import numpy as np
from math import floor, ceil, sqrt

from stylo.drawable import Domain, Drawable

from .image import Image


class TiledImage(Image):
    """
    This builds on the base image class, to allow easy creation of
    images from tilesets. Useful for constructing backgrounds based
    on a grid - e.g level designs etc.
    """

    def __init__(self, width, height, xmax=10, ymax=10,
                 xmin=0, ymin=0, *args, **kwargs):

        # First call the parent to set things up
        super().__init__(width, height, *args, **kwargs)

        # Now we will set up the domain for the image
        self._xmin = xmin
        self._xmax = xmax

        self._ymin = ymin
        self._ymax = ymax

        self.domain = Domain(xmin, xmax, ymin, ymax)

    def __call__(self, tileset, overwrite_domain=False):
        """
        This allows for the possibility of easy application
        of a tileset to the Image, but bog standard drawables
        are still ok.
        """

        # Are we dealing with a drawable?
        if isinstance(tileset, (Drawable,)):

            # If so do the "normal" thing
            super().__call__(tileset, overwrite_domain)
            return

        if isinstance(tileset, (TileSet,)):

            # Here we assume that the tileset is not time dependent
            # so just call the layout method with some, argument
            layout = tileset.layout(0, 0)
            tiles = tileset._tiles

        elif isinstance(tileset, (tuple,)):

            # Here we assume that we have been given a time dependent
            # tileset
            tiles, layout = tileset

        else:
            raise TypeError('TiledImages only support Drawables and '
                            'TileSets!!')

        # With that out of the way let's get down to it. First let's check
        # that the given tileset makes sense

        # Numpy freaks out if we try to .unique() an array containing None's
        # So just turn them into zeros, as a tileset will always have a
        # zeroth tile
        tozero = lambda v: v if v is not None else 0
        vtoz = np.vectorize(tozero)
        test_layout = vtoz(layout)

        if len(tiles) < len(np.unique(test_layout)):
            raise ValueError('The layout defined references more tiles '
                             'than are defined!')

        # Transpose the layout array so that it makes sense to the user
        layout = layout.transpose()

        # Next we need to decide on the size of each of the grid squares
        nx, ny = layout.shape
        xsize = (self.xmax - self.xmin) / nx
        ysize = (self.ymax - self.ymin) / ny

        # Now we go through each tile in the layout and apply it to the
        # image
        for j in range(ny):

            ystart = self.ymin + j*ysize
            yend = ystart + ysize

            for i in range(nx):
                xstart = self.xmin + i*xsize
                xend = xstart + xsize

                tileidx = layout[i, j]

                if tileidx is not None:
                    tile = tiles[tileidx]
                    self[xstart:xend, ystart:yend](tile)

    @property
    def xmin(self):
        return self._xmin

    @xmin.setter
    def xmin(self, value):

        if not isinstance(value, (int, float)):
            raise TypeError('xmin must be a number!')

        if value >= self.xmax:
            raise ValueError('xmin cannot be larger than xmax!')

        self._xmin = value
        self.domain = Domain(value, self.xmax, self.ymin, self.ymax)

    @property
    def xmax(self):
        return self._xmax

    @xmax.setter
    def xmax(self, value):

        if not isinstance(value, (int, float)):
            raise TypeError('xmax must be a number!')

        if value <= self.xmin:
            raise ValueError('xmax cannot be less than xmin!')

        self._xmin = value
        self.domain = Domain(self.xmin, value, self.ymin, self.ymax)

    @property
    def ymin(self):
        return self._ymin

    @ymin.setter
    def ymin(self, value):

        if not isinstance(value, (int, float)):
            raise TypeError('ymax must be a number!')

        if value >= self.ymax:
            raise ValueError('ymin cannot be larger than ymax!')

        self._ymin = value
        self.domain = Domain(self.xmin, self.xmax, value, self.ymax)

    @property
    def ymax(self):
        return self._ymax

    @ymax.setter
    def ymax(self, value):

        if not isinstance(value, (int, float)):
            raise TypeError('ymax must be a number!')

        if value <= self.ymin:
            raise ValueError('ymax cannot be less than ymin!')

        self._ymax = value
        self.domain = Domain(self.xmin, self.xmax, self.ymin, value)


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
