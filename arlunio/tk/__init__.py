import logging

import arlunio as ar

from .components import ImageViewer

try:
    import tkinter as tk
    import tkinter.ttk as ttk

    TK = True
except ImportError:
    import unittest.mock as mock

    tk = mock.MagicMock()
    ttk = mock.MagicMock()

    TK = False


logger = logging.getLogger(__name__)


class ShapeDesigner(tk.Frame):
    """UI for designing new shapes"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.viewer = ImageViewer(self)
        self.viewer.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)
        self.viewer.set_item(ar.S.Circle())
        self.shapes = {s.__name__: s for s in ar.S._items.values()}

        self.shape_picker = ttk.Combobox(self, values=list(self.shapes.keys()))
        self.shape_picker.pack(side=tk.TOP)
        self.shape_picker.current(0)
        self.shape_picker.bind("<<ComboboxSelected>>", self.render_shape)

    def render_shape(self, event):
        logger.debug(event)
        name = self.shape_picker.get()
        shape = self.shapes[name]()

        self.viewer.set_item(shape)


class Shapes:
    """Launches a simple shape previewer."""

    def run(self):

        if not TK:
            logger.info(
                "It appears that tkinter is not available on your system but "
                "is required for this command. Please ensure it is available "
                "and try again "
            )
            return 1

        root = tk.Tk()
        app = ShapeDesigner(root)
        app.mainloop()
