"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import BrainAtlas as OMBrainAtlas
from fairgraph import KGObject


from openminds import IRI


class BrainAtlas(KGObject, OMBrainAtlas):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/BrainAtlas"
    default_space = "atlas"
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
            "openminds.v4.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
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
            "learning_resources",
            "openminds.v4.publications.LearningResource",
            "about",
            reverse="about",
            multiple=True,
            description="reverse of 'about'",
        ),
    ]
    aliases = {"name": "full_name", "versions": "has_versions", "alias": "short_name"}
    existence_query_properties = ("digital_identifier",)
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        abbreviation=None,
        authors=None,
        comments=None,
        custodians=None,
        description=None,
        digital_identifier=None,
        full_name=None,
        has_terminology=None,
        has_versions=None,
        homepage=None,
        how_to_cite=None,
        is_input_to=None,
        is_part_of=None,
        learning_resources=None,
        ontology_identifier=None,
        short_name=None,
        used_species=None,
        versions=None,
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
            authors=authors,
            comments=comments,
            custodians=custodians,
            description=description,
            digital_identifier=digital_identifier,
            full_name=full_name,
            has_terminology=has_terminology,
            has_versions=has_versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_input_to=is_input_to,
            is_part_of=is_part_of,
            learning_resources=learning_resources,
            ontology_identifier=ontology_identifier,
            short_name=short_name,
            used_species=used_species,
            versions=versions,
        )
