import json

import arlunio as ar
import numpy as np
import py.test

from arlunio._shapes import Collection, Key


class TestShape:
    """Tests for the `st.shape` decorator and the base `Shape` class."""

    def test_name(self):
        """Ensure that the returned shape keeps the name of the decorated function."""

        @ar.shape
        def Circle(x, y):
            pass

        assert Circle.__name__ == "Circle"

    def test_parameter_names(self):
        """Ensure that the positional arguments are exposed as parameters."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0):
            pass

        assert Circle.parameters == set(["x", "y"])

    def test_property_names(self):
        """Ensure that the keyword only arguments are exposed as properties."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0):
            pass

        assert Circle().properties == {"x0": 0, "y0": 0}

    def test_default(self):
        """Ensure that a shape inherits its defaults from the decorated function."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0.5, r=1.2):
            pass

        c1 = Circle()

        assert c1.x0 == 0
        assert c1.y0 == 0.5
        assert c1.r == 1.2

    def test_default_overrides(self):
        """Ensure that we can override any of the defaults."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=1, r=0.4):
            pass

        c1 = Circle(x0=1, y0=2, r=3)

        assert c1.x0 == 1
        assert c1.y0 == 2
        assert c1.r == 3

    def test_property_validation(self):
        """Ensure that the shape can perform validation based on given type
        annotations."""

        @ar.shape
        def Circle(x, y, *, x0: float = 0, y0=0):
            pass

        with py.test.raises(TypeError):
            Circle(x0="hi")

    def test_draw(self):
        """Ensure that we can draw a shape and produce an image."""

        @ar.shape
        def Circle(x, y, *, r=0.8):
            return np.sqrt(x * x + y * y) < r * r

        c1 = Circle()

        expected = np.full((4, 4, 3), (255, 255, 255), dtype=np.uint8)
        expected[1, 1] = (0, 0, 0)
        expected[1, 2] = (0, 0, 0)
        expected[2, 1] = (0, 0, 0)
        expected[2, 2] = (0, 0, 0)

        assert (expected == c1(4, 4).pixels).all()

    def test_draw_tuple(self):
        """Ensure that we can draw a shape, specifying the dimensions with a
        tuple."""

        @ar.shape
        def Circle(x, y, *, r=0.8):
            return np.sqrt(x * x + y * y) < r * r

        c1 = Circle()

        expected = np.full((4, 4, 3), (255, 255, 255), dtype=np.uint8)
        expected[1, 1] = (0, 0, 0)
        expected[1, 2] = (0, 0, 0)
        expected[2, 1] = (0, 0, 0)
        expected[2, 2] = (0, 0, 0)

        resolution = (4, 4)
        assert (expected == c1(resolution).pixels).all()

    def test_mask_single(self):
        """Ensure that we can use the shape to test a single point."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0):
            xc = x - x0
            yc = y - y0

            return np.sqrt(xc * xc + yc * yc) < 1

        c1 = Circle()

        assert c1(x=0, y=0)
        assert not c1(x=1, y=0)

    def test_mask_array(self):
        """Ensure that we can use the shape to test a numpy array of points."""

        @ar.shape
        def Circle(x, y):
            return np.sqrt(x * x + y * y) < 1

        c1 = Circle()
        xs = np.array([0, 1, 0])
        ys = np.array([0, 0, 1])

        assert (np.array([True, False, False]) == c1(x=xs, y=ys)).all()

    def test_mask_checks_params(self):
        """Ensure that the shape checks that it has been given all the required
        parameters."""

        @ar.shape
        def Circle(x, y):
            return np.sqrt(x * x + y * y) < 1

        c1 = Circle()

        with py.test.raises(TypeError) as err:
            c1(x=0)

        assert "y" in str(err.value)

    def test_to_json(self):
        """Ensure that we can convert a shape to a Json representation."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0, r=0.8):
            pass

        c1 = Circle(x0=1, y0=2, r=3)

        expected = {
            "name": "Circle",
            "color": "#000000",
            "scale": 1,
            "properties": {"x0": 1, "y0": 2, "r": 3},
        }

        assert expected == json.loads(c1.json)

    def test_from_json(self):
        """Ensure that we can create a shape from its Json representation."""

        @ar.shape
        def Circle(x, y, *, x0=0, y0=0, r=0.5):
            pass

        d = {"name": "Circle", "properties": {"x0": 1, "y0": 2, "r": 3}}

        src = json.dumps(d)
        c1 = Circle.from_json(src)

        assert c1.x0 == 1
        assert c1.y0 == 2
        assert c1.r == 3

    def test_from_json_missing_name(self):
        """Ensure that we check for the `name` field."""

        @ar.shape
        def Circle(x, y):
            pass

        src = '{"properties": []}'

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "name" in str(err.value)

    def test_from_json_missing_properties(self):
        """Ensure that we check for the `properties` field."""

        @ar.shape
        def Circle(x, y):
            pass

        src = '{"name": ""}'

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "properties" in str(err.value)

    def test_from_json_bad_name(self):
        """Ensure that if we try to parse a representation for a different shape we
        throw an error."""

        @ar.shape
        def Circle(x, y):
            pass

        d = {"name": "Square", "properties": []}
        src = json.dumps(d)

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "Circle" in str(err.value)

    def test_from_json_property_missing_name(self):
        """Ensure that if a property doesn't provide a name we throw an error."""

        @ar.shape
        def Circle(x, y):
            pass

        d = {"name": "Circle", "properties": [{"value": 23}]}
        src = json.dumps(d)

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "name" in str(err.value)

    def test_from_json_property_missing_value(self):
        """Ensure that if a property doesn't provide a value we throw an error."""

        @ar.shape
        def Circle(x, y):
            pass

        d = {"name": "Circle", "properties": [{"name": "x0"}]}
        src = json.dumps(d)

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "value" in str(err.value)

    def test_from_json_bad_property_name(self):
        """Ensure that if we encounter an unexpected property we throw an error."""

        @ar.shape
        def Circle(x, y, *, x0=0):
            pass

        d = {"name": "Circle", "properties": [{"name": "p", "value": 34}]}
        src = json.dumps(d)

        with py.test.raises(TypeError) as err:
            Circle.from_json(src)

        assert "p" in str(err.value)


@py.test.mark.parametrize(
    "items,key,expected",
    [({"Circle": 1}, "Circle", 1), ({"Circle": 1, "lib.Square": 2}, "Square", 2)],
)
def test_collection_getattr(items, key, expected):
    """Ensure that we can access items"""

    collection = Collection(items={Key.fromstring(k): v for k, v in items.items()})
    assert getattr(collection, key) == expected


def test_collection_getattr_qualified():
    """Ensure that the user can qualify an ambiguous reference."""

    shapes = {"Square": 1, "lib.Circle": 2, "ext.Circle": 3}
    collection = Collection(items={Key.fromstring(k): v for k, v in shapes.items()})

    assert collection.lib.Circle == 2
    assert collection.ext.Circle == 3


def test_collection_getattr_ambiguous():
    """Ensure that if a reference is ambiguous we throw an error."""

    shapes = {"std.Circle": 1, "ext.Circle": 3}
    collection = Collection(items={Key.fromstring(k): v for k, v in shapes.items()})

    with py.test.raises(AttributeError) as err:
        collection.Circle

    assert "Ambiguous" in str(err.value)
    assert "Circle" in str(err.value)


def test_collection_getattr_not_found():
    """Ensure that if there is no match for a reference we throw an error."""

    shapes = {"Circle": 1}
    collection = Collection(items={Key.fromstring(k): v for k, v in shapes.items()})

    with py.test.raises(AttributeError) as err:
        collection.Square

    assert "No item" in str(err.value)
    assert "Square" in str(err.value)
