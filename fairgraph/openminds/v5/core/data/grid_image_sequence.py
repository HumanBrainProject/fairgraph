"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import GridImageSequence as OMGridImageSequence
from fairgraph import KGObject


class GridImageSequence(KGObject, OMGridImageSequence):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/GridImageSequence"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("data_location", "dimensions", "pixel_sizes", "temporal_sampling_frequency")

    def __init__(
        self,
        name=None,
        additional_remarks=None,
        coordinate_framework=None,
        data_location=None,
        dimensions=None,
        number_of_images=None,
        obtained_with=None,
        pixel_sizes=None,
        temporal_sampling_frequency=None,
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
            number_of_images=number_of_images,
            obtained_with=obtained_with,
            pixel_sizes=pixel_sizes,
            temporal_sampling_frequency=temporal_sampling_frequency,
        )
