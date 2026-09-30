"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import RegularPolygon as OMRegularPolygon
from fairgraph import KGEmbedded


class RegularPolygon(KGEmbedded, OMRegularPolygon):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/RegularPolygon"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("circumradius", "number_of_sides")

    def __init__(self, circumradius=None, number_of_sides=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, circumradius=circumradius, number_of_sides=number_of_sides)
