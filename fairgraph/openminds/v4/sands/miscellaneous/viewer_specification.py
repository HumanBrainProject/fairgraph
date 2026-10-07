"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import ViewerSpecification as OMViewerSpecification
from fairgraph import KGEmbedded


class ViewerSpecification(KGEmbedded, OMViewerSpecification):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ViewerSpecification"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("anchor_points",)

    def __init__(
        self,
        additional_remarks=None,
        anchor_points=None,
        camera_position=None,
        preferred_display_color=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            additional_remarks=additional_remarks,
            anchor_points=anchor_points,
            camera_position=camera_position,
            preferred_display_color=preferred_display_color,
        )
