"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class ServiceLink(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/ServiceLink"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "data_location",
            [
                "openminds.core.File",
                "openminds.core.FileArchive",
                "openminds.core.FileBundle",
                "openminds.core.ModelVersion",
                "openminds.publications.LivePaperResourceItem",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:dataLocation",
            required=True,
            doc="no description available",
        ),
        Property("display_label", str, "vocab:displayLabel", doc="no description available"),
        Property("open_data_in", IRI, "vocab:openDataIn", required=True, doc="no description available"),
        Property("preview_image", "openminds.core.File", "vocab:previewImage", doc="no description available"),
        Property(
            "service",
            "openminds.controlled_terms.Service",
            "vocab:service",
            required=True,
            doc="no description available",
        ),
    ]
    existence_query_properties = ("data_location", "open_data_in", "service")

    def __init__(
        self,
        data_location=None,
        display_label=None,
        open_data_in=None,
        preview_image=None,
        service=None,
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
            data_location=data_location,
            display_label=display_label,
            open_data_in=open_data_in,
            preview_image=preview_image,
            service=service,
        )
