"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObjectV3, IRI
from fairgraph.fields import Field




class HardwareSystem(KGObjectV3):
    """
    
    """
    default_space = "computation"
    type = ["https://openminds.ebrains.eu/computation/HardwareSystem"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the hardware system."),
        Field("version", str, "vocab:version", multiple=False, required=True,
              doc="no description available"),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the hardware system."),
        
    ]
    existence_query_fields = ('name', 'version')
