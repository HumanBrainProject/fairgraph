"""
Structured information on the content type of a file instance, bundle or repository.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class ContentType(KGObject):
    """
    Structured information on the content type of a file instance, bundle or repository.
    """

    default_space = "controlled"
    type_ = "https://openminds.ebrains.eu/core/ContentType"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "data_types",
            "openminds.controlled_terms.DataType",
            "vocab:dataType",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the content type.",
        ),
        Property("display_label", str, "vocab:displayLabel", doc="no description available"),
        Property(
            "file_extensions",
            str,
            "vocab:fileExtension",
            multiple=True,
            doc="String of characters attached as suffix to the names of files of a particular format.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the content type.",
        ),
        Property(
            "related_media_type",
            IRI,
            "vocab:relatedMediaType",
            doc="Reference to an official two-part identifier for file formats and format contents.",
        ),
        Property(
            "specification",
            IRI,
            "vocab:specification",
            doc="Detailed and precise presentation of, or proposal for something.",
        ),
        Property(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
        Property(
            "is_defined_by",
            "openminds.core.ContentTypePattern",
            "^vocab:contentType",
            reverse="content_types",
            multiple=True,
            doc="reverse of 'contentType'",
        ),
        Property(
            "is_format_of",
            [
                "openminds.computation.LocalFile",
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.Configuration",
                "openminds.core.File",
                "openminds.core.FileArchive",
                "openminds.core.FileBundle",
                "openminds.core.FileRepository",
                "openminds.core.ModelVersion",
                "openminds.core.WebResource",
            ],
            "^vocab:format",
            reverse="formats",
            multiple=True,
            doc="reverse of 'format'",
        ),
        Property(
            "is_output_format_of",
            ["openminds.core.SoftwareVersion", "openminds.core.WebServiceVersion"],
            "^vocab:outputFormat",
            reverse="output_formats",
            multiple=True,
            doc="reverse of 'outputFormat'",
        ),
        Property(
            "is_specification_format_of",
            "openminds.core.MetaDataModelVersion",
            "^vocab:specificationFormat",
            reverse="specification_formats",
            multiple=True,
            doc="reverse of 'specificationFormat'",
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
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
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
