from stylo.color.colormap import ColorMap


class FillColor(ColorMap):
    def __init__(self, color=None, colorspace=None):
        super().__init__(colorspace)

        if color is None:
            color = "000000"

        self.color = self._parse_color(color)

    def _paint(self, shape, image_data):

        image_data[shape] = self.color
        return image_data
