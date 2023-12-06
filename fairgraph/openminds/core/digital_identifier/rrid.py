"""
A persistent identifier for a research resource provided by the Resource Identification Initiative.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class RRID(KGObject):
    """
    A persistent identifier for a research resource provided by the Resource Identification Initiative.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/RRID"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the RRID."),
        Field(
            "identifies",
            [
                "openminds.chemicals.ProductSource",
                "openminds.core.Organization",
                "openminds.core.Software",
                "openminds.core.SoftwareVersion",
                "openminds.core.Strain",
                "openminds.ephys.Electrode",
                "openminds.ephys.ElectrodeArray",
                "openminds.ephys.Pipette",
                "openminds.sands.BrainAtlas",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpace",
                "openminds.sands.CommonCoordinateSpaceVersion",
                "openminds.specimenprep.SlicingDevice",
            ],
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
