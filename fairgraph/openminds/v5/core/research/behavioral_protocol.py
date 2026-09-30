"""
Structured information about a protocol used in an experiment studying human or animal behavior.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import BehavioralProtocol as OMBehavioralProtocol
from fairgraph import KGObject


class BehavioralProtocol(KGObject, OMBehavioralProtocol):
    """
    Structured information about a protocol used in an experiment studying human or animal behavior.
    """

    type_ = "https://openminds.om-i.org/types/BehavioralProtocol"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_used_to_group",
            "openminds.v5.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "used_in",
            [
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.core.SubjectGroupState",
                "openminds.v5.core.SubjectState",
                "openminds.v5.core.TissueSampleCollectionState",
                "openminds.v5.core.TissueSampleState",
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
            ],
            ["associatedProtocol", "behavioralProtocol", "protocol"],
            reverse=["associated_protocols", "behavioral_protocols", "protocols"],
            multiple=True,
            description="reverse of associated_protocols, behavioral_protocols, protocols",
        ),
    ]
    existence_query_properties = ("description", "name")

    def __init__(
        self,
        name=None,
        described_in=None,
        description=None,
        internal_identifier=None,
        is_used_to_group=None,
        stimulations=None,
        stimulus_types=None,
        used_in=None,
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
            described_in=described_in,
            description=description,
            internal_identifier=internal_identifier,
            is_used_to_group=is_used_to_group,
            stimulations=stimulations,
            stimulus_types=stimulus_types,
            used_in=used_in,
        )
