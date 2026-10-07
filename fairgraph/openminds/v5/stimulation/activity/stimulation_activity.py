"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.stimulation import StimulationActivity as OMStimulationActivity
from fairgraph import KGObject


from datetime import datetime, time


class StimulationActivity(KGObject, OMStimulationActivity):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/StimulationActivity"
    default_space = "in-depth"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        custom_property_sets=None,
        description=None,
        end_time=None,
        inputs=None,
        is_part_of=None,
        outputs=None,
        performed_by=None,
        preparation_design=None,
        protocols=None,
        setup=None,
        start_time=None,
        stimuli=None,
        study_targets=None,
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
            custom_property_sets=custom_property_sets,
            description=description,
            end_time=end_time,
            inputs=inputs,
            is_part_of=is_part_of,
            outputs=outputs,
            performed_by=performed_by,
            preparation_design=preparation_design,
            protocols=protocols,
            setup=setup,
            start_time=start_time,
            stimuli=stimuli,
            study_targets=study_targets,
        )
