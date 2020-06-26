"""Helpers and utilities for writing tests."""
import hypothesis.strategies as st
import numpy as np
from hypothesis.extra import numpy

pve_num = st.floats(min_value=1, max_value=1e6)
real_num = st.floats(min_value=-1e6, max_value=1e6)

dimension = st.integers(min_value=4, max_value=512)

mask = numpy.arrays(
    dtype=np.bool_, shape=st.tuples(dimension, dimension), fill=st.booleans()
)
