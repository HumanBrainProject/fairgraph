"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ResearchProductGroup(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/ResearchProductGroup"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("context", str, "vocab:context", required=True, doc="no description available"),
        Property(
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
    ]
    reverse_properties = []
    existence_query_properties = ("context", "has_parts")

    def __init__(self, context=None, has_parts=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, space=space, scope=scope, data=data, context=context, has_parts=has_parts)
