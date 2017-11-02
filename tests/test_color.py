from pytest import raises
from hypothesis import given
from hypothesis.strategies import from_regex


from stylo.color import hexcolor


# Some useful strategies
rgb = from_regex('\A[0-9a-fA-F]{6}\Z')
rgba = from_regex('\A[0-9a-fA-F]{8}\Z')


class TestHexColor(object):

    @given(code=rgb)
    def test_with_rgb(self, code):

        col = hexcolor(code)
        assert len(col) == 3

        r, g, b = col
        assert 0 <= r and r <= 255
        assert 0 <= b and b <= 255
        assert 0 <= g and g <= 255

    @given(code=rgba)
    def test_with_rgba(self, code):

        col = hexcolor(code)
        assert len(col) == 4

        r, g, b, a = col
        assert 0 <= r and r <= 255
        assert 0 <= b and b <= 255
        assert 0 <= g and g <= 255
        assert 0 <= a and a <= 255

    @given(code=rgb)
    def test_with_rgb_and_alpha(self, code):

        col = hexcolor(code, alpha=True)
        assert len(col) == 4

        r, g, b, a = col
        assert 0 <= r and r <= 255
        assert 0 <= b and b <= 255
        assert 0 <= g and g <= 255
        assert 0 <= a and a <= 255

    def test_with_bad_values(self):

        with raises(TypeError) as err:
            hexcolor(234)

        assert 'must be a string' in str(err.value)

        with raises(ValueError) as err:
            hexcolor('baadcolor3')

        assert 'does not match a known color code format' in str(err.value)
