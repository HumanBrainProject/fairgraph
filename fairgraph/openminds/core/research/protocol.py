"""
Structured information on a research project.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class Protocol(KGObject):
    """
    Structured information on a research project.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/Protocol"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "described_in",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.WebResource"],
            "vocab:describedIn",
            doc="no description available",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the protocol.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the protocol.",
        ),
        Property(
            "stimulus_types",
            [
                "openminds.controlled_terms.AuditoryStimulusType",
                "openminds.controlled_terms.ElectricalStimulusType",
                "openminds.controlled_terms.GustatoryStimulusType",
                "openminds.controlled_terms.OlfactoryStimulusType",
                "openminds.controlled_terms.OpticalStimulusType",
                "openminds.controlled_terms.TactileStimulusType",
                "openminds.controlled_terms.VisualStimulusType",
            ],
            "vocab:stimulusType",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "techniques",
            [
                "openminds.controlled_terms.AnalysisTechnique",
                "openminds.controlled_terms.MRIPulseSequence",
                "openminds.controlled_terms.StimulationApproach",
                "openminds.controlled_terms.StimulationTechnique",
                "openminds.controlled_terms.Technique",
            ],
            "vocab:technique",
            multiple=True,
            required=True,
            doc="Method of accomplishing a desired aim.",
        ),
        Property(
            "used_in",
            [
                "openminds.core.DatasetVersion",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimen_prep.CranialWindowPreparation",
                "openminds.specimen_prep.TissueCulturePreparation",
                "openminds.specimen_prep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:protocol",
            reverse="protocols",
            multiple=True,
            doc="reverse of 'protocol'",
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
