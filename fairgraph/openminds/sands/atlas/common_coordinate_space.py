"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class CommonCoordinateSpace(KGObject):
    """
    <description not available>
    """

    default_space = "atlas"
    type_ = ["https://openminds.ebrains.eu/sands/CommonCoordinateSpace"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:fullName",
            required=True,
            doc="Whole, non-abbreviated name of the common coordinate space.",
        ),
        Field(
            "alias",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the common coordinate space.",
        ),
        Field("abbreviation", str, "vocab:abbreviation", doc="no description available"),
        Field(
            "authors",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:author",
            multiple=True,
            doc="Creator of a literary or creative work, as well as a dataset publication.",
        ),
        Field(
            "custodians",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:custodian",
            multiple=True,
            doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the common coordinate space.",
        ),
        Field(
            "digital_identifier",
            ["openminds.core.DOI", "openminds.core.ISBN", "openminds.core.RRID"],
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the common coordinate space."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Field(
            "ontology_identifiers",
            str,
            "vocab:ontologyIdentifier",
            multiple=True,
            doc="Term or code used to identify the common coordinate space registered within a particular ontology.",
        ),
        Field(
            "used_species",
            "openminds.controlledterms.Species",
            "vocab:usedSpecies",
            required=True,
            doc="no description available",
        ),
        Field(
            "versions",
            "openminds.sands.CommonCoordinateSpaceVersion",
            "vocab:hasVersion",
            multiple=True,
            required=True,
            doc="Reference to variants of an original.",
        ),
        Field(
            "comments",
            "openminds.core.Comment",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
        Field(
            "is_input_to",
            "openminds.core.DatasetVersion",
            "^vocab:inputData",
            reverse="input_data",
            multiple=True,
            doc="reverse of 'inputData'",
        ),
        Field(
            "is_part_of",
            ["openminds.core.Project", "openminds.core.ResearchProductGroup"],
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Field(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Field(
            "learning_resources",
            "openminds.publications.LearningResource",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
    ]
    existence_query_fields = ("alias", "version_identifier")

    def __init__(
        self,
        name=None,
        alias=None,
        abbreviation=None,
        authors=None,
        custodians=None,
        description=None,
        digital_identifier=None,
        homepage=None,
        how_to_cite=None,
        ontology_identifiers=None,
        used_species=None,
        versions=None,
        comments=None,
        is_input_to=None,
        is_part_of=None,
        is_used_to_group=None,
        learning_resources=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            alias=alias,
            abbreviation=abbreviation,
            authors=authors,
            custodians=custodians,
            description=description,
            digital_identifier=digital_identifier,
            homepage=homepage,
            how_to_cite=how_to_cite,
            ontology_identifiers=ontology_identifiers,
            used_species=used_species,
            versions=versions,
            comments=comments,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            is_used_to_group=is_used_to_group,
            learning_resources=learning_resources,
        )
