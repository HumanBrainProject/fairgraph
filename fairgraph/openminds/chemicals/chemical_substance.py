"""
Structured information about a chemical substance.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ChemicalSubstance(KGObject):
    """
    Structured information about a chemical substance.
    """

    default_space = "in-depth"
    type_ = "https://openminds.ebrains.eu/chemicals/ChemicalSubstance"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "molecular_entity",
            "openminds.controlled_terms.MolecularEntity",
            "vocab:molecularEntity",
            required=True,
            doc="no description available",
        ),
        Property(
            "product_source",
            "openminds.chemicals.ProductSource",
            "vocab:productSource",
            doc="no description available",
        ),
        Property(
            "purity",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:purity",
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
            "composes",
            ["openminds.ephys.Electrode", "openminds.ephys.ElectrodeArray", "openminds.ephys.Pipette"],
            ["^vocab:insulatorMaterial", "^vocab:material"],
            reverse=["insulator_materials", "materials"],
            multiple=True,
            doc="reverse of insulatorMaterial, material",
        ),
        Property(
            "labels",
            "openminds.ephys.PipetteUsage",
            "^vocab:labelingCompound",
            reverse="labeling_compounds",
            multiple=True,
            doc="reverse of 'labelingCompound'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        additional_remarks=None,
        composes=None,
        labels=None,
        molecular_entity=None,
        product_source=None,
        purity=None,
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
            lookup_label=lookup_label,
            additional_remarks=additional_remarks,
            composes=composes,
            labels=labels,
            molecular_entity=molecular_entity,
            product_source=product_source,
            purity=purity,
        )
