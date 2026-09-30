"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import TissueSampleCollectionState as OMTissueSampleCollectionState
from fairgraph import KGObject


class TissueSampleCollectionState(KGObject, OMTissueSampleCollectionState):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/TissueSampleCollectionState"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_children",
            ["openminds.v5.core.TissueSampleCollectionState", "openminds.v5.core.TissueSampleState"],
            "descendedFrom",
            reverse="descended_from",
            multiple=True,
            description="reverse of 'descended_from'",
        ),
        Property(
            "has_study_results_in",
            "openminds.v5.core.DatasetVersion",
            "studiedSpecimen",
            reverse="studied_specimens",
            multiple=True,
            description="reverse of 'studied_specimens'",
        ),
        Property(
            "is_input_to",
            ["openminds.v5.ephys.RecordingActivity", "openminds.v5.specimen_prep.TissueCulturePreparation"],
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.specimen_prep.TissueSampleSlicing",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            "output",
            reverse="outputs",
            multiple=True,
            description="reverse of 'outputs'",
        ),
        Property(
            "is_state_of",
            "openminds.v5.core.TissueSampleCollection",
            "studiedState",
            reverse="studied_states",
            multiple=True,
            description="reverse of 'studied_states'",
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
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        additional_remarks=None,
        age=None,
        associated_protocols=None,
        attributes=None,
        descended_from=None,
        has_children=None,
        has_study_results_in=None,
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
            associated_protocols=associated_protocols,
            attributes=attributes,
            descended_from=descended_from,
            has_children=has_children,
            has_study_results_in=has_study_results_in,
            internal_identifier=internal_identifier,
            is_input_to=is_input_to,
            is_output_of=is_output_of,
            is_state_of=is_state_of,
            is_used_to_group=is_used_to_group,
            pathologies=pathologies,
            relative_time_indication=relative_time_indication,
            weight=weight,
        )
