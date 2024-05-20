"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class CustomCoordinateSpace(KGObject):
    """
    <description not available>
    """

    default_space = "spatial"
    type_ = "https://openminds.ebrains.eu/sands/CustomCoordinateSpace"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "anatomical_axes_orientation",
            "openminds.controlled_terms.AnatomicalAxesOrientation",
            "vocab:anatomicalAxesOrientation",
            required=True,
            doc="Relation between reference planes used in anatomy and mathematics.",
        ),
        Property(
            "axes_origins",
            "openminds.core.QuantitativeValue",
            "vocab:axesOrigin",
            multiple=True,
            required=True,
            doc="Special point in a coordinate system used as a fixed point of reference for the geometry of the surrounding space.",
        ),
        Property(
            "default_images",
            "openminds.core.File",
            "vocab:defaultImage",
            multiple=True,
            doc="Two or three dimensional image that particluarly represents a specific coordinate space.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the custom coordinate space.",
        ),
        Property(
            "native_unit",
            "openminds.controlled_terms.UnitOfMeasurement",
            "vocab:nativeUnit",
            required=True,
            doc="Determinate quantity used in the original measurement.",
        ),
        Property(
            "is_coordinate_space_of",
            "openminds.sands.CustomAnnotation",
            "^vocab:coordinateSpace",
            reverse="coordinate_spaces",
            multiple=True,
            doc="reverse of 'coordinateSpace'",
        ),
        Property(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        anatomical_axes_orientation=None,
        axes_origins=None,
        default_images=None,
        is_coordinate_space_of=None,
        is_used_to_group=None,
        native_unit=None,
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
            name=name,
            anatomical_axes_orientation=anatomical_axes_orientation,
            axes_origins=axes_origins,
            default_images=default_images,
            is_coordinate_space_of=is_coordinate_space_of,
            is_used_to_group=is_used_to_group,
            native_unit=native_unit,
        )
