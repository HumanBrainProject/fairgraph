"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import FileRepositoryStructure as OMFileRepositoryStructure
from fairgraph import KGObject


class FileRepositoryStructure(KGObject, OMFileRepositoryStructure):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/FileRepositoryStructure"
    default_space = "files"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "structures",
            "openminds.v4.core.FileRepository",
            "structurePattern",
            reverse="structure_pattern",
            multiple=True,
            description="reverse of 'structure_pattern'",
        ),
    ]
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        file_path_patterns=None,
        structures=None,
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
            file_path_patterns=file_path_patterns,
            structures=structures,
        )
