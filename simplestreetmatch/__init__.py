import sys

if sys.version_info [0] < 3:
    from streetcollection import StreetCollection
else:
    from .streetcollection import StreetCollection

