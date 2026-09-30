"""
Structured information on the content type of a file instance, bundle or repository.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ContentType as OMContentType
from fairgraph import KGObject


from openminds import IRI


class ContentType(KGObject, OMContentType):
    """
    Structured information on the content type of a file instance, bundle or repository.
    """

    type_ = "https://openminds.om-i.org/types/ContentType"
    default_space = "controlled"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_defined_by",
            "openminds.v4.core.ContentTypePattern",
            "contentType",
            reverse="content_type",
            multiple=True,
            description="reverse of 'content_type'",
        ),
        Property(
            "is_format_of",
            [
                "openminds.v4.computation.LocalFile",
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.Configuration",
                "openminds.v4.core.File",
                "openminds.v4.core.FileArchive",
                "openminds.v4.core.FileBundle",
                "openminds.v4.core.FileRepository",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.WebResource",
            ],
            "format",
            reverse="format",
            multiple=True,
            description="reverse of 'format'",
        ),
        Property(
            "is_output_format_of",
            ["openminds.v4.core.SoftwareVersion", "openminds.v4.core.WebServiceVersion"],
            "outputFormat",
            reverse="output_formats",
            multiple=True,
            description="reverse of 'output_formats'",
        ),
        Property(
            "is_specification_format_of",
            "openminds.v4.core.MetaDataModelVersion",
            "specificationFormat",
            reverse="specification_formats",
            multiple=True,
            description="reverse of 'specification_formats'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        data_types=None,
        description=None,
        display_label=None,
        file_extensions=None,
        is_defined_by=None,
        is_format_of=None,
        is_output_format_of=None,
        is_specification_format_of=None,
        related_media_type=None,
        specification=None,
        synonyms=None,
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
            data_types=data_types,
            description=description,
            display_label=display_label,
            file_extensions=file_extensions,
            is_defined_by=is_defined_by,
            is_format_of=is_format_of,
            is_output_format_of=is_output_format_of,
            is_specification_format_of=is_specification_format_of,
            related_media_type=related_media_type,
            specification=specification,
            synonyms=synonyms,
        )
