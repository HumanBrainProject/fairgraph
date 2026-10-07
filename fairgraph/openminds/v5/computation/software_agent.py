"""
Structured information about a piece of software or web service that can perform a task autonomously.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import SoftwareAgent as OMSoftwareAgent
from fairgraph import KGObject


class SoftwareAgent(KGObject, OMSoftwareAgent):
    """
    Structured information about a piece of software or web service that can perform a task autonomously.
    """

    type_ = "https://openminds.om-i.org/types/SoftwareAgent"
    default_space = "computation"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "activities",
            [
                "openminds.v5.core.ProtocolExecution",
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
            "performedBy",
            reverse="performed_by",
            multiple=True,
            description="reverse of 'performed_by'",
        ),
        Property(
            "started",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
                "openminds.v5.computation.WorkflowExecution",
            ],
            "startedBy",
            reverse="started_by",
            multiple=True,
            description="reverse of 'started_by'",
        ),
    ]
    existence_query_properties = ("name", "software")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        activities=None,
        environment=None,
        software=None,
        started=None,
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
            activities=activities,
            environment=environment,
            software=software,
            started=started,
        )
