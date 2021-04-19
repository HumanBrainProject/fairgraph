"""

"""

# this file was auto-generated


from fairgraph.base import KGObject
from fairgraph.fields import Field


class DOI(KGObject):
    """
    
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/core/DOI"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("identifier", str, "vocab:identifier", multiple=False, required=False,
              doc="Term or code used to identify something or someone."),
        
    ]
    existence_query_fields = ('name',)