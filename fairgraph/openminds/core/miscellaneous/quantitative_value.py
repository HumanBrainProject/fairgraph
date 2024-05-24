"""
Structured information on a quantitative value.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class QuantitativeValue(EmbeddedMetadata):
    """
    Structured information on a quantitative value.
    """

    type_ = "https://openminds.ebrains.eu/core/QuantitativeValue"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "type_of_uncertainty",
            "openminds.controlled_terms.TypeOfUncertainty",
            "vocab:typeOfUncertainty",
            doc="Distinct technique used to quantify the uncertainty of a measurement.",
        ),
        Property(
            "uncertainties",
            float,
            "vocab:uncertainty",
            multiple=True,
            doc="Quantitative value range defining the uncertainty of a measurement.",
        ),
        Property(
            "unit",
            "openminds.controlled_terms.UnitOfMeasurement",
            "vocab:unit",
            doc="Determinate quantity adopted as a standard of measurement.",
        ),
        Property("value", float, "vocab:value", required=True, doc="Entry for a property."),
    ]
    reverse_properties = []

    def __init__(
        self,
        type_of_uncertainty=None,
        uncertainties=None,
        unit=None,
        value=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data, type_of_uncertainty=type_of_uncertainty, uncertainties=uncertainties, unit=unit, value=value
        )
