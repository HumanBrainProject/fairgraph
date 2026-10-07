"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import WebResource as OMWebResource
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
            ["openminds.v5.core.BehavioralProtocol", "openminds.v5.core.Protocol"],
            "describedIn",
            reverse="described_in",
            multiple=True,
            description="reverse of 'described_in'",
        ),
        Property(
            "documents",
            [
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.Interface",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.Service",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.LivePaper",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.sands.AnatomicalAtlas",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFramework",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "documentation",
            reverse="documentation",
            multiple=True,
            description="reverse of 'documentation'",
        ),
        Property(
            "is_entry_point_of",
            "openminds.v5.computation.DeployedInterface",
            "entryPoint",
            reverse="entry_point",
            multiple=True,
            description="reverse of 'entry_point'",
        ),
        Property(
            "is_input_to",
            "openminds.v5.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
        ),
        Property(
            "is_output_of",
            "openminds.v5.core.ModelVersion",
            "outputData",
            reverse="output_data",
            multiple=True,
            description="reverse of 'output_data'",
        ),
        Property(
            "is_reference_for",
            "openminds.v5.computation.ValidationTestVersion",
            "referenceData",
            reverse="reference_data",
            multiple=True,
            description="reverse of 'reference_data'",
        ),
        Property(
            "is_template_of",
            "openminds.v5.core.UsageAgreement",
            "template",
            reverse="template",
            multiple=True,
            description="reverse of 'template'",
        ),
        Property(
            "is_used_by",
            "openminds.v5.computation.ServiceDeployment",
            "uses",
            reverse="uses",
            multiple=True,
            description="reverse of 'uses'",
        ),
        Property(
            "linked_from",
            "openminds.v5.core.ServiceLink",
            "service",
            reverse="services",
            multiple=True,
            description="reverse of 'services'",
        ),
        Property(
            "specifies",
            "openminds.v5.core.InterfaceVersion",
            "specification",
            reverse="specification",
            multiple=True,
            description="reverse of 'specification'",
        ),
    ]
    existence_query_properties = ("iri",)

    def __init__(
        self,
        content_description=None,
        describes=None,
        documents=None,
        format=None,
        iri=None,
        is_entry_point_of=None,
        is_input_to=None,
        is_output_of=None,
        is_reference_for=None,
        is_template_of=None,
        is_used_by=None,
        linked_from=None,
        specifies=None,
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
            documents=documents,
            format=format,
            iri=iri,
            is_entry_point_of=is_entry_point_of,
            is_input_to=is_input_to,
            is_output_of=is_output_of,
            is_reference_for=is_reference_for,
            is_template_of=is_template_of,
            is_used_by=is_used_by,
            linked_from=linked_from,
            specifies=specifies,
        )
