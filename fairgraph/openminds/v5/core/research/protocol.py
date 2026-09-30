"""
Structured information on a research project.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Protocol as OMProtocol
from fairgraph import KGObject


class Protocol(KGObject, OMProtocol):
    """
    Structured information on a research project.
    """

    type_ = "https://openminds.om-i.org/types/Protocol"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "used_in",
            [
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.core.SubjectGroupState",
                "openminds.v5.core.SubjectState",
                "openminds.v5.core.TissueSampleCollectionState",
                "openminds.v5.core.TissueSampleState",
                "openminds.v5.ephys.CellPatching",
                "openminds.v5.ephys.ElectrodePlacement",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
                "openminds.v5.neuroimaging.StaticMRIAcquisition",
                "openminds.v5.specimen_prep.CranialWindowPreparation",
                "openminds.v5.specimen_prep.TissueCulturePreparation",
                "openminds.v5.specimen_prep.TissueSampleSlicing",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            ["associatedProtocol", "protocol"],
            reverse=["associated_protocols", "protocols"],
            multiple=True,
            description="reverse of associated_protocols, protocols",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        described_in=None,
        description=None,
        stimulus_types=None,
        techniques=None,
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
            stimulus_types=stimulus_types,
            techniques=techniques,
            used_in=used_in,
        )
