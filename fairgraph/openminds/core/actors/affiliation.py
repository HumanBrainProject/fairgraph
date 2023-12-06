"""
Structured information about a relationship between two entities, such as a person and their employer.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


from datetime import date


class Affiliation(EmbeddedMetadata):
    """
    Structured information about a relationship between two entities, such as a person and their employer.
    """

    type_ = ["https://openminds.ebrains.eu/core/Affiliation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "end_date",
            date,
            "vocab:endDate",
            doc="Date in the Gregorian calendar at which something terminates in time.",
        ),
        Field(
            "member_of",
            ["openminds.core.Consortium", "openminds.core.Organization"],
            "vocab:memberOf",
            required=True,
            doc="no description available",
        ),
        Field(
            "start_date",
            date,
            "vocab:startDate",
            doc="Date in the Gregorian calendar at which something begins in time",
        ),
    ]

    def __init__(self, end_date=None, member_of=None, start_date=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, end_date=end_date, member_of=member_of, start_date=start_date)
