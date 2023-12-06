"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class LivePaper(KGObject):
    """
    <description not available>
    """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/LivePaper"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the live paper."),
        Field(
            "alias",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the live paper.",
        ),
        Field(
            "authors",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:author",
            multiple=True,
            required=True,
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
            doc="Longer statement or account giving the characteristics of the live paper.",
        ),
        Field(
            "digital_identifier",
            "openminds.core.DOI",
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the live paper."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Field(
            "versions",
            "openminds.publications.LivePaperVersion",
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
            "is_part_of",
            ["openminds.core.Project", "openminds.core.ResearchProductGroup"],
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
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
    existence_query_fields = ("name", "alias")

    def __init__(
        self,
        name=None,
        alias=None,
        authors=None,
        custodians=None,
        description=None,
        digital_identifier=None,
        homepage=None,
        how_to_cite=None,
        versions=None,
        comments=None,
        is_part_of=None,
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
            authors=authors,
            custodians=custodians,
            description=description,
            digital_identifier=digital_identifier,
            homepage=homepage,
            how_to_cite=how_to_cite,
            versions=versions,
            comments=comments,
            is_part_of=is_part_of,
            learning_resources=learning_resources,
        )
