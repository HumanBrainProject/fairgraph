"""
Structured information about computing hardware.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class HardwareSystem(KGObject):
    """
    Structured information about computing hardware.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/HardwareSystem"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the hardware system.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the hardware system.",
        ),
        Property(
            "version_identifier",
            str,
            "vocab:versionIdentifier",
            doc="Term or code used to identify the version of something.",
        ),
    ]
    reverse_properties = [
        Property(
            "used_by",
            "openminds.computation.Environment",
            "^vocab:hardware",
            reverse="hardware",
            multiple=True,
            doc="reverse of 'hardware'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        description=None,
        used_by=None,
        version_identifier=None,
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
            used_by=used_by,
            version_identifier=version_identifier,
        )
