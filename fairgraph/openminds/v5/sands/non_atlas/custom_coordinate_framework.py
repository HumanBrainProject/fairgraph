"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import CustomCoordinateFramework as OMCustomCoordinateFramework
from fairgraph import KGObject


class CustomCoordinateFramework(KGObject, OMCustomCoordinateFramework):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CustomCoordinateFramework"
    default_space = "spatial"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_coordinate_framework_of",
            [
                "openminds.v5.core.GridImage",
                "openminds.v5.core.GridImageSequence",
                "openminds.v5.core.GridImageStack",
                "openminds.v5.core.GridVolume",
                "openminds.v5.core.GridVolumeSequence",
                "openminds.v5.sands.CustomAnnotation",
            ],
            "coordinateFramework",
            reverse="coordinate_framework",
            multiple=True,
            description="reverse of 'coordinate_framework'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v5.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        anatomical_axes_orientation=None,
        axes_origins=None,
        default_images=None,
        is_coordinate_framework_of=None,
        is_used_to_group=None,
        native_unit=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            name=name,
            anatomical_axes_orientation=anatomical_axes_orientation,
            axes_origins=axes_origins,
            default_images=default_images,
            is_coordinate_framework_of=is_coordinate_framework_of,
            is_used_to_group=is_used_to_group,
            native_unit=native_unit,
        )
