from stylo.render.renderer import Renderer, get_coordinate_string


class SimpleRenderer(Renderer):
    """As simple as they come, this renderer simply takes a mask function and
    applies it to the given domain."""

    def render(self, domain, definition, width, height):
        coordinates = get_coordinate_string(definition)
        values = domain[coordinates](width, height)

        return definition(*values)
