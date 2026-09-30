"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Ellipsoid as OMEllipsoid
from fairgraph import KGEmbedded


class Ellipsoid(KGEmbedded, OMEllipsoid):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Ellipsoid"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("intermediate_diameter", "major_diameter", "minor_diameter")

    def __init__(
        self,
        intermediate_diameter=None,
        major_diameter=None,
        minor_diameter=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            intermediate_diameter=intermediate_diameter,
            major_diameter=major_diameter,
            minor_diameter=minor_diameter,
        )
