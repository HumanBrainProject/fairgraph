"""
Structured information about a user account for a web service.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import AccountInformation as OMAccountInformation
from fairgraph import KGObject


class AccountInformation(KGObject, OMAccountInformation):
    """
    Structured information about a user account for a web service.
    """

    type_ = "https://openminds.om-i.org/types/AccountInformation"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "belongs_to",
            "openminds.v4.core.Person",
            "associatedAccount",
            reverse="associated_accounts",
            multiple=True,
            description="reverse of 'associated_accounts'",
        ),
    ]
    existence_query_properties = ("service", "user_name")

    def __init__(
        self, belongs_to=None, service=None, user_name=None, id=None, data=None, space=None, release_status=None
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            belongs_to=belongs_to,
            service=service,
            user_name=user_name,
        )
