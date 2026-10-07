"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import SubjectGroup as OMSubjectGroup
from fairgraph import KGObject


class SubjectGroup(KGObject, OMSubjectGroup):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SubjectGroup"
    default_space = "dataset"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_parts",
            ["openminds.v5.core.Subject", "openminds.v5.core.SubjectGroup"],
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
        Property(
            "has_study_results_in",
            "openminds.v5.core.DatasetVersion",
            "studiedSpecimen",
            reverse="studied_specimens",
            multiple=True,
            description="reverse of 'studied_specimens'",
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
            "used_in",
            ["openminds.v5.sands.AnatomicalAtlasVersion", "openminds.v5.sands.CommonCoordinateFrameworkVersion"],
            "usedSpecimen",
            reverse="used_specimens",
            multiple=True,
            description="reverse of 'used_specimens'",
        ),
    ]
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        additional_remarks=None,
        biological_sexes=None,
        has_parts=None,
        has_study_results_in=None,
        internal_identifier=None,
        is_part_of=None,
        is_used_to_group=None,
        number_of_subjects=None,
        species=None,
        studied_states=None,
        used_in=None,
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
            lookup_label=lookup_label,
            additional_remarks=additional_remarks,
            biological_sexes=biological_sexes,
            has_parts=has_parts,
            has_study_results_in=has_study_results_in,
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            is_used_to_group=is_used_to_group,
            number_of_subjects=number_of_subjects,
            species=species,
            studied_states=studied_states,
            used_in=used_in,
        )
