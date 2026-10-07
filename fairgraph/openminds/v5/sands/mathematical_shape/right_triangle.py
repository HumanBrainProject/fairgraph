"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import RightTriangle as OMRightTriangle
from fairgraph import KGEmbedded


class RightTriangle(KGEmbedded, OMRightTriangle):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/RightTriangle"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("perpendicular_leg_lengths",)

    def __init__(self, perpendicular_leg_lengths=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, perpendicular_leg_lengths=perpendicular_leg_lengths)
