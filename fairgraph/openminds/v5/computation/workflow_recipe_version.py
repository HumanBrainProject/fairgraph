"""
Structured information about a specific implemented version of a workflow recipe.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import WorkflowRecipeVersion as OMWorkflowRecipeVersion
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class WorkflowRecipeVersion(KGObject, OMWorkflowRecipeVersion):
    """
    Structured information about a specific implemented version of a workflow recipe.
    """

    type_ = "https://openminds.om-i.org/types/WorkflowRecipeVersion"
    default_space = "computation"
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
            "defined",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
                "openminds.v5.computation.WorkflowExecution",
            ],
            "recipe",
            reverse="recipe",
            multiple=True,
            description="reverse of 'recipe'",
        ),
        Property(
            "has_variants",
            "openminds.v5.computation.WorkflowRecipeVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
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
            "is_used_by",
            "openminds.v5.computation.ServiceDeployment",
            "uses",
            reverse="uses",
            multiple=True,
            description="reverse of 'uses'",
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
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("full_name", "version_identifier")
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
        defined=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        format=None,
        full_name=None,
        funding=None,
        has_parts=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        is_part_of=None,
        is_preceded_by=None,
        is_used_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        publication_status=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
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
            defined=defined,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            format=format,
            full_name=full_name,
            funding=funding,
            has_parts=has_parts,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_used_by=is_used_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            publication_status=publication_status,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            support_channels=support_channels,
            usage_conditions=usage_conditions,
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
