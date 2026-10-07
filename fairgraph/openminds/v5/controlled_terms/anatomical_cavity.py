"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.controlled_terms import AnatomicalCavity as OMAnatomicalCavity
from fairgraph import KGObject


from openminds import IRI


class AnatomicalCavity(KGObject, OMAnatomicalCavity):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/AnatomicalCavity"
    default_space = "controlled"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.HardwareProduct",
                "openminds.v5.core.Interface",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.Service",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.Book",
                "openminds.v5.publications.Chapter",
                "openminds.v5.publications.LearningResource",
                "openminds.v5.publications.LivePaper",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.publications.ScholarlyArticle",
                "openminds.v5.sands.AnatomicalAtlas",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFramework",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "keyword",
            reverse="keywords",
            multiple=True,
            description="reverse of 'keywords'",
        ),
        Property(
            "interspecies_relation",
            ["openminds.v5.sands.CustomAnatomicalEntity", "openminds.v5.sands.ParcellationEntity"],
            "relatedInterspeciesAnatomy",
            reverse="related_interspecies_anatomy",
            multiple=True,
            description="reverse of 'related_interspecies_anatomy'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v5.core.TissueSample",
                "openminds.v5.core.TissueSampleCollection",
                "openminds.v5.ephys.ElectrodeArrayUsage",
                "openminds.v5.ephys.ElectrodeUsage",
                "openminds.v5.ephys.PipetteUsage",
            ],
            ["anatomicalLocation", "anatomicalLocationOfElectrodes"],
            reverse=["anatomical_location", "anatomical_locations", "anatomical_locations_of_electrodes"],
            multiple=True,
            description="reverse of anatomical_location, anatomical_locations, anatomical_locations_of_electrodes",
        ),
        Property(
            "is_target_of",
            [
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
                "openminds.v5.neuroimaging.StaticMRIAcquisition",
                "openminds.v5.sands.AnatomicalTargetPosition",
            ],
            ["anatomicalTarget", "targetAnatomy"],
            reverse=["anatomical_targets", "target_anatomy"],
            multiple=True,
            description="reverse of anatomical_targets, target_anatomy",
        ),
        Property(
            "is_used_to_group",
            "openminds.v5.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "studied_in",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.Visualization",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.ephys.CellPatching",
                "openminds.v5.ephys.ElectrodePlacement",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.specimen_prep.CranialWindowPreparation",
                "openminds.v5.specimen_prep.TissueCulturePreparation",
                "openminds.v5.specimen_prep.TissueSampleSlicing",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            "studyTarget",
            reverse="study_targets",
            multiple=True,
            description="reverse of 'study_targets'",
        ),
    ]
    existence_query_properties = ("name",)
    sort_property = "name"

    def __init__(
        self,
        name=None,
        definition=None,
        describes=None,
        description=None,
        interspecies_relation=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        other_cross_references=None,
        other_ontology_identifiers=None,
        preferred_cross_reference=None,
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
            definition=definition,
            describes=describes,
            description=description,
            interspecies_relation=interspecies_relation,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            other_cross_references=other_cross_references,
            other_ontology_identifiers=other_ontology_identifiers,
            preferred_cross_reference=preferred_cross_reference,
            preferred_ontology_identifier=preferred_ontology_identifier,
            studied_in=studied_in,
            synonyms=synonyms,
        )
