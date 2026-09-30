"""
Structured information on data originating from human/animal studies or simulations (version level).
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import DatasetVersion as OMDatasetVersion
from fairgraph import KGObject

from urllib.request import urlretrieve
from pathlib import Path
from fairgraph.utility import accepted_terms_of_use
from datetime import date
from openminds import IRI


class DatasetVersion(KGObject, OMDatasetVersion):
    """
    Structured information on data originating from human/animal studies or simulations (version level).
    """

    type_ = "https://openminds.om-i.org/types/DatasetVersion"
    default_space = "dataset"
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
            "has_parts",
            [
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.ephys.CellPatching",
                "openminds.v5.ephys.ElectrodePlacement",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.neuroimaging.DynamicMRIAcquisition",
                "openminds.v5.neuroimaging.StaticMRIAcquisition",
                "openminds.v5.specimen_prep.CranialWindowPreparation",
                "openminds.v5.specimen_prep.TissueCulturePreparation",
                "openminds.v5.specimen_prep.TissueSampleSlicing",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
        Property(
            "has_variants",
            "openminds.v5.core.DatasetVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
        ),
        Property(
            "is_input_to",
            "openminds.v5.computation.DataCopy",
            "input",
            reverse="inputs",
            multiple=True,
            description="reverse of 'inputs'",
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
        data_types=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        ethics_jurisdiction=None,
        experimental_approaches=None,
        full_name=None,
        funding=None,
        has_parts=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        input_data=None,
        is_input_to=None,
        is_part_of=None,
        is_preceded_by=None,
        is_used_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        preparation_types=None,
        protocols=None,
        publication=None,
        publication_status=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        studied_specimens=None,
        study_targets=None,
        support_channels=None,
        techniques=None,
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
            data_types=data_types,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            ethics_jurisdiction=ethics_jurisdiction,
            experimental_approaches=experimental_approaches,
            full_name=full_name,
            funding=funding,
            has_parts=has_parts,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            input_data=input_data,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_used_by=is_used_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            preparation_types=preparation_types,
            protocols=protocols,
            publication=publication,
            publication_status=publication_status,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            studied_specimens=studied_specimens,
            study_targets=study_targets,
            support_channels=support_channels,
            techniques=techniques,
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

    def get_authors(self, client, release_status="released"):
        return self._get_inherited_property("authors", client, release_status)
