"""
Structured information about a digital object identifier, as standardized by the International Organization for Standardization.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import DOI as OMDOI
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
            ["openminds.v5.core.BehavioralProtocol", "openminds.v5.core.Protocol"],
            "describedIn",
            reverse="described_in",
            multiple=True,
            description="reverse of 'described_in'",
        ),
        Property(
            "identifies",
            [
                "openminds.v5.core.HardwareProduct",
                "openminds.v5.publications.Book",
                "openminds.v5.publications.Chapter",
                "openminds.v5.publications.LearningResource",
                "openminds.v5.publications.ScholarlyArticle",
            ],
            "digitalIdentifier",
            reverse="digital_identifier",
            multiple=True,
            description="reverse of 'digital_identifier'",
        ),
        Property(
            "related_to",
            [
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.Interface",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ModelVersion",
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
