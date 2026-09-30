"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Square as OMSquare
from fairgraph import KGEmbedded


class Square(KGEmbedded, OMSquare):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Square"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("side_length",)

    def __init__(self, side_length=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, side_length=side_length)
