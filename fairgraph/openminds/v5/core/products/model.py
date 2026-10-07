"""
Structured information on a computational model (concept level).
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Model as OMModel
from fairgraph import KGObject


from openminds import IRI


class Model(KGObject, OMModel):
    """
    Structured information on a computational model (concept level).
    """

    type_ = "https://openminds.om-i.org/types/Model"
    default_space = "model"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "comments",
            "openminds.v5.core.Comment",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
        Property(
            "has_versions",
            "openminds.v5.core.ModelVersion",
            "isVersionOf",
            reverse="is_version_of",
            multiple=True,
            description="reverse of 'is_version_of'",
        ),
        Property(
            "is_part_of",
            ["openminds.v5.core.Project", "openminds.v5.core.ResearchProductGroup"],
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "learning_resources",
            "openminds.v5.publications.LearningResource",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
    ]
    aliases = {"name": "full_name", "model_scope": "scope", "alias": "short_name"}
    existence_query_properties = ("full_name",)
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        abstraction_level=None,
        comments=None,
        contributions=None,
        contributor_affiliations=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        full_name=None,
        has_versions=None,
        homepage=None,
        how_to_cite=None,
        is_part_of=None,
        keywords=None,
        learning_resources=None,
        model_scope=None,
        related_publications=None,
        scope=None,
        short_name=None,
        study_targets=None,
        support_channels=None,
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
            abstraction_level=abstraction_level,
            comments=comments,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            full_name=full_name,
            has_versions=has_versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_part_of=is_part_of,
            keywords=keywords,
            learning_resources=learning_resources,
            model_scope=model_scope,
            related_publications=related_publications,
            scope=scope,
            short_name=short_name,
            study_targets=study_targets,
            support_channels=support_channels,
        )
