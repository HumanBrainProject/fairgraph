"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.ephys import CellPatching as OMCellPatching
from fairgraph import KGObject


from datetime import datetime, time


class CellPatching(KGObject, OMCellPatching):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CellPatching"
    default_space = "in-depth"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        bath_temperature=None,
        custom_property_sets=None,
        description=None,
        devices=None,
        end_time=None,
        inputs=None,
        is_part_of=None,
        outputs=None,
        performed_by=None,
        preparation_design=None,
        protocols=None,
        start_time=None,
        study_targets=None,
        target_position=None,
        tissue_bath_solution=None,
        variation=None,
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
            bath_temperature=bath_temperature,
            custom_property_sets=custom_property_sets,
            description=description,
            devices=devices,
            end_time=end_time,
            inputs=inputs,
            is_part_of=is_part_of,
            outputs=outputs,
            performed_by=performed_by,
            preparation_design=preparation_design,
            protocols=protocols,
            start_time=start_time,
            study_targets=study_targets,
            target_position=target_position,
            tissue_bath_solution=tissue_bath_solution,
            variation=variation,
        )
