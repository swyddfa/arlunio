"""Specific hypothesis strategies that are useful for testing.

It defines the following strategies:

- :code:`dimension`: Represents a size or dimension e.g. for numpy arrays image
  sizes etc.
"""
from hypothesis.strategies import integers


dimension = integers(min_value=2, max_value=1024)
