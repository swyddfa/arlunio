import logging

from typing import Any

import attr

try:
    import tkinter as tk
    from PIL import ImageTk
except ImportError:
    import unittest.mock as mock

    tk = mock.MagicMock()


logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class CanvasItem:

    source: Any = None
    """Represents the source of truth for the item"""

    tk: Any = None
    """The tk representation of the item"""

    canvas: Any = None
    """The canvas representation of the item"""


class ArlunioCanvas(tk.Canvas):
    """A canvas object, capable of display arlunio related items"""

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.bind("<Configure>", self.on_resize)

        self._item = None
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

        logger.debug("Resizing canvas %s x %s", self.width, self.height)
        self.config(width=self.width, height=self.height)

        cx, cy = self.width / 2, self.height / 2

        img = self._item.source(self.width, self.height)._as_pillow_image()
        self._item.tk = ImageTk.PhotoImage(img)
        self.coords(self._item.canvas, cx, cy)
        self.itemconfig(self._item.canvas, image=self._item.tk)

    def set_item(self, item):
        canvas_item = CanvasItem(source=item)

        img = item(self.width, self.height)._as_pillow_image()
        canvas_item.tk = ImageTk.PhotoImage(img)

        cx, cy = self.width / 2, self.height / 2
        canvas_item.canvas = self.create_image(cx, cy, image=canvas_item.tk)
        self._item = canvas_item


class ImageViewer(tk.Frame):
    """A component dedicated to displaying images"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.canvas = ArlunioCanvas(self, width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

    def set_item(self, item):
        self.canvas.set_item(item)
