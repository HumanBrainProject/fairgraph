"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import SingleColor as OMSingleColor
from fairgraph import KGObject


class SingleColor(KGObject, OMSingleColor):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SingleColor"
    default_space = "atlas"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("value",)

    def __init__(self, value=None, id=None, data=None, space=None, release_status=None):
        return KGObject.__init__(self, id=id, space=space, release_status=release_status, data=data, value=value)
