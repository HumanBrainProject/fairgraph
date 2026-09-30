"""
Structured information about an association of two or more persons or organizations, with the objective of participating in a common activity.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Consortium as OMConsortium
from fairgraph import KGObject


from openminds import IRI


class Consortium(KGObject, OMConsortium):
    """
    Structured information about an association of two or more persons or organizations, with the objective of participating in a common activity.
    """

    type_ = "https://openminds.om-i.org/types/Consortium"
    default_space = "common"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_member_of",
            "openminds.v5.core.Membership",
            "member",
            reverse="member",
            multiple=True,
            description="reverse of 'member'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("full_name", "memberships")
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        contact_information=None,
        full_name=None,
        homepage=None,
        is_member_of=None,
        memberships=None,
        short_name=None,
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
            name=name,
            alias=alias,
            contact_information=contact_information,
            full_name=full_name,
            homepage=homepage,
            is_member_of=is_member_of,
            memberships=memberships,
            short_name=short_name,
        )
