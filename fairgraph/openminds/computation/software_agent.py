"""
Structured information about a piece of software or web service that can perform a task autonomously.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class SoftwareAgent(KGObject):
    """
    Structured information about a piece of software or web service that can perform a task autonomously.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/SoftwareAgent"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "environment", "openminds.computation.Environment", "vocab:environment", doc="no description available"
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the software agent.",
        ),
        Property(
            "software",
            "openminds.core.SoftwareVersion",
            "vocab:software",
            required=True,
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
            "activities",
            [
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimen_prep.CranialWindowPreparation",
                "openminds.specimen_prep.TissueCulturePreparation",
                "openminds.specimen_prep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:performedBy",
            reverse="performed_by",
            multiple=True,
            doc="reverse of 'performedBy'",
        ),
        Property(
            "started",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
                "openminds.computation.WorkflowExecution",
            ],
            "^vocab:startedBy",
            reverse="started_by",
            multiple=True,
            doc="reverse of 'startedBy'",
        ),
    ]
    existence_query_properties = ("name", "software")

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
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            activities=activities,
            environment=environment,
            software=software,
            started=started,
        )
