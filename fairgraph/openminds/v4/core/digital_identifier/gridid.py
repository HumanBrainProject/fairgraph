"""
A GRID (Global Research Identifier Database) identifier.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import GRIDID as OMGRIDID
from fairgraph import KGObject


class GRIDID(KGObject, OMGRIDID):
    """
    A GRID (Global Research Identifier Database) identifier.
    """

    type_ = "https://openminds.om-i.org/types/GRIDID"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            "openminds.v4.core.Organization",
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
