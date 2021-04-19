"""
Structured information on a hash.
"""

# this file was auto-generated


from fairgraph.base import KGObject
from fairgraph.fields import Field


class Hash(KGObject):
    """
    Structured information on a hash.
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/core/Hash"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("algorithm", str, "vocab:algorithm", multiple=False, required=True,
              doc="Procedure for solving a mathematical problem in a finite number of steps. Can involve repetition of an operation."),
        Field("digest", str, "vocab:digest", multiple=False, required=True,
              doc="Summation or condensation of a body of information."),
        
    ]
    existence_query_fields = ('name',)