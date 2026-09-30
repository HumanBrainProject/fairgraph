"""
Structured information on a used license.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import License as OMLicense
from fairgraph import KGObject


from openminds import IRI


class License(KGObject, OMLicense):
    """
    Structured information on a used license.
    """

    type_ = "https://openminds.om-i.org/types/License"
    default_space = "controlled"
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
    existence_query_properties = ("alias",)

    def __init__(
        self,
        name=None,
        alias=None,
        applies_to=None,
        full_name=None,
        is_source_of=None,
        legal_code=None,
        short_name=None,
        webpages=None,
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
            full_name=full_name,
            is_source_of=is_source_of,
            legal_code=legal_code,
            short_name=short_name,
            webpages=webpages,
        )
