"""
Structured information on the copyright.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class Copyright(EmbeddedMetadata):
    """
    Structured information on the copyright.
    """

    type_ = "https://openminds.ebrains.eu/core/Copyright"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "holders",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:holder",
            multiple=True,
            required=True,
            doc="Legal person in possession of something.",
        ),
        Property(
            "years",
            str,
            "vocab:year",
            multiple=True,
            required=True,
            doc="Cycle in the Gregorian calendar specified by a number and comprised of 365 or 366 days divided into 12 months beginning with January and ending with December.",
        ),
    ]

    def __init__(self, holders=None, years=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, holders=holders, years=years)
