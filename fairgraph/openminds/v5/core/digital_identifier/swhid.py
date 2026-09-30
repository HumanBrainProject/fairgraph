"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import SWHID as OMSWHID
from fairgraph import KGObject


class SWHID(KGObject, OMSWHID):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SWHID"
    default_space = "software"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            [
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
            ],
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
