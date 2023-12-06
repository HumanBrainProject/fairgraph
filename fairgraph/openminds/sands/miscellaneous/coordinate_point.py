"""
Structured information on a coordinate point.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class CoordinatePoint(EmbeddedMetadata):
    """
    Structured information on a coordinate point.
    """

    type_ = ["https://openminds.ebrains.eu/sands/CoordinatePoint"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "coordinate_space",
            ["openminds.sands.CommonCoordinateSpaceVersion", "openminds.sands.CustomCoordinateSpace"],
            "vocab:coordinateSpace",
            required=True,
            doc="Two or three dimensional geometric setting.",
        ),
        Field(
            "coordinates",
            "openminds.core.QuantitativeValue",
            "vocab:coordinates",
            multiple=True,
            required=True,
            doc="Pair or triplet of numbers defining a location in a given coordinate space.",
        ),
    ]

    def __init__(self, coordinate_space=None, coordinates=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, coordinate_space=coordinate_space, coordinates=coordinates)
