"""
A persistent identifier for a researcher provided by Open Researcher and Contributor ID, Inc.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ORCID as OMORCID
from fairgraph import KGObject


class ORCID(KGObject, OMORCID):
    """
    A persistent identifier for a researcher provided by Open Researcher and Contributor ID, Inc.
    """

    type_ = "https://openminds.om-i.org/types/ORCID"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            "openminds.v4.core.Person",
            "digitalIdentifier",
            reverse="digital_identifiers",
            multiple=True,
            description="reverse of 'digital_identifiers'",
        ),
    ]
    existence_query_properties = ("identifier",)

    def __init__(self, identifier=None, identifies=None, id=None, data=None, space=None, release_status=None):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            identifier=identifier,
            identifies=identifies,
        )
