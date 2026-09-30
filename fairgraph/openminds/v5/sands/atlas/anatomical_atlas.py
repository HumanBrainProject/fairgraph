"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import AnatomicalAtlas as OMAnatomicalAtlas
from fairgraph import KGObject


from openminds import IRI


class AnatomicalAtlas(KGObject, OMAnatomicalAtlas):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/AnatomicalAtlas"
    default_space = "atlas"
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
            "openminds.v5.sands.AnatomicalAtlasVersion",
            "isVersionOf",
            reverse="is_version_of",
            multiple=True,
            description="reverse of 'is_version_of'",
        ),
        Property(
            "is_input_to",
            "openminds.v5.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
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
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("digital_identifier",)

    def __init__(
        self,
        name=None,
        alias=None,
        abbreviation=None,
        comments=None,
        contributions=None,
        contributor_affiliations=None,
        description=None,
        digital_identifier=None,
        documentation=None,
        full_name=None,
        has_terminology=None,
        has_versions=None,
        homepage=None,
        how_to_cite=None,
        is_input_to=None,
        is_part_of=None,
        keywords=None,
        learning_resources=None,
        ontology_identifier=None,
        related_publications=None,
        short_name=None,
        support_channels=None,
        used_taxon=None,
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
            comments=comments,
            contributions=contributions,
            contributor_affiliations=contributor_affiliations,
            description=description,
            digital_identifier=digital_identifier,
            documentation=documentation,
            full_name=full_name,
            has_terminology=has_terminology,
            has_versions=has_versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            keywords=keywords,
            learning_resources=learning_resources,
            ontology_identifier=ontology_identifier,
            related_publications=related_publications,
            short_name=short_name,
            support_channels=support_channels,
            used_taxon=used_taxon,
        )
