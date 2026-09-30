"""
A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import HANDLE as OMHANDLE
from fairgraph import KGObject


class HANDLE(KGObject, OMHANDLE):
    """
    A persistent identifier for an information resource provided by the Handle System of the Corporation for National Research Initiatives.
    """

    type_ = "https://openminds.om-i.org/types/HANDLE"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
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

    def __init__(self, identifier=None, related_to=None, id=None, data=None, space=None, release_status=None):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            identifier=identifier,
            related_to=related_to,
        )
