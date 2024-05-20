"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class IdentifiersDotOrgID(KGObject):
    """
    <description not available>
    """

    default_space = "common"
    type_ = "https://openminds.ebrains.eu/core/IdentifiersDotOrgID"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "identifier",
            str,
            "vocab:identifier",
            required=True,
            doc="Term or code used to identify the identifiers dot org i d.",
        ),
        Property(
            "identifies",
            ["openminds.core.Dataset", "openminds.core.DatasetVersion"],
            "^vocab:digitalIdentifier",
            reverse="digital_identifiers",
            multiple=True,
            doc="reverse of 'digitalIdentifier'",
        ),
    ]
    existence_query_properties = ("identifier",)

    def __init__(self, identifier=None, identifies=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, identifier=identifier, identifies=identifies
        )
