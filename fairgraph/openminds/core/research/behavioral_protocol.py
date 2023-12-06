"""
Structured information about a protocol used in an experiment studying human or animal behavior.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class BehavioralProtocol(KGObject):
    """
    Structured information about a protocol used in an experiment studying human or animal behavior.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/BehavioralProtocol"]
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
            doc="Word or phrase that constitutes the distinctive designation of the behavioral protocol.",
        ),
        Field(
            "described_in",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.WebResource"],
            "vocab:describedIn",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the behavioral protocol.",
        ),
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the behavioral protocol within a particular product.",
        ),
        Field(
            "stimulations",
            ["openminds.controlledterms.StimulationApproach", "openminds.controlledterms.StimulationTechnique"],
            "vocab:stimulation",
            multiple=True,
            doc="no description available",
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
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Field(
            "used_in",
            ["openminds.core.DatasetVersion", "openminds.core.ProtocolExecution"],
            "^vocab:behavioralProtocol",
            reverse="behavioral_protocols",
            multiple=True,
            doc="reverse of 'behavioralProtocol'",
        ),
    ]
    existence_query_fields = ("description", "name")

    def __init__(
        self,
        name=None,
        described_in=None,
        description=None,
        internal_identifier=None,
        stimulations=None,
        stimulus_types=None,
        is_used_to_group=None,
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
            internal_identifier=internal_identifier,
            stimulations=stimulations,
            stimulus_types=stimulus_types,
            is_used_to_group=is_used_to_group,
            used_in=used_in,
        )
