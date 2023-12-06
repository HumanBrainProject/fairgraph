"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Periodical(KGObject):
    """
    <description not available>
    """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/Periodical"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            doc="Word or phrase that constitutes the distinctive designation of the periodical.",
        ),
        Field("abbreviation", str, "vocab:abbreviation", doc="no description available"),
        Field(
            "digital_identifier",
            "openminds.core.ISSN",
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field(
            "has_parts",
            "openminds.publications.PublicationVolume",
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
    ]
    existence_query_fields = ("abbreviation",)

    def __init__(
        self,
        name=None,
        abbreviation=None,
        digital_identifier=None,
        has_parts=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            abbreviation=abbreviation,
            digital_identifier=digital_identifier,
            has_parts=has_parts,
        )
