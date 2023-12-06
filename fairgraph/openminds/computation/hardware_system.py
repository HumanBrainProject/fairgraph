"""
Structured information about computing hardware.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class HardwareSystem(KGObject):
    """
    Structured information about computing hardware.
    """

    default_space = "computation"
    type_ = ["https://openminds.ebrains.eu/computation/HardwareSystem"]
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
            doc="Word or phrase that constitutes the distinctive designation of the hardware system.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the hardware system.",
        ),
        Field(
            "version_identifier",
            str,
            "vocab:versionIdentifier",
            doc="Term or code used to identify the version of something.",
        ),
        Field(
            "used_by",
            "openminds.computation.Environment",
            "^vocab:hardware",
            reverse="hardware",
            multiple=True,
            doc="reverse of 'hardware'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        description=None,
        version_identifier=None,
        used_by=None,
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
            version_identifier=version_identifier,
            used_by=used_by,
        )
