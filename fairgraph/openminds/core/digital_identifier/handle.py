"""
A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class HANDLE(KGObject):
    """
    A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/HANDLE"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the HANDLE."),
        Field(
            "related_to",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:relatedPublication",
            reverse="related_publications",
            multiple=True,
            doc="reverse of 'relatedPublication'",
        ),
    ]
    existence_query_fields = ("identifier",)

    def __init__(self, identifier=None, related_to=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, identifier=identifier, related_to=related_to
        )
