"""
Structured information on the contribution made to a research product.
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.properties import Property


class Contribution(EmbeddedMetadata):
    """
    Structured information on the contribution made to a research product.
    """

    type_ = "https://openminds.ebrains.eu/core/Contribution"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "contributor",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:contributor",
            required=True,
            doc="Legal person that gave or supplied something as a part or share.",
        ),
        Property(
            "types",
            "openminds.controlled_terms.ContributionType",
            "vocab:type",
            multiple=True,
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
    ]
    reverse_properties = []

    def __init__(self, contributor=None, types=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, contributor=contributor, types=types)
