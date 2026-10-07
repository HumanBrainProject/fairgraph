"""
Structured information about a property of some entity or process whose value is a number.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import NumericalProperty as OMNumericalProperty
from fairgraph import KGEmbedded


class NumericalProperty(KGEmbedded, OMNumericalProperty):
    """
    Structured information about a property of some entity or process whose value is a number.
    """

    type_ = "https://openminds.om-i.org/types/NumericalProperty"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("name", "values")

    def __init__(self, name=None, values=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, name=name, values=values)
