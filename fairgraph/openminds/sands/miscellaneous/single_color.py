"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class SingleColor(KGObject):
    """
    <description not available>
    """

    default_space = "atlas"
    type_ = "https://openminds.ebrains.eu/sands/SingleColor"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("value", str, "vocab:value", required=True, doc="Entry for a property."),
    ]
    existence_query_properties = ("value",)

    def __init__(self, value=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, space=space, scope=scope, data=data, value=value)
