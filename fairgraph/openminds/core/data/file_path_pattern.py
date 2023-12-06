"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class FilePathPattern(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = ["https://openminds.ebrains.eu/core/FilePathPattern"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "grouping_types",
            "openminds.controlledterms.FileBundleGrouping",
            "vocab:groupingType",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Field("regex", str, "vocab:regex", required=True, doc="no description available"),
    ]

    def __init__(self, grouping_types=None, regex=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, grouping_types=grouping_types, regex=regex)
