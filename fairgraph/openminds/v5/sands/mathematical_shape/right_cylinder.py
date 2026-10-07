"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import RightCylinder as OMRightCylinder
from fairgraph import KGEmbedded


class RightCylinder(KGEmbedded, OMRightCylinder):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/RightCylinder"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("base_distance", "base_shape")

    def __init__(self, base_distance=None, base_shape=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, base_distance=base_distance, base_shape=base_shape)
