"""
Structured information on a subject.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Subject as OMSubject
from fairgraph import KGObject


class Subject(KGObject, OMSubject):
    """
    Structured information on a subject.
    """

    type_ = "https://openminds.om-i.org/types/Subject"
    default_space = "dataset"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_study_results_in",
            "openminds.v4.core.DatasetVersion",
            "studiedSpecimen",
            reverse="studied_specimens",
            multiple=True,
            description="reverse of 'studied_specimens'",
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
            "used_in",
            ["openminds.v4.sands.BrainAtlasVersion", "openminds.v4.sands.CommonCoordinateSpaceVersion"],
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
        biological_sex=None,
        has_study_results_in=None,
        internal_identifier=None,
        is_part_of=None,
        is_used_to_group=None,
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
            biological_sex=biological_sex,
            has_study_results_in=has_study_results_in,
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            is_used_to_group=is_used_to_group,
            species=species,
            studied_states=studied_states,
            used_in=used_in,
        )
