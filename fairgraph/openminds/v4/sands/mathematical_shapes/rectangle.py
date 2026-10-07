"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import Rectangle as OMRectangle
from fairgraph import KGEmbedded


class Rectangle(KGEmbedded, OMRectangle):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Rectangle"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("length", "width")

    def __init__(self, length=None, width=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, length=length, width=width)
