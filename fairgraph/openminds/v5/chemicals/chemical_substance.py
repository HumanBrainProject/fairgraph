"""
Structured information about a chemical substance.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.chemicals import ChemicalSubstance as OMChemicalSubstance
from fairgraph import KGObject


class ChemicalSubstance(KGObject, OMChemicalSubstance):
    """
    Structured information about a chemical substance.
    """

    type_ = "https://openminds.om-i.org/types/ChemicalSubstance"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "composes",
            ["openminds.v5.ephys.Electrode", "openminds.v5.ephys.ElectrodeArray", "openminds.v5.ephys.Pipette"],
            ["insulatorMaterial", "material"],
            reverse=["insulator_material", "material"],
            multiple=True,
            description="reverse of insulator_material, material",
        ),
        Property(
            "labels",
            "openminds.v5.ephys.PipetteUsage",
            "labelingCompound",
            reverse="labeling_compound",
            multiple=True,
            description="reverse of 'labeling_compound'",
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            lookup_label=lookup_label,
            additional_remarks=additional_remarks,
            composes=composes,
            labels=labels,
            molecular_entity=molecular_entity,
            product_source=product_source,
            purity=purity,
        )
