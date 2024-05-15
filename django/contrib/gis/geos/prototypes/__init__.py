"""
 This module contains all of the GEOS ctypes function prototypes. Each
 prototype handles the interaction between the GEOS library and Python
 via ctypes.
"""

from django.contrib.gis.geos.prototypes.coordseq import (
    create_cs,  # NOQA
    )
from django.contrib.gis.geos.prototypes.geom import (
    create_collection,  # NOQA
    )
from django.contrib.gis.geos.prototypes.misc import *  # NOQA
from django.contrib.gis.geos.prototypes.predicates import (  # NOQA
    geos_contains,
    geos_covers,
    geos_crosses,
    geos_disjoint,
    geos_equals,
    geos_equalsexact,
    geos_equalsidentical,
    geos_hasz,
    geos_intersects,
    geos_isclosed,
    geos_isempty,
    geos_isring,
    geos_issimple,
    geos_isvalid,
    geos_overlaps,
    geos_relatepattern,
    geos_touches,
    geos_within,
)
from django.contrib.gis.geos.prototypes.topology import *  # NOQA
