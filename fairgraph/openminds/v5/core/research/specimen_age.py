"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import SpecimenAge as OMSpecimenAge
from fairgraph import KGEmbedded


class SpecimenAge(KGEmbedded, OMSpecimenAge):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SpecimenAge"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("age", "reference")

    def __init__(self, age=None, reference=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, age=age, reference=reference)
