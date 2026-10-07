"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import SpecimenWeight as OMSpecimenWeight
from fairgraph import KGEmbedded


class SpecimenWeight(KGEmbedded, OMSpecimenWeight):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SpecimenWeight"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("type", "weight")

    def __init__(self, type=None, weight=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, type=type, weight=weight)
