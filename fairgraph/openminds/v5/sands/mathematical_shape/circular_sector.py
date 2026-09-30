"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import CircularSector as OMCircularSector
from fairgraph import KGEmbedded


class CircularSector(KGEmbedded, OMCircularSector):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CircularSector"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("central_angle", "radius")

    def __init__(self, central_angle=None, radius=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, central_angle=central_angle, radius=radius)
