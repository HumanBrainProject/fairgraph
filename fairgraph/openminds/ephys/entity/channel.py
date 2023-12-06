"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class Channel(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = ["https://openminds.ebrains.eu/ephys/Channel"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            required=True,
            doc="Term or code that identifies the channel within a particular product.",
        ),
        Field(
            "unit",
            "openminds.controlledterms.UnitOfMeasurement",
            "vocab:unit",
            required=True,
            doc="Determinate quantity adopted as a standard of measurement.",
        ),
    ]

    def __init__(self, internal_identifier=None, unit=None, id=None, data=None, space=None, scope=None):
        return super().__init__(data=data, internal_identifier=internal_identifier, unit=unit)
