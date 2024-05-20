"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class ViewerSpecification(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = "https://openminds.ebrains.eu/sands/ViewerSpecification"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Property(
            "anchor_points",
            "openminds.core.QuantitativeValue",
            "vocab:anchorPoint",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Property(
            "camera_position",
            "openminds.sands.CoordinatePoint",
            "vocab:cameraPosition",
            doc="no description available",
        ),
        Property(
            "preferred_display_color",
            ["openminds.controlled_terms.Colormap", "openminds.sands.SingleColor"],
            "vocab:preferredDisplayColor",
            doc="no description available",
        ),
    ]

    def __init__(
        self,
        additional_remarks=None,
        anchor_points=None,
        camera_position=None,
        preferred_display_color=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            additional_remarks=additional_remarks,
            anchor_points=anchor_points,
            camera_position=camera_position,
            preferred_display_color=preferred_display_color,
        )
