"""
Structured information on used funding.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Funding as OMFunding
from fairgraph import KGObject


class Funding(KGObject, OMFunding):
    """
    Structured information on used funding.
    """

    type_ = "https://openminds.om-i.org/types/Funding"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "funded",
            [
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.DatasetVersion",
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
            "funding",
            reverse="funding",
            multiple=True,
            description="reverse of 'funding'",
        ),
    ]
    existence_query_properties = ("funder",)

    def __init__(
        self,
        acknowledgement=None,
        award_number=None,
        award_title=None,
        funded=None,
        funder=None,
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
            acknowledgement=acknowledgement,
            award_number=award_number,
            award_title=award_title,
            funded=funded,
            funder=funder,
        )
