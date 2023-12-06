"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class FileArchive(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/FileArchive"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            required=True,
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Field(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Field("source_data", "openminds.core.File", "vocab:sourceData", multiple=True, doc="no description available"),
        Field(
            "is_location_of",
            "openminds.core.ServiceLink",
            "^vocab:dataLocation",
            reverse="data_locations",
            multiple=True,
            doc="reverse of 'dataLocation'",
        ),
        Field(
            "is_output_of",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.GenericComputation",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "^vocab:output",
            reverse="outputs",
            multiple=True,
            doc="reverse of 'output'",
        ),
    ]
    existence_query_fields = ("iri", "format")

    def __init__(
        self,
        format=None,
        iri=None,
        source_data=None,
        is_location_of=None,
        is_output_of=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            format=format,
            iri=iri,
            source_data=source_data,
            is_location_of=is_location_of,
            is_output_of=is_output_of,
        )
