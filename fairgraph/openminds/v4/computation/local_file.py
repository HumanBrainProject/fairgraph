"""
Structured information about a file that is not accessible via a URL.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.computation import LocalFile as OMLocalFile
from fairgraph import KGObject


class LocalFile(KGObject, OMLocalFile):
    """
    Structured information about a file that is not accessible via a URL.
    """

    type_ = "https://openminds.om-i.org/types/LocalFile"
    default_space = "computation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_output_of",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.Visualization",
            ],
            "output",
            reverse="outputs",
            multiple=True,
            description="reverse of 'outputs'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v4.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
    ]
    existence_query_properties = ("name", "hashes")

    def __init__(
        self,
        name=None,
        content_description=None,
        copy_of=None,
        data_types=None,
        format=None,
        hash=None,
        is_output_of=None,
        is_used_to_group=None,
        path=None,
        special_usage_role=None,
        storage_size=None,
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
            content_description=content_description,
            copy_of=copy_of,
            data_types=data_types,
            format=format,
            hash=hash,
            is_output_of=is_output_of,
            is_used_to_group=is_used_to_group,
            path=path,
            special_usage_role=special_usage_role,
            storage_size=storage_size,
        )
