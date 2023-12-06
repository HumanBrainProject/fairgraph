"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Pipette(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/ephys/Pipette"]
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
            doc="Word or phrase that constitutes the distinctive designation of the pipette.",
        ),
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the pipette.",
        ),
        Field(
            "device_type",
            "openminds.controlledterms.DeviceType",
            "vocab:deviceType",
            required=True,
            doc="no description available",
        ),
        Field(
            "digital_identifier",
            ["openminds.core.DOI", "openminds.core.RRID"],
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field(
            "external_diameter",
            "openminds.core.QuantitativeValue",
            "vocab:externalDiameter",
            doc="no description available",
        ),
        Field(
            "internal_diameter",
            "openminds.core.QuantitativeValue",
            "vocab:internalDiameter",
            doc="no description available",
        ),
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the pipette within a particular product.",
        ),
        Field(
            "manufacturers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:manufacturer",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "material",
            [
                "openminds.chemicals.ChemicalMixture",
                "openminds.chemicals.ChemicalSubstance",
                "openminds.controlledterms.MolecularEntity",
            ],
            "vocab:material",
            doc="no description available",
        ),
        Field(
            "owners",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:owner",
            multiple=True,
            doc="no description available",
        ),
        Field("serial_number", str, "vocab:serialNumber", doc="no description available"),
        Field(
            "is_part_of",
            "openminds.core.Setup",
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Field(
            "usage",
            "openminds.ephys.PipetteUsage",
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        name=None,
        lookup_label=None,
        description=None,
        device_type=None,
        digital_identifier=None,
        external_diameter=None,
        internal_diameter=None,
        internal_identifier=None,
        manufacturers=None,
        material=None,
        owners=None,
        serial_number=None,
        is_part_of=None,
        usage=None,
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
            lookup_label=lookup_label,
            description=description,
            device_type=device_type,
            digital_identifier=digital_identifier,
            external_diameter=external_diameter,
            internal_diameter=internal_diameter,
            internal_identifier=internal_identifier,
            manufacturers=manufacturers,
            material=material,
            owners=owners,
            serial_number=serial_number,
            is_part_of=is_part_of,
            usage=usage,
        )
