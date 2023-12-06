"""
Structured information on a research project.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class Project(KGObject):
    """
    Structured information on a research project.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/Project"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the project."),
        Field(
            "alias", str, "vocab:shortName", required=True, doc="Shortened or fully abbreviated name of the project."
        ),
        Field(
            "coordinators",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:coordinator",
            multiple=True,
            doc="Legal person who organizes the collaborative work of people or groups.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the project.",
        ),
        Field(
            "has_parts",
            [
                "openminds.computation.ValidationTest",
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipe",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.Dataset",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModel",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.Model",
                "openminds.core.ModelVersion",
                "openminds.core.Software",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebService",
                "openminds.core.WebServiceVersion",
                "openminds.publications.LivePaper",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlas",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpace",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "vocab:hasPart",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the project."),
    ]
    existence_query_fields = ("alias",)

    def __init__(
        self,
        name=None,
        alias=None,
        coordinators=None,
        description=None,
        has_parts=None,
        homepage=None,
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
            name=name,
            alias=alias,
            coordinators=coordinators,
            description=description,
            has_parts=has_parts,
            homepage=homepage,
        )
