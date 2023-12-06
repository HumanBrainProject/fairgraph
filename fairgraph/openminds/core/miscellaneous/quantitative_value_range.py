"""
A representation of a range of quantitative values.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class QuantitativeValueRange(EmbeddedMetadata):
    """
    A representation of a range of quantitative values.
    """

    type_ = ["https://openminds.ebrains.eu/core/QuantitativeValueRange"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("max_value", float, "vocab:maxValue", required=True, doc="Greatest quantity attained or allowed."),
        Field(
            "max_value_unit",
            "openminds.controlledterms.UnitOfMeasurement",
            "vocab:maxValueUnit",
            doc="no description available",
        ),
        Field("min_value", float, "vocab:minValue", required=True, doc="Smallest quantity attained or allowed."),
        Field(
            "min_value_unit",
            "openminds.controlledterms.UnitOfMeasurement",
            "vocab:minValueUnit",
            doc="no description available",
        ),
    ]

    def __init__(
        self,
        max_value=None,
        max_value_unit=None,
        min_value=None,
        min_value_unit=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            max_value=max_value,
            max_value_unit=max_value_unit,
            min_value=min_value,
            min_value_unit=min_value_unit,
        )
