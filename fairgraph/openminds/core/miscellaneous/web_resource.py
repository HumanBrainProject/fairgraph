"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class WebResource(KGObject):
    """
    <description not available>
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/WebResource"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("content_description", str, "vocab:contentDescription", doc="no description available"),
        Field(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Field(
            "iri",
            IRI,
            "vocab:IRI",
            required=True,
            doc="Stands for Internationalized Resource Identifier which is an internet protocol standard that builds on the URI protocol, extending the set of permitted characters to include Unicode/ISO 10646.",
        ),
        Field(
            "describes",
            ["openminds.core.BehavioralProtocol", "openminds.core.Protocol"],
            "^vocab:describedIn",
            reverse="described_in",
            multiple=True,
            doc="reverse of 'describedIn'",
        ),
        Field(
            "fully_documents",
            [
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.LivePaperVersion",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:fullDocumentation",
            reverse="full_documentations",
            multiple=True,
            doc="reverse of 'fullDocumentation'",
        ),
        Field(
            "is_applied_to",
            "openminds.core.DatasetVersion",
            "^vocab:license",
            reverse="licenses",
            multiple=True,
            doc="reverse of 'license'",
        ),
        Field(
            "is_output_of",
            "openminds.core.ModelVersion",
            "^vocab:outputData",
            reverse="output_data",
            multiple=True,
            doc="reverse of 'outputData'",
        ),
        Field(
            "is_reference_for",
            "openminds.computation.ValidationTestVersion",
            "^vocab:referenceData",
            reverse="reference_data",
            multiple=True,
            doc="reverse of 'referenceData'",
        ),
    ]
    existence_query_fields = ("iri",)

    def __init__(
        self,
        content_description=None,
        format=None,
        iri=None,
        describes=None,
        fully_documents=None,
        is_applied_to=None,
        is_output_of=None,
        is_reference_for=None,
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
            content_description=content_description,
            format=format,
            iri=iri,
            describes=describes,
            fully_documents=fully_documents,
            is_applied_to=is_applied_to,
            is_output_of=is_output_of,
            is_reference_for=is_reference_for,
        )
