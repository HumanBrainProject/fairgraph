"""
An International Standard Serial Number of the ISSN International Centre.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ISSN as OMISSN
from fairgraph import KGObject


class ISSN(KGObject, OMISSN):
    """
    An International Standard Serial Number of the ISSN International Centre.
    """

    type_ = "https://openminds.om-i.org/types/ISSN"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            "openminds.v4.publications.Periodical",
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
        self, identifier=None, identifies=None, related_to=None, id=None, data=None, space=None, release_status=None
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            identifier=identifier,
            identifies=identifies,
            related_to=related_to,
        )
