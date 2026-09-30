"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import ParcellationEntityVersion as OMParcellationEntityVersion
from fairgraph import KGObject


class ParcellationEntityVersion(KGObject, OMParcellationEntityVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ParcellationEntityVersion"
    default_space = "atlas"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_children",
            "openminds.v5.sands.ParcellationEntityVersion",
            "hasParent",
            reverse="has_parents",
            multiple=True,
            description="reverse of 'has_parents'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v5.core.ServiceLink",
                "openminds.v5.core.TissueSample",
                "openminds.v5.core.TissueSampleCollection",
                "openminds.v5.ephys.ElectrodeArrayUsage",
                "openminds.v5.ephys.ElectrodeUsage",
                "openminds.v5.ephys.PipetteUsage",
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
    existence_query_properties = ("name", "version_identifier")
    sort_property = "lookup_label"

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
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            is_version_of=is_version_of,
            ontology_identifiers=ontology_identifiers,
            relation_assessments=relation_assessments,
            studied_in=studied_in,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
        )
