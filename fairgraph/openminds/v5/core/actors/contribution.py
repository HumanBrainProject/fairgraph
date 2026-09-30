"""
Structured information on the contribution made to a research product.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Contribution as OMContribution
from fairgraph import KGEmbedded


class Contribution(KGEmbedded, OMContribution):
    """
    Structured information on the contribution made to a research product.
    """

    type_ = "https://openminds.om-i.org/types/Contribution"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("contributors", "type")

    def __init__(self, contributors=None, type=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, contributors=contributors, type=type)
