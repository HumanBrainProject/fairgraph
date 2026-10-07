"""
Structured information on used funding.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Funding as OMFunding
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
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.publications.ScholarlyArticle",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
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
