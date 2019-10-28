import logging
import tkinter as tk

from typing import Any

import attr

from PIL import ImageTk

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

        self._items = []
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

        logger.debug("Resizing canvas %s x %s", self.width, self.height)
        self.config(width=self.width, height=self.height)

        cx, cy = self.width / 2, self.height / 2

        for item in self._items:
            img = item.source(self.width, self.height)._as_pillow_image()
            item.tk = ImageTk.PhotoImage(img)
            self.coords(item.canvas, cx, cy)
            self.itemconfig(item.canvas, image=item.tk)

    def add_item(self, item):

        canvas_item = CanvasItem(source=item)

        img = item(self.width, self.height)._as_pillow_image()
        canvas_item.tk = ImageTk.PhotoImage(img)

        cx, cy = self.width / 2, self.height / 2
        canvas_item.canvas = self.create_image(cx, cy, image=canvas_item.tk)
        self._items.append(canvas_item)


class ImageViewer(tk.Frame):
    """A component dedicated to displaying images"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.canvas = ArlunioCanvas(self, width=640, height=480)
        self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

    def add_item(self, item):
        self.canvas.add_item(item)
