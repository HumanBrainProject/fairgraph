"""
An International Standard Serial Number of the ISSN International Centre.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ISSN(KGObject):
    """
    An International Standard Serial Number of the ISSN International Centre.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/ISSN"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the ISSN."),
    ]
    reverse_properties = [
        Property(
            "identifies",
            "openminds.publications.Periodical",
            "^vocab:digitalIdentifier",
            reverse="digital_identifiers",
            multiple=True,
            doc="reverse of 'digitalIdentifier'",
        ),
        Property(
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
    existence_query_properties = ("identifier",)

    def __init__(self, identifier=None, identifies=None, related_to=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            identifier=identifier,
            identifies=identifies,
            related_to=related_to,
        )
