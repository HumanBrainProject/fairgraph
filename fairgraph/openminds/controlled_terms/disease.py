"""
Structured information on a disease.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class Disease(KGObject):
    """
    Structured information on a disease.
    """

    default_space = "controlled"
    type_ = "https://openminds.ebrains.eu/controlledTerms/Disease"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the disease.",
        ),
        Property(
            "interlex_identifier",
            IRI,
            "vocab:interlexIdentifier",
            doc="Persistent identifier for a term registered in the InterLex project.",
        ),
        Property(
            "knowledge_space_link",
            IRI,
            "vocab:knowledgeSpaceLink",
            doc="Persistent link to an encyclopedia entry in the Knowledge Space project.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the disease.",
        ),
        Property(
            "preferred_ontology_identifier",
            IRI,
            "vocab:preferredOntologyIdentifier",
            doc="Persistent identifier of a preferred ontological term.",
        ),
        Property(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
    ]
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.LivePaperVersion",
                "openminds.publications.ScholarlyArticle",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:keyword",
            reverse="keywords",
            multiple=True,
            doc="reverse of 'keyword'",
        ),
        Property(
            "is_modeled_by",
            "openminds.core.Strain",
            "^vocab:diseaseModel",
            reverse="disease_models",
            multiple=True,
            doc="reverse of 'diseaseModel'",
        ),
        Property(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Property(
            "specimen_state",
            [
                "openminds.core.SubjectGroupState",
                "openminds.core.SubjectState",
                "openminds.core.TissueSampleCollectionState",
                "openminds.core.TissueSampleState",
            ],
            "^vocab:pathology",
            reverse="pathologies",
            multiple=True,
            doc="reverse of 'pathology'",
        ),
        Property(
            "studied_in",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.ValidationTest",
                "openminds.computation.Visualization",
                "openminds.core.DatasetVersion",
                "openminds.core.Model",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimen_prep.CranialWindowPreparation",
                "openminds.specimen_prep.TissueCulturePreparation",
                "openminds.specimen_prep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:studyTarget",
            reverse="study_targets",
            multiple=True,
            doc="reverse of 'studyTarget'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        describes=None,
        description=None,
        interlex_identifier=None,
        is_modeled_by=None,
        is_used_to_group=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        specimen_state=None,
        studied_in=None,
        synonyms=None,
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
            definition=definition,
            describes=describes,
            description=description,
            interlex_identifier=interlex_identifier,
            is_modeled_by=is_modeled_by,
            is_used_to_group=is_used_to_group,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            specimen_state=specimen_state,
            studied_in=studied_in,
            synonyms=synonyms,
        )
