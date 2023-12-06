"""
A persistent identifier for a research organization, provided by the Research Organization Registry.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class RORID(KGObject):
    """
    A persistent identifier for a research organization, provided by the Research Organization Registry.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/RORID"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the RORID."),
        Field(
            "identifies",
            "openminds.core.Organization",
            "^vocab:digitalIdentifier",
            reverse="digital_identifiers",
            multiple=True,
            doc="reverse of 'digitalIdentifier'",
        ),
    ]
    existence_query_fields = ("identifier",)

    def __init__(self, identifier=None, identifies=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, identifier=identifier, identifies=identifies
        )
