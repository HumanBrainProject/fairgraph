"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import WebResource as OMWebResource
from fairgraph import KGObject


from openminds import IRI


class WebResource(KGObject, OMWebResource):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/WebResource"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            ["openminds.v4.core.BehavioralProtocol", "openminds.v4.core.Protocol"],
            "describedIn",
            reverse="described_in",
            multiple=True,
            description="reverse of 'described_in'",
        ),
        Property(
            "fully_documents",
            [
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "fullDocumentation",
            reverse="full_documentation",
            multiple=True,
            description="reverse of 'full_documentation'",
        ),
        Property(
            "is_applied_to",
            "openminds.v4.core.DatasetVersion",
            "license",
            reverse="license",
            multiple=True,
            description="reverse of 'license'",
        ),
        Property(
            "is_output_of",
            "openminds.v4.core.ModelVersion",
            "outputData",
            reverse="output_data",
            multiple=True,
            description="reverse of 'output_data'",
        ),
        Property(
            "is_reference_for",
            "openminds.v4.computation.ValidationTestVersion",
            "referenceData",
            reverse="reference_data",
            multiple=True,
            description="reverse of 'reference_data'",
        ),
    ]
    existence_query_properties = ("iri",)

    def __init__(
        self,
        content_description=None,
        describes=None,
        format=None,
        fully_documents=None,
        iri=None,
        is_applied_to=None,
        is_output_of=None,
        is_reference_for=None,
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
            content_description=content_description,
            describes=describes,
            format=format,
            fully_documents=fully_documents,
            iri=iri,
            is_applied_to=is_applied_to,
            is_output_of=is_output_of,
            is_reference_for=is_reference_for,
        )
