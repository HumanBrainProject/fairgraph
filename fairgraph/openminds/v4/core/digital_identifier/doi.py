"""
Structured information about a digital object identifier, as standardized by the International Organization for Standardization.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import DOI as OMDOI
from fairgraph import KGObject


class DOI(KGObject, OMDOI):
    """
    Structured information about a digital object identifier, as standardized by the International Organization for Standardization.
    """

    type_ = "https://openminds.om-i.org/types/DOI"
    default_space = "dataset"
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
            "identifies",
            [
                "openminds.v4.computation.ValidationTest",
                "openminds.v4.computation.WorkflowRecipe",
                "openminds.v4.core.Dataset",
                "openminds.v4.core.MetaDataModel",
                "openminds.v4.core.Model",
                "openminds.v4.core.Software",
                "openminds.v4.ephys.Electrode",
                "openminds.v4.ephys.ElectrodeArray",
                "openminds.v4.ephys.Pipette",
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.LivePaper",
                "openminds.v4.publications.ScholarlyArticle",
                "openminds.v4.sands.BrainAtlas",
                "openminds.v4.sands.CommonCoordinateSpace",
                "openminds.v4.specimen_prep.SlicingDevice",
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
        describes=None,
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
            describes=describes,
            identifier=identifier,
            identifies=identifies,
            related_to=related_to,
        )
