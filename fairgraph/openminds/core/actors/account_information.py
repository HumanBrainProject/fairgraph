"""
Structured information about a user account for a web service.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class AccountInformation(KGObject):
    """
    Structured information about a user account for a web service.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/AccountInformation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("service", "openminds.core.WebService", "vocab:service", required=True, doc="no description available"),
        Field("user_name", str, "vocab:userName", required=True, doc="no description available"),
        Field(
            "belongs_to",
            "openminds.core.Person",
            "^vocab:associatedAccount",
            reverse="associated_accounts",
            multiple=True,
            doc="reverse of 'associatedAccount'",
        ),
    ]
    existence_query_fields = ("service", "user_name")

    def __init__(self, service=None, user_name=None, belongs_to=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id, space=space, scope=scope, data=data, service=service, user_name=user_name, belongs_to=belongs_to
        )
