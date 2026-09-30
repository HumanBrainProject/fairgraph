"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Location as OMLocation
from fairgraph import KGEmbedded


class Location(KGEmbedded, OMLocation):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Location"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("country",)

    def __init__(
        self, address=None, country=None, geo_coordinates=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, address=address, country=country, geo_coordinates=geo_coordinates)
