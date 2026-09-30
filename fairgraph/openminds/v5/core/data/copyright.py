"""
Structured information on the copyright.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Copyright as OMCopyright
from fairgraph import KGEmbedded


class Copyright(KGEmbedded, OMCopyright):
    """
    Structured information on the copyright.
    """

    type_ = "https://openminds.om-i.org/types/Copyright"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("holders", "years")

    def __init__(
        self, custom_usage_clause=None, holders=None, years=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, custom_usage_clause=custom_usage_clause, holders=holders, years=years
        )
