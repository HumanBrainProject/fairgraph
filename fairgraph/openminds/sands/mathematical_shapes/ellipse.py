"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class Ellipse(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = "https://openminds.ebrains.eu/sands/Ellipse"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "semi_major_axis",
            "openminds.core.QuantitativeValue",
            "vocab:semiMajorAxis",
            required=True,
            doc="no description available",
        ),
        Property(
            "semi_minor_axis",
            "openminds.core.QuantitativeValue",
            "vocab:semiMinorAxis",
            required=True,
            doc="no description available",
        ),
    ]

    def __init__(self, semi_major_axis=None, semi_minor_axis=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, semi_major_axis=semi_major_axis, semi_minor_axis=semi_minor_axis)
