"""
Structured information about properties of an entity that are not represented in an openMINDS schema.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import CustomPropertySet as OMCustomPropertySet
from fairgraph import KGEmbedded


class CustomPropertySet(KGEmbedded, OMCustomPropertySet):
    """
    Structured information about properties of an entity that are not represented in an openMINDS schema.
    """

    type_ = "https://openminds.om-i.org/types/CustomPropertySet"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("context", "data_location", "relevant_for")

    def __init__(
        self, context=None, data_location=None, relevant_for=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, context=context, data_location=data_location, relevant_for=relevant_for
        )
