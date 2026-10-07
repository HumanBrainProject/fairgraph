"""
Structured information about the description of a prospective workflow.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.computation import WorkflowRecipe as OMWorkflowRecipe
from fairgraph import KGObject


from openminds import IRI


class WorkflowRecipe(KGObject, OMWorkflowRecipe):
    """
    Structured information about the description of a prospective workflow.
    """

    type_ = "https://openminds.om-i.org/types/WorkflowRecipe"
    default_space = "computation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "comments",
            "openminds.v4.core.Comment",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
        Property(
            "is_part_of",
            ["openminds.v4.core.Project", "openminds.v4.core.ResearchProductGroup"],
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "learning_resources",
            "openminds.v4.publications.LearningResource",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
