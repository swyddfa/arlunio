import sys

major, minor, *_ = sys.version_info
assert (major, minor) >= (3, 6)

print("{}.{}".format(major, minor))
