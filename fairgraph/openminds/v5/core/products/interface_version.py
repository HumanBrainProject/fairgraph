"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import InterfaceVersion as OMInterfaceVersion
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class InterfaceVersion(KGObject, OMInterfaceVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/InterfaceVersion"
    default_space = "interface"
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
            "has_variants",
            "openminds.v5.core.InterfaceVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
        ),
        Property(
            "is_implemented_by",
            "openminds.v5.core.SoftwareVersion",
            "implements",
            reverse="implements",
            multiple=True,
            description="reverse of 'implements'",
        ),
        Property(
            "is_interface_of",
            "openminds.v5.computation.DeployedInterface",
            "interface",
            reverse="interface",
            multiple=True,
            description="reverse of 'interface'",
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
    existence_query_properties = ("short_name", "version_identifier")
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        accessibility=None,
        comments=None,
        contributions=None,
        contributor_affiliations=None,
        copyright=None,
        description=None,
        documentation=None,
        full_name=None,
        funding=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        is_implemented_by=None,
        is_interface_of=None,
        is_part_of=None,
        is_preceded_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        linked_from=None,
        publication_status=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        specification=None,
        support_channels=None,
        usage_conditions=None,
        version_identifier=None,
        version_specification=None,
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
            accessibility=accessibility,
            comments=comments,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            copyright=copyright,
            description=description,
            documentation=documentation,
            full_name=full_name,
            funding=funding,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_implemented_by=is_implemented_by,
            is_interface_of=is_interface_of,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            linked_from=linked_from,
            publication_status=publication_status,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            specification=specification,
            support_channels=support_channels,
            usage_conditions=usage_conditions,
            version_identifier=version_identifier,
            version_specification=version_specification,
        )
