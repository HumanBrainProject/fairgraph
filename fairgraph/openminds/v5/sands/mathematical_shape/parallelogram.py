"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Parallelogram as OMParallelogram
from fairgraph import KGEmbedded


class Parallelogram(KGEmbedded, OMParallelogram):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Parallelogram"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("base_distance", "base_length", "interior_angle")

    def __init__(
        self,
        base_distance=None,
        base_length=None,
        interior_angle=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self, data=data, base_distance=base_distance, base_length=base_length, interior_angle=interior_angle
        )
