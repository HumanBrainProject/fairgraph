"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Rectangle as OMRectangle
from fairgraph import KGEmbedded


class Rectangle(KGEmbedded, OMRectangle):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Rectangle"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("major_side_length", "minor_side_length")

    def __init__(
        self, major_side_length=None, minor_side_length=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, major_side_length=major_side_length, minor_side_length=minor_side_length
        )
