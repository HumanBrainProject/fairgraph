"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import Ellipse as OMEllipse
from fairgraph import KGEmbedded


class Ellipse(KGEmbedded, OMEllipse):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Ellipse"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("semi_major_axis", "semi_minor_axis")

    def __init__(
        self, semi_major_axis=None, semi_minor_axis=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, semi_major_axis=semi_major_axis, semi_minor_axis=semi_minor_axis)
