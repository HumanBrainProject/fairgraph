"""
Structured information on a subject.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field




class Subject(KGObject):
    """
    Structured information on a subject.
    """
    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/Subject"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", multiple=False, required=False,
              doc="no description available"),
        Field("biological_sex", "openminds.controlledterms.BiologicalSex", "vocab:biologicalSex", multiple=False, required=False,
              doc="Differentiation of individuals of most species (animals and plants) based on the type of gametes they produce."),
        Field("internal_identifier", str, "vocab:internalIdentifier", multiple=False, required=False,
              doc="Term or code that identifies the subject within a particular product."),
        Field("is_part_of", "openminds.core.SubjectGroup", "vocab:isPartOf", multiple=True, required=False,
              doc="Reference to the ensemble of multiple things or beings."),
        Field("species", ["openminds.controlledterms.Species", "openminds.core.Strain"], "vocab:species", multiple=False, required=True,
              doc="Category of biological classification comprising related organisms or populations potentially capable of interbreeding, and being designated by a binomial that consists of the name of a genus followed by a Latin or latinized uncapitalized noun or adjective."),
        Field("studied_states", "openminds.core.SubjectState", "vocab:studiedState", multiple=True, required=True,
              doc="Reference to a point in time at which the subject was studied in a particular mode or condition."),

    ]
    existence_query_fields = ('lookup_label',)

    def __init__(self, lookup_label=None, biological_sex=None, internal_identifier=None, is_part_of=None, species=None, studied_states=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, space=space, scope=scope, data=data, lookup_label=lookup_label, biological_sex=biological_sex, internal_identifier=internal_identifier, is_part_of=is_part_of, species=species, studied_states=studied_states)