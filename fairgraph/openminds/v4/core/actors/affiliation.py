"""
Structured information about a relationship between two entities, such as a person and their employer.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Affiliation as OMAffiliation
from fairgraph import KGEmbedded


from datetime import date


class Affiliation(KGEmbedded, OMAffiliation):
    """
    Structured information about a relationship between two entities, such as a person and their employer.
    """

    type_ = "https://openminds.om-i.org/types/Affiliation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("member_of",)

    def __init__(
        self, end_date=None, member_of=None, start_date=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, end_date=end_date, member_of=member_of, start_date=start_date)
