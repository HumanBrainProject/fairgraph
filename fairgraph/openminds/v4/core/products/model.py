"""
Structured information on a computational model (concept level).
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Model as OMModel
from fairgraph import KGObject


from openminds import IRI


class Model(KGObject, OMModel):
    """
    Structured information on a computational model (concept level).
    """

    type_ = "https://openminds.om-i.org/types/Model"
    default_space = "model"
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
    aliases = {"name": "full_name", "versions": "has_versions", "model_scope": "scope", "alias": "short_name"}
    existence_query_properties = ("full_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        abstraction_level=None,
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
        model_scope=None,
        scope=None,
        short_name=None,
        study_targets=None,
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
            abstraction_level=abstraction_level,
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
            model_scope=model_scope,
            scope=scope,
            short_name=short_name,
            study_targets=study_targets,
            versions=versions,
        )
