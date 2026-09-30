"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import AnatomicalAtlasVersion as OMAnatomicalAtlasVersion
from fairgraph import KGObject

from urllib.request import urlretrieve
from pathlib import Path
from fairgraph.utility import accepted_terms_of_use
from datetime import date
from openminds import IRI


class AnatomicalAtlasVersion(KGObject, OMAnatomicalAtlasVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/AnatomicalAtlasVersion"
    default_space = "atlas"
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
            "openminds.v5.sands.AnatomicalAtlasVersion",
            "isVariantOf",
            reverse="is_variant_of",
            multiple=True,
            description="reverse of 'is_variant_of'",
        ),
        Property(
            "is_input_to",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.ProtocolExecution",
            ],
            ["input", "inputData"],
            reverse=["input_data", "inputs"],
            multiple=True,
            description="reverse of input_data, inputs",
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
    existence_query_properties = ("short_name", "version_identifier")
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        abbreviation=None,
        accessibility=None,
        comments=None,
        contributions=None,
        contributor_affiliations=None,
        coordinate_framework=None,
        copyright=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        full_name=None,
        funding=None,
        has_terminology=None,
        has_variants=None,
        homepage=None,
        how_to_cite=None,
        is_input_to=None,
        is_part_of=None,
        is_preceded_by=None,
        is_used_by=None,
        is_variant_of=None,
        is_version_of=None,
        keywords=None,
        learning_resources=None,
        major_version_identifier=None,
        ontology_identifier=None,
        publication_status=None,
        related_publications=None,
        release_date=None,
        repository=None,
        short_name=None,
        support_channels=None,
        type=None,
        usage_conditions=None,
        used_specimens=None,
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
            abbreviation=abbreviation,
            accessibility=accessibility,
            comments=comments,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            coordinate_framework=coordinate_framework,
            copyright=copyright,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            full_name=full_name,
            funding=funding,
            has_terminology=has_terminology,
            has_variants=has_variants,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            is_preceded_by=is_preceded_by,
            is_used_by=is_used_by,
            is_variant_of=is_variant_of,
            is_version_of=is_version_of,
            keywords=keywords,
            learning_resources=learning_resources,
            major_version_identifier=major_version_identifier,
            ontology_identifier=ontology_identifier,
            publication_status=publication_status,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            short_name=short_name,
            support_channels=support_channels,
            type=type,
            usage_conditions=usage_conditions,
            used_specimens=used_specimens,
            version_identifier=version_identifier,
            version_specification=version_specification,
        )
