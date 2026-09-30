"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import IdentifiersDotOrgID as OMIdentifiersDotOrgID
from fairgraph import KGObject


class IdentifiersDotOrgID(KGObject, OMIdentifiersDotOrgID):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/IdentifiersDotOrgID"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            ["openminds.v4.core.Dataset", "openminds.v4.core.DatasetVersion"],
            "digitalIdentifier",
            reverse="digital_identifier",
            multiple=True,
            description="reverse of 'digital_identifier'",
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
