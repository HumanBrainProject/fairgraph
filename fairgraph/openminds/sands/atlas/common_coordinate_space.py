"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import KGObject, IRI
from fairgraph.fields import Field




class CommonCoordinateSpace(KGObject):
    """

    """
    default_space = "atlas"
    type = ["https://openminds.ebrains.eu/sands/CommonCoordinateSpace"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("name", str, "vocab:fullName", multiple=False, required=True,
              doc="Whole, non-abbreviated name of the common coordinate space."),
        Field("alias", str, "vocab:shortName", multiple=False, required=True,
              doc="Shortened or fully abbreviated name of the common coordinate space."),
        Field("abbreviation", str, "vocab:abbreviation", multiple=False, required=False,
              doc="no description available"),
        Field("authors", ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"], "vocab:author", multiple=True, required=False,
              doc="Creator of a literary or creative work, as well as a dataset publication."),
        Field("custodians", ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"], "vocab:custodian", multiple=True, required=False,
              doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product."),
        Field("description", str, "vocab:description", multiple=False, required=True,
              doc="Longer statement or account giving the characteristics of the common coordinate space."),
        Field("digital_identifier", ["openminds.core.DOI", "openminds.core.ISBN", "openminds.core.RRID"], "vocab:digitalIdentifier", multiple=False, required=False,
              doc="Digital handle to identify objects or legal persons."),
        Field("versions", "openminds.sands.CommonCoordinateSpaceVersion", "vocab:hasVersion", multiple=True, required=True,
              doc="Reference to variants of an original."),
        Field("homepage", IRI, "vocab:homepage", multiple=False, required=False,
              doc="Main website of the common coordinate space."),
        Field("how_to_cite", str, "vocab:howToCite", multiple=False, required=False,
              doc="Preferred format for citing a particular object or legal person."),
        Field("ontology_identifiers", str, "vocab:ontologyIdentifier", multiple=True, required=False,
              doc="Term or code used to identify the common coordinate space registered within a particular ontology."),
        Field("used_species", "openminds.controlledterms.Species", "vocab:usedSpecies", multiple=False, required=True,
              doc="no description available"),

    ]
    existence_query_fields = ('alias', 'version_identifier')
