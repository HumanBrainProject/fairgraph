"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import StringProperty as OMStringProperty
from fairgraph import KGEmbedded


from openminds import IRI


class StringProperty(KGEmbedded, OMStringProperty):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/StringProperty"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("name", "value")

    def __init__(
        self,
        name=None,
        external_definition_of_name=None,
        value=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self, data=data, name=name, external_definition_of_name=external_definition_of_name, value=value
        )
