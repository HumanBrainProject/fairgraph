"""
Structured information on a file repository.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class FileRepository(KGObject):
    """
    Structured information on a file repository.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/FileRepository"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "content_type_patterns",
            "openminds.core.ContentTypePattern",
            "vocab:contentTypePattern",
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
            "hosted_by",
            "openminds.core.Organization",
            "vocab:hostedBy",
            required=True,
            doc="Reference to an organization that provides facilities and services for something.",
        ),
        Property(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the file repository.",
        ),
        Property(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
        Property(
            "structure_pattern",
            "openminds.core.FileRepositoryStructure",
            "vocab:structurePattern",
            doc="no description available",
        ),
        Property(
            "type",
            "openminds.controlled_terms.FileRepositoryType",
            "vocab:type",
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Property(
            "contains_content_of",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:repository",
            reverse="repositories",
            multiple=True,
            doc="reverse of 'repository'",
        ),
        Property(
            "files",
            "openminds.core.File",
            "^vocab:fileRepository",
            reverse="file_repositories",
            multiple=True,
            doc="reverse of 'fileRepository'",
        ),
        Property(
            "has_parts",
            "openminds.core.FileBundle",
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
    ]
    existence_query_properties = ("iri",)

    def __init__(
        self,
        name=None,
        contains_content_of=None,
        content_type_patterns=None,
        files=None,
        format=None,
        has_parts=None,
        hash=None,
        hosted_by=None,
        iri=None,
        storage_size=None,
        structure_pattern=None,
        type=None,
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
            contains_content_of=contains_content_of,
            content_type_patterns=content_type_patterns,
            files=files,
            format=format,
            has_parts=has_parts,
            hash=hash,
            hosted_by=hosted_by,
            iri=iri,
            storage_size=storage_size,
            structure_pattern=structure_pattern,
            type=type,
        )
