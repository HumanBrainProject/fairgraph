"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.controlled_terms import UBERONParcellation as OMUBERONParcellation
from fairgraph import KGObject


from openminds import IRI


class UBERONParcellation(KGObject, OMUBERONParcellation):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/UBERONParcellation"
    default_space = "controlled"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "defines",
            ["openminds.v4.sands.CustomAnatomicalEntity", "openminds.v4.sands.ParcellationEntity"],
            "relatedUBERONTerm",
            reverse="related_uberon_term",
            multiple=True,
            description="reverse of 'related_uberon_term'",
        ),
        Property(
            "describes",
            [
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.publications.ScholarlyArticle",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "keyword",
            reverse="keywords",
            multiple=True,
            description="reverse of 'keywords'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v4.core.TissueSample",
                "openminds.v4.core.TissueSampleCollection",
                "openminds.v4.ephys.ElectrodeArrayUsage",
                "openminds.v4.ephys.ElectrodeUsage",
                "openminds.v4.ephys.PipetteUsage",
            ],
            ["anatomicalLocation", "anatomicalLocationOfElectrodes"],
            reverse=["anatomical_location", "anatomical_locations", "anatomical_locations_of_electrodes"],
            multiple=True,
            description="reverse of anatomical_location, anatomical_locations, anatomical_locations_of_electrodes",
        ),
        Property(
            "is_target_of",
            "openminds.v4.sands.AnatomicalTargetPosition",
            "anatomicalTarget",
            reverse="anatomical_targets",
            multiple=True,
            description="reverse of 'anatomical_targets'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v4.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "studied_in",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.ValidationTest",
                "openminds.v4.computation.Visualization",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.Model",
                "openminds.v4.core.ProtocolExecution",
                "openminds.v4.ephys.CellPatching",
                "openminds.v4.ephys.ElectrodePlacement",
                "openminds.v4.ephys.RecordingActivity",
                "openminds.v4.specimen_prep.CranialWindowPreparation",
                "openminds.v4.specimen_prep.TissueCulturePreparation",
                "openminds.v4.specimen_prep.TissueSampleSlicing",
                "openminds.v4.stimulation.StimulationActivity",
            ],
            "studyTarget",
            reverse="study_targets",
            multiple=True,
            description="reverse of 'study_targets'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        defines=None,
        definition=None,
        describes=None,
        description=None,
        interlex_identifier=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        studied_in=None,
        synonyms=None,
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
            defines=defines,
            definition=definition,
            describes=describes,
            description=description,
            interlex_identifier=interlex_identifier,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            studied_in=studied_in,
            synonyms=synonyms,
        )
