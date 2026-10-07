"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Membership as OMMembership
from fairgraph import KGEmbedded


from datetime import date


class Membership(KGEmbedded, OMMembership):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Membership"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("member",)

    def __init__(
        self, end_date=None, member=None, start_date=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(self, data=data, end_date=end_date, member=member, start_date=start_date)
