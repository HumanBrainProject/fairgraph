"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class LivePaperSection(KGObject):
    """
    <description not available>
    """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/LivePaperSection"]
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
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the live paper section.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the live paper section.",
        ),
        Field(
            "is_part_of",
            "openminds.publications.LivePaperVersion",
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Field("order", int, "vocab:order", required=True, doc="no description available"),
        Field(
            "type",
            str,
            "vocab:type",
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Field(
            "has_parts",
            "openminds.publications.LivePaperResourceItem",
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
    ]
    existence_query_fields = ("is_part_of", "name", "order", "type")

    def __init__(
        self,
        name=None,
        description=None,
        is_part_of=None,
        order=None,
        type=None,
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
            description=description,
            is_part_of=is_part_of,
            order=order,
            type=type,
            has_parts=has_parts,
        )
