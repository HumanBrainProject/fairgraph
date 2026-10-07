"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Accessibility as OMAccessibility
from fairgraph import KGObject


class Accessibility(KGObject, OMAccessibility):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Accessibility"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_accessibility_of",
            [
                "openminds.v5.computation.DeployedInterface",
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "accessibility",
            reverse="accessibility",
            multiple=True,
            description="reverse of 'accessibility'",
        ),
    ]
    existence_query_properties = ("channel", "eligibility", "form", "payment_models", "process")

    def __init__(
        self,
        application=None,
        channel=None,
        eligibility=None,
        form=None,
        is_accessibility_of=None,
        payment_models=None,
        process=None,
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
            application=application,
            channel=channel,
            eligibility=eligibility,
            form=form,
            is_accessibility_of=is_accessibility_of,
            payment_models=payment_models,
            process=process,
        )
