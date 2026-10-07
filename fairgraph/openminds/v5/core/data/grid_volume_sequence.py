"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import GridVolumeSequence as OMGridVolumeSequence
from fairgraph import KGObject


class GridVolumeSequence(KGObject, OMGridVolumeSequence):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/GridVolumeSequence"
    default_space = "in-depth"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("data_location", "dimensions", "temporal_sampling_frequency", "voxel_sizes")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        additional_remarks=None,
        coordinate_framework=None,
        data_location=None,
        dimensions=None,
        number_of_planes=None,
        number_of_volumes=None,
        obtained_with=None,
        temporal_sampling_frequency=None,
        voxel_sizes=None,
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
            additional_remarks=additional_remarks,
            coordinate_framework=coordinate_framework,
            data_location=data_location,
            dimensions=dimensions,
            number_of_planes=number_of_planes,
            number_of_volumes=number_of_volumes,
            obtained_with=obtained_with,
            temporal_sampling_frequency=temporal_sampling_frequency,
            voxel_sizes=voxel_sizes,
        )
