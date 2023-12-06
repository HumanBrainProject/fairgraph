"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class LivePaperResourceItem(KGObject):
    """
    <description not available>
    """

    default_space = "livepapers"
    type_ = ["https://openminds.ebrains.eu/publications/LivePaperResourceItem"]
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
            doc="Word or phrase that constitutes the distinctive designation of the live paper resource item.",
        ),
        Field(
            "hosted_by",
            ["openminds.core.Organization", "openminds.core.WebService", "openminds.controlledterms.Service"],
            "vocab:hostedBy",
            required=True,
            doc="Reference to an organization that provides facilities and services for something.",
        ),
        Field(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Field(
            "is_part_of",
            "openminds.publications.LivePaperSection",
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Field(
            "is_location_of",
            "openminds.core.ServiceLink",
            "^vocab:dataLocation",
            reverse="data_locations",
            multiple=True,
            doc="reverse of 'dataLocation'",
        ),
    ]
    existence_query_fields = ("name", "iri", "is_also_part_of")

    def __init__(
        self,
        name=None,
        hosted_by=None,
        iri=None,
        is_part_of=None,
        is_location_of=None,
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
            hosted_by=hosted_by,
            iri=iri,
            is_part_of=is_part_of,
            is_location_of=is_location_of,
        )
