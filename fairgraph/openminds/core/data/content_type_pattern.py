"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ContentTypePattern(KGObject):
    """
    <description not available>
    """

    default_space = "files"
    type_ = "https://openminds.ebrains.eu/core/ContentTypePattern"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "content_type",
            "openminds.core.ContentType",
            "vocab:contentType",
            required=True,
            doc="no description available",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property("regex", str, "vocab:regex", required=True, doc="no description available"),
    ]
    reverse_properties = [
        Property(
            "identifies_content_of",
            "openminds.core.FileRepository",
            "^vocab:contentTypePattern",
            reverse="content_type_patterns",
            multiple=True,
            doc="reverse of 'contentTypePattern'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        content_type=None,
        identifies_content_of=None,
        regex=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            lookup_label=lookup_label,
            content_type=content_type,
            identifies_content_of=identifies_content_of,
            regex=regex,
        )
