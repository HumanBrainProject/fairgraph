"""
Structured information on a research project.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Protocol(KGObject):
    """
    Structured information on a research project.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/Protocol"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the protocol.",
        ),
        Field(
            "described_in",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.WebResource"],
            "vocab:describedIn",
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the protocol.",
        ),
        Field(
            "stimulus_types",
            [
                "openminds.controlledterms.AuditoryStimulusType",
                "openminds.controlledterms.ElectricalStimulusType",
                "openminds.controlledterms.GustatoryStimulusType",
                "openminds.controlledterms.OlfactoryStimulusType",
                "openminds.controlledterms.OpticalStimulusType",
                "openminds.controlledterms.TactileStimulusType",
                "openminds.controlledterms.VisualStimulusType",
            ],
            "vocab:stimulusType",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "techniques",
            [
                "openminds.controlledterms.AnalysisTechnique",
                "openminds.controlledterms.StimulationApproach",
                "openminds.controlledterms.StimulationTechnique",
                "openminds.controlledterms.Technique",
            ],
            "vocab:technique",
            multiple=True,
            required=True,
            doc="Method of accomplishing a desired aim.",
        ),
        Field(
            "used_in",
            [
                "openminds.core.DatasetVersion",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimenprep.CranialWindowPreparation",
                "openminds.specimenprep.TissueCulturePreparation",
                "openminds.specimenprep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:protocol",
            reverse="protocols",
            multiple=True,
            doc="reverse of 'protocol'",
        ),
    ]
    existence_query_fields = ("name",)

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
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            described_in=described_in,
            description=description,
            stimulus_types=stimulus_types,
            techniques=techniques,
            used_in=used_in,
        )
