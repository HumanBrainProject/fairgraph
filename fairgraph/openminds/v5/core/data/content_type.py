"""
Structured information on the content type of a file instance, bundle or repository.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import ContentType as OMContentType
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
            "has_derived",
            "openminds.v5.core.ContentType",
            "isBasedOn",
            reverse="is_based_on",
            multiple=True,
            description="reverse of 'is_based_on'",
        ),
        Property(
            "is_defined_by",
            "openminds.v5.core.ContentTypePattern",
            "contentType",
            reverse="content_type",
            multiple=True,
            description="reverse of 'content_type'",
        ),
        Property(
            "is_format_of",
            [
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Configuration",
                "openminds.v5.core.File",
                "openminds.v5.core.FileArchive",
                "openminds.v5.core.FileBundle",
                "openminds.v5.core.FileRepository",
                "openminds.v5.core.LocalFile",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.WebResource",
            ],
            "format",
            reverse="format",
            multiple=True,
            description="reverse of 'format'",
        ),
        Property(
            "is_output_format_of",
            "openminds.v5.core.SoftwareVersion",
            "outputFormat",
            reverse="output_formats",
            multiple=True,
            description="reverse of 'output_formats'",
        ),
        Property(
            "is_specification_format_of",
            "openminds.v5.core.MetaDataModelVersion",
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
        defining_sources=None,
        description=None,
        display_label=None,
        file_extensions=None,
        has_derived=None,
        is_based_on=None,
        is_defined_by=None,
        is_format_of=None,
        is_output_format_of=None,
        is_specification_format_of=None,
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
            defining_sources=defining_sources,
            description=description,
            display_label=display_label,
            file_extensions=file_extensions,
            has_derived=has_derived,
            is_based_on=is_based_on,
            is_defined_by=is_defined_by,
            is_format_of=is_format_of,
            is_output_format_of=is_output_format_of,
            is_specification_format_of=is_specification_format_of,
            specification=specification,
            synonyms=synonyms,
        )
