"""
A representation of an array of quantitative values, optionally with uncertainties.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class QuantitativeValueArray(KGObject):
    """
    A representation of an array of quantitative values, optionally with uncertainties.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/QuantitativeValueArray"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "negative_uncertainties",
            float,
            "vocab:negativeUncertainties",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "positive_uncertainties",
            float,
            "vocab:positiveUncertainties",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "type_of_uncertainty",
            "openminds.controlledterms.TypeOfUncertainty",
            "vocab:typeOfUncertainty",
            doc="Distinct technique used to quantify the uncertainty of a measurement.",
        ),
        Field(
            "unit",
            "openminds.controlledterms.UnitOfMeasurement",
            "vocab:unit",
            doc="Determinate quantity adopted as a standard of measurement.",
        ),
        Field("values", float, "vocab:values", multiple=True, required=True, doc="no description available"),
    ]
    existence_query_fields = ("values",)

    def __init__(
        self,
        negative_uncertainties=None,
        positive_uncertainties=None,
        type_of_uncertainty=None,
        unit=None,
        values=None,
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
            negative_uncertainties=negative_uncertainties,
            positive_uncertainties=positive_uncertainties,
            type_of_uncertainty=type_of_uncertainty,
            unit=unit,
            values=values,
        )
