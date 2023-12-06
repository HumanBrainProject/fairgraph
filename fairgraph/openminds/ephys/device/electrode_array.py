"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class ElectrodeArray(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/ephys/ElectrodeArray"]
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
            doc="Word or phrase that constitutes the distinctive designation of the electrode array.",
        ),
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "conductor_material",
            [
                "openminds.chemicals.ChemicalMixture",
                "openminds.chemicals.ChemicalSubstance",
                "openminds.controlledterms.MolecularEntity",
            ],
            "vocab:conductorMaterial",
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the electrode array.",
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
            "electrode_identifiers",
            str,
            "vocab:electrodeIdentifier",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Field(
            "insulator_material",
            [
                "openminds.chemicals.ChemicalMixture",
                "openminds.chemicals.ChemicalSubstance",
                "openminds.controlledterms.MolecularEntity",
            ],
            "vocab:insulatorMaterial",
            doc="no description available",
        ),
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the electrode array within a particular product.",
        ),
        Field(
            "intrinsic_resistance",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:intrinsicResistance",
            doc="no description available",
        ),
        Field(
            "manufacturers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:manufacturer",
            multiple=True,
            doc="no description available",
        ),
        Field("number_of_electrodes", int, "vocab:numberOfElectrodes", required=True, doc="no description available"),
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
            "openminds.ephys.ElectrodeArrayUsage",
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
        conductor_material=None,
        description=None,
        device_type=None,
        digital_identifier=None,
        electrode_identifiers=None,
        insulator_material=None,
        internal_identifier=None,
        intrinsic_resistance=None,
        manufacturers=None,
        number_of_electrodes=None,
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
            conductor_material=conductor_material,
            description=description,
            device_type=device_type,
            digital_identifier=digital_identifier,
            electrode_identifiers=electrode_identifiers,
            insulator_material=insulator_material,
            internal_identifier=internal_identifier,
            intrinsic_resistance=intrinsic_resistance,
            manufacturers=manufacturers,
            number_of_electrodes=number_of_electrodes,
            owners=owners,
            serial_number=serial_number,
            is_part_of=is_part_of,
            usage=usage,
        )
