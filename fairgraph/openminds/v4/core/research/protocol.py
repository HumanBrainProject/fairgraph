"""
Structured information on a research project.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Protocol as OMProtocol
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
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.ProtocolExecution",
                "openminds.v4.ephys.CellPatching",
                "openminds.v4.ephys.ElectrodePlacement",
                "openminds.v4.ephys.RecordingActivity",
                "openminds.v4.specimen_prep.CranialWindowPreparation",
                "openminds.v4.specimen_prep.TissueCulturePreparation",
                "openminds.v4.specimen_prep.TissueSampleSlicing",
                "openminds.v4.stimulation.StimulationActivity",
            ],
            "protocol",
            reverse="protocols",
            multiple=True,
            description="reverse of 'protocols'",
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
