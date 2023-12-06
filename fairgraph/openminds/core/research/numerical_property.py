"""
Structured information about a property of some entity or process whose value is a number.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class NumericalProperty(EmbeddedMetadata):
    """
    Structured information about a property of some entity or process whose value is a number.
    """

    type_ = ["https://openminds.ebrains.eu/core/NumericalProperty"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the numerical property.",
        ),
        Field(
            "values",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:value",
            multiple=True,
            required=True,
            doc="Entry for a property.",
        ),
    ]

    def __init__(self, name=None, values=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, name=name, values=values)
