"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import GeoCoordinates as OMGeoCoordinates
from fairgraph import KGEmbedded


from numbers import Real


class GeoCoordinates(KGEmbedded, OMGeoCoordinates):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/GeoCoordinates"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("latitude", "longitude")

    def __init__(
        self, elevation=None, latitude=None, longitude=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, elevation=elevation, latitude=latitude, longitude=longitude)
