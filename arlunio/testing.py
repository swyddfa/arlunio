from hypothesis.strategies import floats, integers

pve_num = floats(min_value=1, max_value=1e6)
real_num = floats(min_value=-1e6, max_value=1e6)

dimension = integers(min_value=4, max_value=512)
