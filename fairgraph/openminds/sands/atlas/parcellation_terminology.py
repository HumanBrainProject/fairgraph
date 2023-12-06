"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class ParcellationTerminology(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = ["https://openminds.ebrains.eu/sands/ParcellationTerminology"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "data_locations",
            "openminds.core.File",
            "vocab:dataLocation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "has_entities",
            "openminds.sands.ParcellationEntity",
            "vocab:hasEntity",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Field(
            "ontology_identifiers",
            str,
            "vocab:ontologyIdentifier",
            multiple=True,
            doc="Term or code used to identify the parcellation terminology registered within a particular ontology.",
        ),
    ]

    def __init__(
        self,
        data_locations=None,
        has_entities=None,
        ontology_identifiers=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            data_locations=data_locations,
            has_entities=has_entities,
            ontology_identifiers=ontology_identifiers,
        )
