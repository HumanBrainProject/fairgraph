"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Spheroid as OMSpheroid
from fairgraph import KGEmbedded


class Spheroid(KGEmbedded, OMSpheroid):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Spheroid"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("equatorial_diameter", "polar_diameter")

    def __init__(
        self, equatorial_diameter=None, polar_diameter=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, equatorial_diameter=equatorial_diameter, polar_diameter=polar_diameter
        )
