"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Frustum as OMFrustum
from fairgraph import KGEmbedded


from numbers import Real


class Frustum(KGEmbedded, OMFrustum):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Frustum"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("base_distance", "major_base_shape", "minor_base_scale")

    def __init__(
        self,
        base_distance=None,
        major_base_shape=None,
        minor_base_scale=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            base_distance=base_distance,
            major_base_shape=major_base_shape,
            minor_base_scale=minor_base_scale,
        )
