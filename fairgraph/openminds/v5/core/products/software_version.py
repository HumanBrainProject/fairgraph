"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import SoftwareVersion as OMSoftwareVersion
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class SoftwareVersion(KGObject, OMSoftwareVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SoftwareVersion"
    default_space = "software"
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
            "openminds.v5.core.SoftwareVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
        ),
        Property(
            "is_dependency_of",
            "openminds.v5.computation.ServiceDeployment",
            "dependsOn",
            reverse="depends_on",
            multiple=True,
            description="reverse of 'depends_on'",
        ),
        Property(
            "is_input_to",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
            ],
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
        ),
        Property(
            "is_part_of",
            [
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Project",
                "openminds.v5.core.ResearchProductGroup",
                "openminds.v5.core.Setup",
            ],
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
            "publication",
            "openminds.v5.publications.LivePaperVersion",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
        Property(
            "used_in",
            ["openminds.v5.computation.Environment", "openminds.v5.computation.SoftwareAgent"],
            "software",
            reverse="software",
            multiple=True,
            description="reverse of 'software'",
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
        dependencies=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        full_name=None,
        funding=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        implements=None,
        input_formats=None,
        is_dependency_of=None,
        is_input_to=None,
        is_part_of=None,
        is_preceded_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        languages=None,
        learning_resources=None,
        operating_devices=None,
        operating_systems=None,
        output_formats=None,
        programming_languages=None,
        publication=None,
        publication_status=None,
        related_publications=None,
        release_date=None,
        repository=None,
        scopes=None,
        short_name=None,
        support_channels=None,
        usage_conditions=None,
        used_in=None,
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
            dependencies=dependencies,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            full_name=full_name,
            funding=funding,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            implements=implements,
            input_formats=input_formats,
            is_dependency_of=is_dependency_of,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            languages=languages,
            learning_resources=learning_resources,
            operating_devices=operating_devices,
            operating_systems=operating_systems,
            output_formats=output_formats,
            programming_languages=programming_languages,
            publication=publication,
            publication_status=publication_status,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            scopes=scopes,
            short_name=short_name,
            support_channels=support_channels,
            usage_conditions=usage_conditions,
            used_in=used_in,
            version_identifier=version_identifier,
            version_specification=version_specification,
        )

    def _get_inherited_property(self, property_name, client, release_status="released"):
        value = getattr(self, property_name)
        if value:
            return value
        else:
            parent = self.is_version_of.resolve(client, release_status=release_status)
            return getattr(parent, property_name)

    def get_full_name(self, client, release_status="released"):
        return self._get_inherited_property("full_name", client, release_status)

    def get_short_name(self, client, release_status="released"):
        return self._get_inherited_property("short_name", client, release_status)

    def get_description(self, client, release_status="released"):
        return self._get_inherited_property("description", client, release_status)

    def get_developers(self, client, release_status="released"):
        return self._get_inherited_property("developers", client, release_status)
