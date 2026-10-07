"""
Structured information on a file repository.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import FileRepository as OMFileRepository
from fairgraph import KGObject


from openminds import IRI


class FileRepository(KGObject, OMFileRepository):
    """
    Structured information on a file repository.
    """

    type_ = "https://openminds.om-i.org/types/FileRepository"
    default_space = "dataset"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "contains_content_of",
            [
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "repository",
            reverse="repository",
            multiple=True,
            description="reverse of 'repository'",
        ),
        Property(
            "files",
            "openminds.v4.core.File",
            "fileRepository",
            reverse="file_repository",
            multiple=True,
            description="reverse of 'file_repository'",
        ),
        Property(
            "has_parts",
            "openminds.v4.core.FileBundle",
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
    ]
    existence_query_properties = ("iri",)
    sort_property = "name"

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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
