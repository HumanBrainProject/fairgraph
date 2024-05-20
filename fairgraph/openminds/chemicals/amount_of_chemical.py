"""
Structured information about the amount of a given chemical that was used.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class AmountOfChemical(EmbeddedMetadata):
    """
    Structured information about the amount of a given chemical that was used.
    """

    type_ = "https://openminds.ebrains.eu/chemicals/AmountOfChemical"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("amount", "openminds.core.QuantitativeValue", "vocab:amount", doc="no description available"),
        Property(
            "chemical_product",
            [
                "openminds.chemicals.ChemicalMixture",
                "openminds.chemicals.ChemicalSubstance",
                "openminds.controlled_terms.MolecularEntity",
            ],
            "vocab:chemicalProduct",
            required=True,
            doc="no description available",
        ),
    ]

    def __init__(self, amount=None, chemical_product=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, amount=amount, chemical_product=chemical_product)
