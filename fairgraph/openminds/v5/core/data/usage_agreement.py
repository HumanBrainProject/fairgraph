"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import UsageAgreement as OMUsageAgreement
from fairgraph import KGObject


class UsageAgreement(KGObject, OMUsageAgreement):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/UsageAgreement"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "applies_to",
            [
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.HardwareProduct",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.Book",
                "openminds.v5.publications.Chapter",
                "openminds.v5.publications.LearningResource",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.publications.ScholarlyArticle",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "usageCondition",
            reverse="usage_conditions",
            multiple=True,
            description="reverse of 'usage_conditions'",
        ),
        Property(
            "is_source_of",
            "openminds.v5.core.UsageAgreement",
            "source",
            reverse="sources",
            multiple=True,
            description="reverse of 'sources'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = (
        "authoring_parties",
        "full_name",
        "jurisdiction",
        "modification_profiles",
        "short_name",
        "template",
    )

    def __init__(
        self,
        name=None,
        alias=None,
        applies_to=None,
        authoring_parties=None,
        full_name=None,
        is_source_of=None,
        jurisdiction=None,
        modification_profiles=None,
        short_name=None,
        sources=None,
        support_channels=None,
        template=None,
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
            alias=alias,
            applies_to=applies_to,
            authoring_parties=authoring_parties,
            full_name=full_name,
            is_source_of=is_source_of,
            jurisdiction=jurisdiction,
            modification_profiles=modification_profiles,
            short_name=short_name,
            sources=sources,
            support_channels=support_channels,
            template=template,
        )
