"""
Structured information about a digital object identifier, as standardized by the International Organization for Standardization.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class DOI(KGObject):
    """
    Structured information about a digital object identifier, as standardized by the International Organization for Standardization.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/DOI"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("identifier", str, "vocab:identifier", required=True, doc="Term or code used to identify the DOI."),
        Field(
            "describes",
            ["openminds.core.BehavioralProtocol", "openminds.core.Protocol"],
            "^vocab:describedIn",
            reverse="described_in",
            multiple=True,
            doc="reverse of 'describedIn'",
        ),
        Field(
            "identifies",
            [
                "openminds.computation.ValidationTest",
                "openminds.computation.WorkflowRecipe",
                "openminds.core.Dataset",
                "openminds.core.MetaDataModel",
                "openminds.core.Model",
                "openminds.core.Software",
                "openminds.ephys.Electrode",
                "openminds.ephys.ElectrodeArray",
                "openminds.ephys.Pipette",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.LivePaper",
                "openminds.publications.ScholarlyArticle",
                "openminds.sands.BrainAtlas",
                "openminds.sands.CommonCoordinateSpace",
                "openminds.specimenprep.SlicingDevice",
            ],
            "^vocab:digitalIdentifier",
            reverse="digital_identifiers",
            multiple=True,
            doc="reverse of 'digitalIdentifier'",
        ),
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

    def __init__(
        self,
        identifier=None,
        describes=None,
        identifies=None,
        related_to=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            identifier=identifier,
            describes=describes,
            identifies=identifies,
            related_to=related_to,
        )
