"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - cell-attached patch
         - A variation of the patch-clamp technique in which the cell membrane remains intact.
       * - perforated patch
         - A variation of the patch-clamp technique in which the cell membrane is perforated.
       * - loose patch
         - A variation of the patch-clamp technique involving a seal with low electrical resistance.
       * - inside-out patch
         - A variation of the patch-clamp technique in which a patch of membrane is excised and the cytosolic surface exposed.
       * - outside-out patch
         - A variation of the patch-clamp technique in which a patch of membrane is excised and the external surface exposed.
       * - whole-cell patch
         - A variation of the patch-clamp technique in which the patch is ruptured, giving access to the intracellular space.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import KGObject, IRI
from fairgraph.fields import Field




class PatchClampVariation(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - cell-attached patch
         - A variation of the patch-clamp technique in which the cell membrane remains intact.
       * - perforated patch
         - A variation of the patch-clamp technique in which the cell membrane is perforated.
       * - loose patch
         - A variation of the patch-clamp technique involving a seal with low electrical resistance.
       * - inside-out patch
         - A variation of the patch-clamp technique in which a patch of membrane is excised and the cytosolic surface exposed.
       * - outside-out patch
         - A variation of the patch-clamp technique in which a patch of membrane is excised and the external surface exposed.
       * - whole-cell patch
         - A variation of the patch-clamp technique in which the patch is ruptured, giving access to the intracellular space.

    """
    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/PatchClampVariation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the patch clamp variation."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the patch clamp variation."),
        Field("interlex_identifier", IRI, "vocab:interlexIdentifier", multiple=False, required=False,
              doc="Persistent identifier for a term registered in the InterLex project."),
        Field("knowledge_space_link", IRI, "vocab:knowledgeSpaceLink", multiple=False, required=False,
              doc="Persistent link to an encyclopedia entry in the Knowledge Space project."),
        Field("preferred_ontology_identifier", IRI, "vocab:preferredOntologyIdentifier", multiple=False, required=False,
              doc="Persistent identifier of a preferred ontological term."),
        Field("synonyms", str, "vocab:synonym", multiple=True, required=False,
              doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses."),

    ]
    existence_query_fields = ('name',)
