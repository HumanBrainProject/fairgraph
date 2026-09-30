"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.ephys import Channel as OMChannel
from fairgraph import KGEmbedded


class Channel(KGEmbedded, OMChannel):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Channel"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("internal_identifier", "unit")

    def __init__(self, internal_identifier=None, unit=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, internal_identifier=internal_identifier, unit=unit)
