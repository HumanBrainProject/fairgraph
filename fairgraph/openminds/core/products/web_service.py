"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from fairgraph.base import IRI


class WebService(KGObject):
    """
    <description not available>
    """

    default_space = "webservice"
    type_ = ["https://openminds.ebrains.eu/core/WebService"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the web service."),
        Field(
            "alias",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the web service.",
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
            doc="Longer statement or account giving the characteristics of the web service.",
        ),
        Field(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            required=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the web service."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Field(
            "versions",
            "openminds.core.WebServiceVersion",
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
            "has_accounts",
            "openminds.core.AccountInformation",
            "^vocab:service",
            reverse="services",
            multiple=True,
            doc="reverse of 'service'",
        ),
        Field(
            "hosts",
            "openminds.publications.LivePaperResourceItem",
            "^vocab:hostedBy",
            reverse="hosted_by",
            multiple=True,
            doc="reverse of 'hostedBy'",
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
    existence_query_fields = ("description", "developers", "name", "versions", "alias")

    def __init__(
        self,
        name=None,
        alias=None,
        custodians=None,
        description=None,
        developers=None,
        homepage=None,
        how_to_cite=None,
        versions=None,
        comments=None,
        has_accounts=None,
        hosts=None,
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
            custodians=custodians,
            description=description,
            developers=developers,
            homepage=homepage,
            how_to_cite=how_to_cite,
            versions=versions,
            comments=comments,
            has_accounts=has_accounts,
            hosts=hosts,
            is_part_of=is_part_of,
            learning_resources=learning_resources,
        )
