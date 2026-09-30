"""
An International Standard Book Number of the International ISBN Agency.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ISBN as OMISBN
from fairgraph import KGObject


class ISBN(KGObject, OMISBN):
    """
    An International Standard Book Number of the International ISBN Agency.
    """

    type_ = "https://openminds.om-i.org/types/ISBN"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "cited_in",
            [
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.ScholarlyArticle",
            ],
            "citedPublication",
            reverse="cited_publications",
            multiple=True,
            description="reverse of 'cited_publications'",
        ),
        Property(
            "identifies",
            [
                "openminds.v4.publications.Book",
                "openminds.v4.sands.BrainAtlas",
                "openminds.v4.sands.CommonCoordinateSpace",
            ],
            "digitalIdentifier",
            reverse="digital_identifier",
            multiple=True,
            description="reverse of 'digital_identifier'",
        ),
        Property(
            "related_to",
            [
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.WebServiceVersion",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "relatedPublication",
            reverse="related_publications",
            multiple=True,
            description="reverse of 'related_publications'",
        ),
    ]
    existence_query_properties = ("identifier",)

    def __init__(
        self,
        cited_in=None,
        identifier=None,
        identifies=None,
        related_to=None,
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
            cited_in=cited_in,
            identifier=identifier,
            identifies=identifies,
            related_to=related_to,
        )
