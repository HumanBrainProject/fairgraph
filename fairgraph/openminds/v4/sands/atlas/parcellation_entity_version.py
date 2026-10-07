"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import ParcellationEntityVersion as OMParcellationEntityVersion
from fairgraph import KGObject


class ParcellationEntityVersion(KGObject, OMParcellationEntityVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ParcellationEntityVersion"
    default_space = "atlas"
    SORT_PRIORITY = ("lookupLabel", "name", "fullName", "shortName", "familyName", "abbreviation")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_children",
            "openminds.v4.sands.ParcellationEntityVersion",
            "hasParent",
            reverse="has_parents",
            multiple=True,
            description="reverse of 'has_parents'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v4.core.ServiceLink",
                "openminds.v4.core.TissueSample",
                "openminds.v4.core.TissueSampleCollection",
                "openminds.v4.ephys.ElectrodeArrayUsage",
                "openminds.v4.ephys.ElectrodeUsage",
                "openminds.v4.ephys.PipetteUsage",
            ],
            ["anatomicalLocation", "anatomicalLocationOfElectrodes", "dataLocation"],
            reverse=[
                "anatomical_location",
                "anatomical_locations",
                "anatomical_locations_of_electrodes",
                "data_location",
            ],
            multiple=True,
            description="reverse of anatomical_location, anatomical_locations, anatomical_locations_of_electrodes, data_location",
        ),
        Property(
            "is_part_of",
            "openminds.v4.sands.ParcellationTerminologyVersion",
            "hasEntity",
            reverse="has_entities",
            multiple=True,
            description="reverse of 'has_entities'",
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
            "is_version_of",
            "openminds.v4.sands.ParcellationEntity",
            "hasVersion",
            reverse="has_versions",
            multiple=True,
            description="reverse of 'has_versions'",
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
    existence_query_properties = ("name", "version_identifier")

    def __init__(
        self,
        name=None,
        lookup_label=None,
        abbreviation=None,
        additional_remarks=None,
        alternate_names=None,
        corrected_name=None,
        has_annotations=None,
        has_children=None,
        has_parents=None,
        is_location_of=None,
        is_part_of=None,
        is_target_of=None,
        is_used_to_group=None,
        is_version_of=None,
        ontology_identifiers=None,
        relation_assessments=None,
        studied_in=None,
        version_identifier=None,
        version_innovation=None,
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
            additional_remarks=additional_remarks,
            alternate_names=alternate_names,
            corrected_name=corrected_name,
            has_annotations=has_annotations,
            has_children=has_children,
            has_parents=has_parents,
            is_location_of=is_location_of,
            is_part_of=is_part_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            is_version_of=is_version_of,
            ontology_identifiers=ontology_identifiers,
            relation_assessments=relation_assessments,
            studied_in=studied_in,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
        )
