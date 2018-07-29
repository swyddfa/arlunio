"""Specific hypothesis strategies that are useful for testing.

It defines the following strategies:

- :code:`dimension`: Represents a size or dimension e.g. for numpy arrays image
  sizes etc.
- :code:`real`: Represents a real number in the range +/-1 million
"""
from hypothesis.strategies import integers, floats

real = floats(min_value=-1e6, max_value=1e6)
dimension = integers(min_value=2, max_value=1024)
