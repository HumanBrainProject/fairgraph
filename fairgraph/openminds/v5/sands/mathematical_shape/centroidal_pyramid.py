"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import CentroidalPyramid as OMCentroidalPyramid
from fairgraph import KGEmbedded


class CentroidalPyramid(KGEmbedded, OMCentroidalPyramid):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CentroidalPyramid"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("apex_base_distance", "base_shape")

    def __init__(self, apex_base_distance=None, base_shape=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, apex_base_distance=apex_base_distance, base_shape=base_shape)
