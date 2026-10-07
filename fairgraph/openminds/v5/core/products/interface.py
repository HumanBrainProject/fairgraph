"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Interface as OMInterface
from fairgraph import KGObject


from openminds import IRI


class Interface(KGObject, OMInterface):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Interface"
    default_space = "interface"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
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
            "openminds.v5.core.InterfaceVersion",
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
        Property(
            "linked_from",
            "openminds.v5.core.ServiceLink",
            "service",
            reverse="services",
            multiple=True,
            description="reverse of 'services'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("short_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        comments=None,
        communication_protocol=None,
        contributions=None,
        contributor_affiliations=None,
        description=None,
        documentation=None,
        full_name=None,
        has_versions=None,
        homepage=None,
        how_to_cite=None,
        interface_type=None,
        is_part_of=None,
        keywords=None,
        learning_resources=None,
        linked_from=None,
        related_publications=None,
        short_name=None,
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
            comments=comments,
            communication_protocol=communication_protocol,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            description=description,
            documentation=documentation,
            full_name=full_name,
            has_versions=has_versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
            interface_type=interface_type,
            is_part_of=is_part_of,
            keywords=keywords,
            learning_resources=learning_resources,
            linked_from=linked_from,
            related_publications=related_publications,
            short_name=short_name,
            support_channels=support_channels,
        )
