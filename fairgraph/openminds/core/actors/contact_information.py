"""
Structured information about how to contact a given person or consortium.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class ContactInformation(KGObject):
    """
    Structured information about how to contact a given person or consortium.
    """

    default_space = "restricted"
    type_ = ["https://openminds.ebrains.eu/core/ContactInformation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "email",
            str,
            "vocab:email",
            required=True,
            doc="Address to which or from which an electronic mail can be sent.",
        ),
        Field(
            "is_contact_information_of",
            ["openminds.core.Consortium", "openminds.core.Person"],
            "^vocab:contactInformation",
            reverse="contact_information",
            multiple=True,
            doc="reverse of 'contactInformation'",
        ),
    ]
    existence_query_fields = ("email",)

    def __init__(self, email=None, is_contact_information_of=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            email=email,
            is_contact_information_of=is_contact_information_of,
        )
