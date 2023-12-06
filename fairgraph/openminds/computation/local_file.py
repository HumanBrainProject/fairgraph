"""
Structured information about a file that is not accessible via a URL.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class LocalFile(KGObject):
    """
    Structured information about a file that is not accessible via a URL.
    """

    default_space = "computation"
    type_ = ["https://openminds.ebrains.eu/computation/LocalFile"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the local file.",
        ),
        Field("content_description", str, "vocab:contentDescription", doc="no description available"),
        Field("copy_of", "openminds.core.File", "vocab:copyOf", doc="no description available"),
        Field(
            "data_types",
            "openminds.controlledterms.DataType",
            "vocab:dataType",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Field(
            "hash",
            "openminds.core.Hash",
            "vocab:hash",
            doc="Term used for the process of converting any data into a single value. Often also directly refers to the resulting single value.",
        ),
        Field("path", str, "vocab:path", required=True, doc="no description available"),
        Field(
            "special_usage_role",
            "openminds.controlledterms.FileUsageRole",
            "vocab:specialUsageRole",
            doc="Particular function of something when it is used.",
        ),
        Field(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
        Field(
            "is_output_of",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "^vocab:output",
            reverse="outputs",
            multiple=True,
            doc="reverse of 'output'",
        ),
        Field(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
    ]
    existence_query_fields = ("name", "path")

    def __init__(
        self,
        name=None,
        content_description=None,
        copy_of=None,
        data_types=None,
        format=None,
        hash=None,
        path=None,
        special_usage_role=None,
        storage_size=None,
        is_output_of=None,
        is_used_to_group=None,
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
            name=name,
            content_description=content_description,
            copy_of=copy_of,
            data_types=data_types,
            format=format,
            hash=hash,
            path=path,
            special_usage_role=special_usage_role,
            storage_size=storage_size,
            is_output_of=is_output_of,
            is_used_to_group=is_used_to_group,
        )
