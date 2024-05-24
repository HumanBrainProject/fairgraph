"""
Structured information about properties of an entity that are not represented in an openMINDS schema.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class CustomPropertySet(EmbeddedMetadata):
    """
    Structured information about properties of an entity that are not represented in an openMINDS schema.
    """

    type_ = "https://openminds.ebrains.eu/core/CustomPropertySet"
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
            "data_location",
            ["openminds.core.Configuration", "openminds.core.File", "openminds.core.PropertyValueList"],
            "vocab:dataLocation",
            required=True,
            doc="no description available",
        ),
        Property(
            "relevant_for",
            [
                "openminds.controlled_terms.AnalysisTechnique",
                "openminds.controlled_terms.MRIPulseSequence",
                "openminds.controlled_terms.StimulationApproach",
                "openminds.controlled_terms.StimulationTechnique",
                "openminds.controlled_terms.Technique",
            ],
            "vocab:relevantFor",
            required=True,
            doc="Reference to what or whom the custom property set bears significance.",
        ),
    ]
    reverse_properties = []

    def __init__(
        self, context=None, data_location=None, relevant_for=None, id=None, data=None, space=None, scope=None
    ):
        return super().__init__(data=data, context=context, data_location=data_location, relevant_for=relevant_for)
