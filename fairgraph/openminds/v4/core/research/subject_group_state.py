"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import SubjectGroupState as OMSubjectGroupState
from fairgraph import KGObject


class SubjectGroupState(KGObject, OMSubjectGroupState):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SubjectGroupState"
    default_space = "dataset"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_children",
            [
                "openminds.v4.core.SubjectGroupState",
                "openminds.v4.core.TissueSampleCollectionState",
                "openminds.v4.core.TissueSampleState",
            ],
            "descendedFrom",
            reverse="descended_from",
            multiple=True,
            description="reverse of 'descended_from'",
        ),
        Property(
            "is_input_to",
            ["openminds.v4.ephys.RecordingActivity", "openminds.v4.specimen_prep.TissueCulturePreparation"],
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
        ),
        Property(
            "is_output_of",
            ["openminds.v4.core.ProtocolExecution", "openminds.v4.stimulation.StimulationActivity"],
            "output",
            reverse="outputs",
            multiple=True,
            description="reverse of 'outputs'",
        ),
        Property(
            "is_state_of",
            "openminds.v4.core.SubjectGroup",
            "studiedState",
            reverse="studied_states",
            multiple=True,
            description="reverse of 'studied_states'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v4.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
    ]
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        additional_remarks=None,
        age=None,
        age_categories=None,
        attributes=None,
        descended_from=None,
        handedness=None,
        has_children=None,
        internal_identifier=None,
        is_input_to=None,
        is_output_of=None,
        is_state_of=None,
        is_used_to_group=None,
        pathologies=None,
        relative_time_indication=None,
        weight=None,
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
            additional_remarks=additional_remarks,
            age=age,
            age_categories=age_categories,
            attributes=attributes,
            descended_from=descended_from,
            handedness=handedness,
            has_children=has_children,
            internal_identifier=internal_identifier,
            is_input_to=is_input_to,
            is_output_of=is_output_of,
            is_state_of=is_state_of,
            is_used_to_group=is_used_to_group,
            pathologies=pathologies,
            relative_time_indication=relative_time_indication,
            weight=weight,
        )
