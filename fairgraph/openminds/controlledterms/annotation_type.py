"""


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - annotation mask
         - An 'annotation mask' is a filled object masking an area or volume of interest.
       * - annotation point
         - 'Annotation point(s)' are individual point(s) that are annotated with the same label.
       * - annotation contour line
         - An 'annotation contour line' is a two-dimensional boundary of an area of interest.
       * - deterministic annotation
         - A 'deterministic annotation' provides an exact assignment of an entity or a list of entities to a defined annotation. The assingment itself can be based on a deterministic or maximum probability assumption.
       * - probabalistic annotation
         - A 'probabalistic annotation' provides the probability or probabilites to which an entity or a list of entities belong(s) to a defined annotation.
       * - annotation surface
         - An 'annotation surface' is a three-dimensional boundary of a volume of interest.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field




class AnnotationType(KGObject):
    """


    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - annotation mask
         - An 'annotation mask' is a filled object masking an area or volume of interest.
       * - annotation point
         - 'Annotation point(s)' are individual point(s) that are annotated with the same label.
       * - annotation contour line
         - An 'annotation contour line' is a two-dimensional boundary of an area of interest.
       * - deterministic annotation
         - A 'deterministic annotation' provides an exact assignment of an entity or a list of entities to a defined annotation. The assingment itself can be based on a deterministic or maximum probability assumption.
       * - probabalistic annotation
         - A 'probabalistic annotation' provides the probability or probabilites to which an entity or a list of entities belong(s) to a defined annotation.
       * - annotation surface
         - An 'annotation surface' is a three-dimensional boundary of a volume of interest.

    """
    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/AnnotationType"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:name", multiple=False, required=True,
              doc="Word or phrase that constitutes the distinctive designation of the annotation type."),
        Field("definition", str, "vocab:definition", multiple=False, required=False,
              doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the annotation type."),
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

    def __init__(self, name=None, definition=None, description=None, interlex_identifier=None, knowledge_space_link=None, preferred_ontology_identifier=None, synonyms=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, space=space, scope=scope, data=data, name=name, definition=definition, description=description, interlex_identifier=interlex_identifier, knowledge_space_link=knowledge_space_link, preferred_ontology_identifier=preferred_ontology_identifier, synonyms=synonyms)