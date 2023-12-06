"""
Structured information about properties of an entity that are not represented in an openMINDS schema.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class CustomPropertySet(EmbeddedMetadata):
    """
    Structured information about properties of an entity that are not represented in an openMINDS schema.
    """

    type_ = ["https://openminds.ebrains.eu/core/CustomPropertySet"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("context", str, "vocab:context", required=True, doc="no description available"),
        Field(
            "data_location",
            ["openminds.core.Configuration", "openminds.core.File", "openminds.core.PropertyValueList"],
            "vocab:dataLocation",
            required=True,
            doc="no description available",
        ),
        Field(
            "relevant_for",
            [
                "openminds.controlledterms.AnalysisTechnique",
                "openminds.controlledterms.StimulationApproach",
                "openminds.controlledterms.StimulationTechnique",
                "openminds.controlledterms.Technique",
            ],
            "vocab:relevantFor",
            required=True,
            doc="Reference to what or whom the custom property set bears significance.",
        ),
    ]

    def __init__(
        self, context=None, data_location=None, relevant_for=None, id=None, data=None, space=None, scope=None
    ):
        return super().__init__(data=data, context=context, data_location=data_location, relevant_for=relevant_for)
