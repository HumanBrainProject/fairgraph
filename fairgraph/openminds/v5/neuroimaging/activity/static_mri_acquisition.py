"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.neuroimaging import StaticMRIAcquisition as OMStaticMRIAcquisition
from fairgraph import KGObject


from datetime import datetime, time


class StaticMRIAcquisition(KGObject, OMStaticMRIAcquisition):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/StaticMRIAcquisition"
    default_space = "in-depth"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        contrast_agents=None,
        custom_property_sets=None,
        description=None,
        device=None,
        distortion_corrections=None,
        end_time=None,
        inputs=None,
        is_part_of=None,
        motion_corrections=None,
        outputs=None,
        performed_by=None,
        preparation_design=None,
        protocols=None,
        registration_data=None,
        specimen_orientation=None,
        start_time=None,
        study_targets=None,
        target_anatomy=None,
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
            lookup_label=lookup_label,
            contrast_agents=contrast_agents,
            custom_property_sets=custom_property_sets,
            description=description,
            device=device,
            distortion_corrections=distortion_corrections,
            end_time=end_time,
            inputs=inputs,
            is_part_of=is_part_of,
            motion_corrections=motion_corrections,
            outputs=outputs,
            performed_by=performed_by,
            preparation_design=preparation_design,
            protocols=protocols,
            registration_data=registration_data,
            specimen_orientation=specimen_orientation,
            start_time=start_time,
            study_targets=study_targets,
            target_anatomy=target_anatomy,
        )
