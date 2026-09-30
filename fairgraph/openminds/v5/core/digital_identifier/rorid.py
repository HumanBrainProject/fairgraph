"""
A persistent identifier for a research organization, provided by the Research Organization Registry.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import RORID as OMRORID
from fairgraph import KGObject


class RORID(KGObject, OMRORID):
    """
    A persistent identifier for a research organization, provided by the Research Organization Registry.
    """

    type_ = "https://openminds.om-i.org/types/RORID"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            "openminds.v5.core.Organization",
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
