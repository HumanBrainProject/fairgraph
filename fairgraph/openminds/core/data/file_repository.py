"""
Structured information on a file repository.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class FileRepository(KGObject):
    """
    Structured information on a file repository.
    """

    default_space = "dataset"
    type_ = ["https://openminds.ebrains.eu/core/FileRepository"]
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
            doc="Word or phrase that constitutes the distinctive designation of the file repository.",
        ),
        Field(
            "content_type_patterns",
            "openminds.core.ContentTypePattern",
            "vocab:contentTypePattern",
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
        Field(
            "hosted_by",
            "openminds.core.Organization",
            "vocab:hostedBy",
            required=True,
            doc="Reference to an organization that provides facilities and services for something.",
        ),
        Field(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Field(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
        Field(
            "structure_pattern",
            "openminds.core.FileRepositoryStructure",
            "vocab:structurePattern",
            doc="no description available",
        ),
        Field(
            "type",
            "openminds.controlledterms.FileRepositoryType",
            "vocab:type",
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Field(
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
        Field(
            "files",
            "openminds.core.File",
            "^vocab:fileRepository",
            reverse="file_repositories",
            multiple=True,
            doc="reverse of 'fileRepository'",
        ),
        Field(
            "has_parts",
            "openminds.core.FileBundle",
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
    ]
    existence_query_fields = ("iri",)

    def __init__(
        self,
        name=None,
        content_type_patterns=None,
        format=None,
        hash=None,
        hosted_by=None,
        iri=None,
        storage_size=None,
        structure_pattern=None,
        type=None,
        contains_content_of=None,
        files=None,
        has_parts=None,
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
            content_type_patterns=content_type_patterns,
            format=format,
            hash=hash,
            hosted_by=hosted_by,
            iri=iri,
            storage_size=storage_size,
            structure_pattern=structure_pattern,
            type=type,
            contains_content_of=contains_content_of,
            files=files,
            has_parts=has_parts,
        )
