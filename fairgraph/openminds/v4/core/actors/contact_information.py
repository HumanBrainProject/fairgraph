"""
Structured information about how to contact a given person or consortium.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ContactInformation as OMContactInformation
from fairgraph import KGObject


class ContactInformation(KGObject, OMContactInformation):
    """
    Structured information about how to contact a given person or consortium.
    """

    type_ = "https://openminds.om-i.org/types/ContactInformation"
    default_space = "restricted"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_contact_information_of",
            ["openminds.v4.core.Consortium", "openminds.v4.core.Person"],
            "contactInformation",
            reverse="contact_information",
            multiple=True,
            description="reverse of 'contact_information'",
        ),
    ]
    existence_query_properties = ("email",)

    def __init__(
        self, email=None, is_contact_information_of=None, id=None, data=None, space=None, release_status=None
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            email=email,
            is_contact_information_of=is_contact_information_of,
        )
