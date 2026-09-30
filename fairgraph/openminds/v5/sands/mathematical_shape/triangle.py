"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Triangle as OMTriangle
from fairgraph import KGEmbedded


class Triangle(KGEmbedded, OMTriangle):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Triangle"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("apex_angle", "leg_lengths")

    def __init__(self, apex_angle=None, leg_lengths=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, apex_angle=apex_angle, leg_lengths=leg_lengths)
