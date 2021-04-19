"""
Structured information on a coordinate point.
"""

# this file was auto-generated


from fairgraph.base import KGObject
from fairgraph.fields import Field


class CoordinatePoint(KGObject):
    """
    Structured information on a coordinate point.
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/sands/CoordinatePoint"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("coordinatess", "openminds.core.QuantitativeValue", "vocab:coordinates", multiple=True, required=True,
              doc="Pair or triplet of numbers defining a location in a given coordinate space."),
        Field("coordinate_space", "openminds.sands.CoordinateSpace", "vocab:coordinateSpace", multiple=False, required=True,
              doc="Two or three dimensional geometric setting."),
        
    ]
    existence_query_fields = ('name',)