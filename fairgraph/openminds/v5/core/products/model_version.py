"""
Structured information on a computational model (version level).
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import ModelVersion as OMModelVersion
from fairgraph import KGObject

from urllib.request import urlretrieve
from pathlib import Path
from fairgraph.utility import accepted_terms_of_use
from datetime import date
from openminds import IRI


class ModelVersion(KGObject, OMModelVersion):
    """
    Structured information on a computational model (version level).
    """

    type_ = "https://openminds.om-i.org/types/ModelVersion"
    default_space = "model"
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
            "has_variants",
            "openminds.v5.core.ModelVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
        ),
        Property(
            "is_input_to",
            [
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Simulation",
            ],
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
        ),
        Property(
            "is_location_of",
            "openminds.v5.core.ServiceLink",
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
        Property(
            "is_output_of",
            "openminds.v5.computation.Optimization",
            "output",
            reverse="outputs",
            multiple=True,
            description="reverse of 'outputs'",
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
        Property(
            "publication",
            "openminds.v5.publications.LivePaperVersion",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("full_name", "version_identifier")

    def __init__(
        self,
        name=None,
        alias=None,
        accessibility=None,
        comments=None,
        configuration=None,
        contributions=None,
        contributor_affiliations=None,
        copyright=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        entry_point=None,
        formats=None,
        full_name=None,
        funding=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        input_data=None,
        is_input_to=None,
        is_location_of=None,
        is_output_of=None,
        is_part_of=None,
        is_preceded_by=None,
        is_used_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        output_data=None,
        publication=None,
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
            configuration=configuration,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            copyright=copyright,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            entry_point=entry_point,
            formats=formats,
            full_name=full_name,
            funding=funding,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            input_data=input_data,
            is_input_to=is_input_to,
            is_location_of=is_location_of,
            is_output_of=is_output_of,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_used_by=is_used_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            output_data=output_data,
            publication=publication,
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

    def download(self, local_path, client, accept_terms_of_use=False):
        if accepted_terms_of_use(client, accept_terms_of_use=accept_terms_of_use):
            repo = self.repository.resolve(client, release_status=self.release_status or None)
            if repo.iri.value.startswith("https://object.cscs.ch/v1/AUTH") or repo.iri.value.startswith(
                "https://data-proxy.ebrains.eu/api/v1/buckets"
            ):
                zip_archive_url = f"https://data.kg.ebrains.eu/zip?container={repo.iri.value}"
            else:
                raise NotImplementedError("Download not yet implemented for this repository type")
            if local_path.endswith(".zip"):
                local_filename = Path(local_path)
            else:
                local_filename = Path(local_path) / (zip_archive_url.split("/")[-1] + ".zip")
            local_filename.parent.mkdir(parents=True, exist_ok=True)
            local_filename, headers = urlretrieve(zip_archive_url, local_filename)
            return local_filename, repo.iri.value

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
