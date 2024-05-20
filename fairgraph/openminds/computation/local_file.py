"""
Structured information about a file that is not accessible via a URL.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class LocalFile(KGObject):
    """
    Structured information about a file that is not accessible via a URL.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/LocalFile"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("content_description", str, "vocab:contentDescription", doc="no description available"),
        Property("copy_of", "openminds.core.File", "vocab:copyOf", doc="no description available"),
        Property(
            "data_types",
            "openminds.controlled_terms.DataType",
            "vocab:dataType",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Property(
            "hash",
            "openminds.core.Hash",
            "vocab:hash",
            doc="Term used for the process of converting any data into a single value. Often also directly refers to the resulting single value.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the local file.",
        ),
        Property("path", str, "vocab:path", required=True, doc="no description available"),
        Property(
            "special_usage_role",
            "openminds.controlled_terms.FileUsageRole",
            "vocab:specialUsageRole",
            doc="Particular function of something when it is used.",
        ),
        Property(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
        Property(
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
        Property(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
    ]
    existence_query_properties = ("name", "path")

    def __init__(
        self,
        name=None,
        content_description=None,
        copy_of=None,
        data_types=None,
        format=None,
        hash=None,
        is_output_of=None,
        is_used_to_group=None,
        path=None,
        special_usage_role=None,
        storage_size=None,
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
            is_output_of=is_output_of,
            is_used_to_group=is_used_to_group,
            path=path,
            special_usage_role=special_usage_role,
            storage_size=storage_size,
        )
