"""
Structured information about a relationship between two entities, such as a person and their employer.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Affiliation as OMAffiliation
from fairgraph import KGEmbedded


class Affiliation(KGEmbedded, OMAffiliation):
    """
    Structured information about a relationship between two entities, such as a person and their employer.
    """

    type_ = "https://openminds.om-i.org/types/Affiliation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("organizations", "person")

    def __init__(self, organizations=None, person=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, organizations=organizations, person=person)
