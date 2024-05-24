"""
Structured information about the description of a prospective workflow.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class WorkflowRecipe(KGObject):
    """
    Structured information about the description of a prospective workflow.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/WorkflowRecipe"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "custodians",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:custodian",
            multiple=True,
            doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the workflow recipe.",
        ),
        Property(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            required=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Property(
            "digital_identifier",
            "openminds.core.DOI",
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Property(
            "full_name",
            str,
            "vocab:fullName",
            required=True,
            doc="Whole, non-abbreviated name of the workflow recipe.",
        ),
        Property(
            "has_versions",
            "openminds.computation.WorkflowRecipeVersion",
            "vocab:hasVersion",
            multiple=True,
            required=True,
            doc="Reference to variants of an original.",
        ),
        Property("homepage", IRI, "vocab:homepage", doc="Main website of the workflow recipe."),
        Property(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Property(
            "short_name",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the workflow recipe.",
        ),
    ]
    reverse_properties = [
        Property(
            "comments",
            "openminds.core.Comment",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
        Property(
            "is_part_of",
            ["openminds.core.Project", "openminds.core.ResearchProductGroup"],
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Property(
            "learning_resources",
            "openminds.publications.LearningResource",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
    ]
    aliases = {"name": "full_name", "versions": "has_versions", "alias": "short_name"}
    existence_query_properties = ("full_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        comments=None,
        custodians=None,
        description=None,
        developers=None,
        digital_identifier=None,
        full_name=None,
        has_versions=None,
        homepage=None,
        how_to_cite=None,
        is_part_of=None,
        learning_resources=None,
        short_name=None,
        versions=None,
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
            comments=comments,
            custodians=custodians,
            description=description,
            developers=developers,
            digital_identifier=digital_identifier,
            full_name=full_name,
            has_versions=has_versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_part_of=is_part_of,
            learning_resources=learning_resources,
            short_name=short_name,
            versions=versions,
        )
