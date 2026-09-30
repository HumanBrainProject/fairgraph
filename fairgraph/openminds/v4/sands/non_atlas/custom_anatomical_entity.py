"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import CustomAnatomicalEntity as OMCustomAnatomicalEntity
from fairgraph import KGObject


class CustomAnatomicalEntity(KGObject, OMCustomAnatomicalEntity):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/CustomAnatomicalEntity"
    default_space = "spatial"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
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
        has_annotations=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        related_uberon_term=None,
        relation_assessments=None,
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
            has_annotations=has_annotations,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            related_uberon_term=related_uberon_term,
            relation_assessments=relation_assessments,
            studied_in=studied_in,
        )
