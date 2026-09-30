"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import AnatomicalTargetPosition as OMAnatomicalTargetPosition
from fairgraph import KGEmbedded


class AnatomicalTargetPosition(KGEmbedded, OMAnatomicalTargetPosition):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/AnatomicalTargetPosition"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("anatomical_targets", "target_identification_type")

    def __init__(
        self,
        additional_remarks=None,
        anatomical_targets=None,
        spatial_locations=None,
        target_identification_type=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            additional_remarks=additional_remarks,
            anatomical_targets=anatomical_targets,
            spatial_locations=spatial_locations,
            target_identification_type=target_identification_type,
        )
