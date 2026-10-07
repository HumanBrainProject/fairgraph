"""
A representation of a range of quantitative values.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import QuantitativeValueRange as OMQuantitativeValueRange
from fairgraph import KGEmbedded


from numbers import Real


class QuantitativeValueRange(KGEmbedded, OMQuantitativeValueRange):
    """
    A representation of a range of quantitative values.
    """

    type_ = "https://openminds.om-i.org/types/QuantitativeValueRange"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("max_value", "min_value")

    def __init__(
        self,
        max_value=None,
        max_value_unit=None,
        min_value=None,
        min_value_unit=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            max_value=max_value,
            max_value_unit=max_value_unit,
            min_value=min_value,
            min_value_unit=min_value_unit,
        )
