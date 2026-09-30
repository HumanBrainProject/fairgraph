"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import ParcellationEntity as OMParcellationEntity
from fairgraph import KGObject


class ParcellationEntity(KGObject, OMParcellationEntity):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ParcellationEntity"
    default_space = "atlas"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_children",
            "openminds.v5.sands.ParcellationEntity",
            "hasParent",
            reverse="has_parents",
            multiple=True,
            description="reverse of 'has_parents'",
        ),
        Property(
            "has_versions",
            "openminds.v5.sands.ParcellationEntityVersion",
            "isVersionOf",
            reverse="is_version_of",
            multiple=True,
            description="reverse of 'is_version_of'",
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
    sort_property = "lookup_label"

    def __init__(
        self,
        name=None,
        lookup_label=None,
        abbreviation=None,
        alternate_names=None,
        definition=None,
        has_children=None,
        has_parents=None,
        has_versions=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        ontology_identifiers=None,
        related_interspecies_anatomy=None,
        studied_in=None,
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
            lookup_label=lookup_label,
            abbreviation=abbreviation,
            alternate_names=alternate_names,
            definition=definition,
            has_children=has_children,
            has_parents=has_parents,
            has_versions=has_versions,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            ontology_identifiers=ontology_identifiers,
            related_interspecies_anatomy=related_interspecies_anatomy,
            studied_in=studied_in,
        )
