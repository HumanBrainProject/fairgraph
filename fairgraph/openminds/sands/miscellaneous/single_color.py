"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class SingleColor(KGObject):
    """

    """
    default_space = "atlas"
    type_ = ["https://openminds.ebrains.eu/sands/SingleColor"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("value", str, "vocab:value", multiple=False, required=True,
              doc="Entry for a property."),

    ]
    existence_query_fields = ('value',)
