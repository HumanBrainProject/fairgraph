"""
Structured information about a specific implementation of a validation test.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.computation import ValidationTestVersion as OMValidationTestVersion
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class ValidationTestVersion(KGObject, OMValidationTestVersion):
    """
    Structured information about a specific implementation of a validation test.
    """

    type_ = "https://openminds.om-i.org/types/ValidationTestVersion"
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
            "is_input_to",
            ["openminds.v4.computation.DataCopy", "openminds.v4.computation.ModelValidation"],
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
        ),
        Property(
            "is_old_version_of",
            "openminds.v4.computation.ValidationTestVersion",
            "isNewVersionOf",
            reverse="is_new_version_of",
            multiple=True,
            description="reverse of 'is_new_version_of'",
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
            "is_version_of",
            "openminds.v4.computation.ValidationTest",
            "hasVersion",
            reverse="has_versions",
            multiple=True,
            description="reverse of 'has_versions'",
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
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("short_name", "version_identifier")

    def __init__(
        self,
        name=None,
        alias=None,
        accessibility=None,
        comments=None,
        configuration=None,
        copyright=None,
        custodians=None,
        description=None,
        developers=None,
        digital_identifier=None,
        entry_point=None,
        format=None,
        full_documentation=None,
        full_name=None,
        funding=None,
        homepage=None,
        how_to_cite=None,
        is_alternative_version_of=None,
        is_input_to=None,
        is_new_version_of=None,
        is_old_version_of=None,
        is_part_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        licenses=None,
        other_contributions=None,
        reference_data=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        support_channels=None,
        version_identifier=None,
        version_innovation=None,
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
            configuration=configuration,
            copyright=copyright,
            custodians=custodians,
            description=description,
            developers=developers,
            digital_identifier=digital_identifier,
            entry_point=entry_point,
            format=format,
            full_documentation=full_documentation,
            full_name=full_name,
            funding=funding,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_alternative_version_of=is_alternative_version_of,
            is_input_to=is_input_to,
            is_new_version_of=is_new_version_of,
            is_old_version_of=is_old_version_of,
            is_part_of=is_part_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            licenses=licenses,
            other_contributions=other_contributions,
            reference_data=reference_data,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            support_channels=support_channels,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
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
