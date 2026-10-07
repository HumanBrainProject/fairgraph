"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import CoordinatePoint as OMCoordinatePoint
from fairgraph import KGEmbedded


class CoordinatePoint(KGEmbedded, OMCoordinatePoint):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CoordinatePoint"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("coordinate_framework", "coordinates")

    def __init__(
        self, coordinate_framework=None, coordinates=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, coordinate_framework=coordinate_framework, coordinates=coordinates)
