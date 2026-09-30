"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Ellipse as OMEllipse
from fairgraph import KGEmbedded


class Ellipse(KGEmbedded, OMEllipse):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Ellipse"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("diameters",)

    def __init__(self, diameters=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, diameters=diameters)
