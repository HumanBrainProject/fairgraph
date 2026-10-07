"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import GridImage as OMGridImage
from fairgraph import KGObject


class GridImage(KGObject, OMGridImage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/GridImage"
    default_space = "in-depth"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("data_location", "dimensions", "pixel_sizes")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        additional_remarks=None,
        coordinate_framework=None,
        data_location=None,
        dimensions=None,
        obtained_with=None,
        pixel_sizes=None,
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
            obtained_with=obtained_with,
            pixel_sizes=pixel_sizes,
        )
