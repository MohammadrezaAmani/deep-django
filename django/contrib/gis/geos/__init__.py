"""
The GeoDjango GEOS module.  Please consult the GeoDjango documentation
for more details: https://docs.djangoproject.com/en/dev/ref/contrib/gis/geos/
"""

from .collections import (
    MultiLineString,  # NOQA
    )
from .error import GEOSException  # NOQA
from .factory import fromfile, fromstr  # NOQA
from .geometry import GEOSGeometry, hex_regex, wkt_regex  # NOQA
from .io import WKBReader, WKBWriter, WKTReader, WKTWriter  # NOQA
from .libgeos import geos_version  # NOQA
from .linestring import LinearRing, LineString  # NOQA
from .point import Point  # NOQA
from .polygon import Polygon  # NOQA
