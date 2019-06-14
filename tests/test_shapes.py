import json

import numpy as np
import pytest
import stylo as st


class TestShape:
    """Tests for the `st.shape` decorator and the base `Shape` class."""

    @pytest.fixture()
    def circle(self):
        @st.shape
        def Circle(x, y, *, x0=0, y0=0, r=0.8):
            xc = x - x0
            yc = y - y0

            return np.sqrt(xc * xc + yc * yc) < r * r

        return Circle

    def test_name(self, circle):
        """Ensure that the returned shape keeps the name of the decorated function."""
        assert circle.__name__ == "Circle"

    def test_parameters(self, circle):
        """Ensure that the positional arguments are exposed as parameters."""
        assert circle.parameters == set(["x", "y"])

    def test_defaults(self, circle):
        """Ensure that a shape inherits its defaults from the decorated function."""

        c1 = circle()

        assert c1.x0 == 0
        assert c1.y0 == 0
        assert c1.r == 0.8

    def test_default_overrides(self, circle):
        """Ensure that we can override any of the defaults."""

        c1 = circle(x0=1, y0=2, r=3)

        assert c1.x0 == 1
        assert c1.y0 == 2
        assert c1.r == 3

    def test_setting_properties(self, circle):
        """Ensure that if we set a property the internal dict is updated."""

        c1 = circle()
        c1.x0 = 2

        assert c1._properties["x0"] == 2

    def test_draw(self, circle):
        """Ensure that we can draw a shape and produce an image."""

        c1 = circle()

        expected = np.full((4, 4, 3), (255, 255, 255), dtype=np.uint8)
        expected[1, 1] = (0, 0, 0)
        expected[1, 2] = (0, 0, 0)
        expected[2, 1] = (0, 0, 0)
        expected[2, 2] = (0, 0, 0)

        assert (expected == c1(4, 4).pixels).all()

    def test_mask_single(self, circle):
        """Ensure that we can use the shape to test a single point."""

        c1 = circle()

        assert c1(x=0, y=0)
        assert not c1(x=1, y=0)

    def test_mask_array(self, circle):
        """Ensure that we can use the shape to test a numpy array of points."""

        c1 = circle()
        xs = np.array([0, 1, 0])
        ys = np.array([0, 0, 1])

        assert (np.array([True, False, False]) == c1(x=xs, y=ys)).all()

    def test_mask_checks_params(self, circle):
        """Ensure that the shape checks that it has been given all the required
        parameters."""

        c1 = circle()

        with pytest.raises(TypeError) as err:
            c1(x=0)

        assert "y" in str(err.value)

    def test_to_json(self, circle):
        """Ensure that we can convert a shape to a Json representation."""

        c1 = circle(x0=1, y0=2, r=3)

        expected = {
            "name": "Circle",
            "color": "#000000",
            "parameters": ["x", "y"],
            "properties": [
                {"name": "x0", "value": 1},
                {"name": "y0", "value": 2},
                {"name": "r", "value": 3},
            ],
        }

        assert expected == json.loads(c1.json)

    def test_from_json(self, circle):
        """Ensure that we can create a shape from its Json representation."""

        d = {
            "name": "Circle",
            "properties": [
                {"name": "x0", "value": 1},
                {"name": "y0", "value": 2},
                {"name": "r", "value": 3},
            ],
        }

        src = json.dumps(d)
        c1 = circle.fromjson(src)

        assert c1.x0 == 1
        assert c1.y0 == 2
        assert c1.r == 3

    def test_from_json_missing_name(self, circle):
        """Ensure that we check for the `name` field."""

        src = '{"properties": []}'

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "name" in str(err.value)

    def test_from_json_missing_properties(self, circle):
        """Ensure that we check for the `properties` field."""

        src = '{"name": ""}'

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "properties" in str(err.value)

    def test_from_json_bad_name(self, circle):
        """Ensure that if we try to parse a representation for a different shape we
        throw an error."""

        d = {"name": "Square", "properties": []}
        src = json.dumps(d)

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "Circle" in str(err.value)

    def test_from_json_property_missing_name(self, circle):
        """Ensure that if a property doesn't provide a name we throw an error."""

        d = {"name": "Circle", "properties": [{"value": 23}]}
        src = json.dumps(d)

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "name" in str(err.value)

    def test_from_json_property_missing_value(self, circle):
        """Ensure that if a property doesn't provide a value we throw an error."""

        d = {"name": "Circle", "properties": [{"name": "x0"}]}
        src = json.dumps(d)

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "value" in str(err.value)

    def test_from_json_bad_property_name(self, circle):
        """Ensure that if we encounter an unexpected property we throw an error."""

        d = {"name": "Circle", "properties": [{"name": "p", "value": 34}]}
        src = json.dumps(d)

        with pytest.raises(TypeError) as err:
            circle.fromjson(src)

        assert "p" in str(err.value)
