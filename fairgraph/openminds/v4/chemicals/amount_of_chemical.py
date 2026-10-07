"""
Structured information about the amount of a given chemical that was used.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.chemicals import AmountOfChemical as OMAmountOfChemical
from fairgraph import KGEmbedded


class AmountOfChemical(KGEmbedded, OMAmountOfChemical):
    """
    Structured information about the amount of a given chemical that was used.
    """

    type_ = "https://openminds.om-i.org/types/AmountOfChemical"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("chemical_product", "amount")

    def __init__(self, amount=None, chemical_product=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, amount=amount, chemical_product=chemical_product)
