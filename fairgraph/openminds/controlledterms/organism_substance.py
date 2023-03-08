"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `arterial blood <http://purl.obolibrary.org/obo/UBERON_0013755>`_
         - 'Arterial blood' is the oxygenated portion of blood which occupies the pulmonary vein, the left chambers of the heart, and the arteries of the circulatory system.
       * - `venous blood <http://purl.obolibrary.org/obo/UBERON_0013756>`_
         - 'Venous blood' is deoxygenated blood which travels from the peripheral vessels, through the venous system into the right atrium of the heart.
       * - `blood <http://purl.obolibrary.org/obo/UBERON_0000178>`_
         - ''Blood' is a body fluid in the circulatory system of vertebrates that transports substances to and from cells (e.g. nutrients, oxygen or metabolic waste products). [[adapted from Wikipedia](https://en.wikipedia.org/wiki/Blood)]

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObject, IRI
from fairgraph.fields import Field




class OrganismSubstance(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - `arterial blood <http://purl.obolibrary.org/obo/UBERON_0013755>`_
         - 'Arterial blood' is the oxygenated portion of blood which occupies the pulmonary vein, the left chambers of the heart, and the arteries of the circulatory system.
       * - `venous blood <http://purl.obolibrary.org/obo/UBERON_0013756>`_
         - 'Venous blood' is deoxygenated blood which travels from the peripheral vessels, through the venous system into the right atrium of the heart.
       * - `blood <http://purl.obolibrary.org/obo/UBERON_0000178>`_
         - ''Blood' is a body fluid in the circulatory system of vertebrates that transports substances to and from cells (e.g. nutrients, oxygen or metabolic waste products). [[adapted from Wikipedia](https://en.wikipedia.org/wiki/Blood)]

    """
    default_space = "controlled"
    type = ["https://openminds.ebrains.eu/controlledTerms/OrganismSubstance"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the organism substance."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the organism substance."),
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
