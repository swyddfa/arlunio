from .coords import cartesian, extend_periodically, translate, reflect,\
                    polar, mk_domain
from .color import hex_to_rgb
from .image import Image, LayeredImage, TiledImage
from .motion import Projectile
from .objects import TileSet
#from .prims import between, circle, ellipse, rectangle, square,\
#                   Puppet
from .time import animate

from .version import __version__
