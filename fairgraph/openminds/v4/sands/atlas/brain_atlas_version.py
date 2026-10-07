"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import BrainAtlasVersion as OMBrainAtlasVersion
from fairgraph import KGObject

from urllib.request import urlretrieve
from pathlib import Path
from fairgraph.utility import accepted_terms_of_use
from datetime import date
from openminds import IRI


class BrainAtlasVersion(KGObject, OMBrainAtlasVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/BrainAtlasVersion"
    default_space = "atlas"
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
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.ProtocolExecution",
            ],
            ["input", "inputData"],
            reverse=["input_data", "inputs"],
            multiple=True,
            description="reverse of input_data, inputs",
        ),
        Property(
            "is_old_version_of",
            "openminds.v4.sands.BrainAtlasVersion",
            "isNewVersionOf",
            reverse="is_new_version_of",
            multiple=True,
            description="reverse of 'is_new_version_of'",
        ),
        Property(
            "is_part_of",
            [
                "openminds.v4.core.Project",
                "openminds.v4.core.ResearchProductGroup",
                "openminds.v4.core.SoftwareVersion",
            ],
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "is_version_of",
            "openminds.v4.sands.BrainAtlas",
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
        abbreviation=None,
        accessibility=None,
        authors=None,
        comments=None,
        coordinate_space=None,
        copyright=None,
        custodians=None,
        description=None,
        digital_identifier=None,
        full_documentation=None,
        full_name=None,
        funding=None,
        has_terminology=None,
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
        license=None,
        major_version_identifier=None,
        ontology_identifier=None,
        other_contributions=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        support_channels=None,
        type=None,
        used_specimens=None,
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
            abbreviation=abbreviation,
            accessibility=accessibility,
            authors=authors,
            comments=comments,
            coordinate_space=coordinate_space,
            copyright=copyright,
            custodians=custodians,
            description=description,
            digital_identifier=digital_identifier,
            full_documentation=full_documentation,
            full_name=full_name,
            funding=funding,
            has_terminology=has_terminology,
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
            license=license,
            major_version_identifier=major_version_identifier,
            ontology_identifier=ontology_identifier,
            other_contributions=other_contributions,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            support_channels=support_channels,
            type=type,
            used_specimens=used_specimens,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
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

    def get_authors(self, client, release_status="released"):
        return self._get_inherited_property("authors", client, release_status)
