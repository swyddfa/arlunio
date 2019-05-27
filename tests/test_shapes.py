import stylo as st


class TestShape:
    """Tests for the `st.shape` decorator."""

    def test_name(self):
        """Ensure that the returned shape keeps the name of the decorated
        function."""

        @st.shape
        def MyShape(x, y):
            pass

        assert MyShape.__name__ == "MyShape"
