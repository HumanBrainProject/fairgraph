"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class FileRepositoryStructure(KGObject):
    """
    <description not available>
    """

    default_space = "files"
    type_ = "https://openminds.ebrains.eu/core/FileRepositoryStructure"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "file_path_patterns",
            "openminds.core.FilePathPattern",
            "vocab:filePathPattern",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "structures",
            "openminds.core.FileRepository",
            "^vocab:structurePattern",
            reverse="structure_patterns",
            multiple=True,
            doc="reverse of 'structurePattern'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self, lookup_label=None, file_path_patterns=None, structures=None, id=None, data=None, space=None, scope=None
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            lookup_label=lookup_label,
            file_path_patterns=file_path_patterns,
            structures=structures,
        )
