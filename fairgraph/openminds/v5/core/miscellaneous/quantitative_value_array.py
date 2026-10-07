"""
A representation of an array of quantitative values, optionally with uncertainties.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import QuantitativeValueArray as OMQuantitativeValueArray
from fairgraph import KGEmbedded


from numbers import Real


class QuantitativeValueArray(KGEmbedded, OMQuantitativeValueArray):
    """
    A representation of an array of quantitative values, optionally with uncertainties.
    """

    type_ = "https://openminds.om-i.org/types/QuantitativeValueArray"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("values",)

    def __init__(
        self,
        negative_uncertainties=None,
        positive_uncertainties=None,
        type_of_uncertainty=None,
        unit=None,
        values=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            negative_uncertainties=negative_uncertainties,
            positive_uncertainties=positive_uncertainties,
            type_of_uncertainty=type_of_uncertainty,
            unit=unit,
            values=values,
        )
