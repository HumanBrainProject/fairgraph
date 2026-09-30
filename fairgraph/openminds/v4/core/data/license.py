"""
Structured information on a used license.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import License as OMLicense
from fairgraph import KGObject


from openminds import IRI


class License(KGObject, OMLicense):
    """
    Structured information on a used license.
    """

    type_ = "https://openminds.om-i.org/types/License"
    default_space = "controlled"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_applied_to",
            [
                "openminds.v4.computation.ValidationTestVersion",
                "openminds.v4.computation.WorkflowRecipeVersion",
                "openminds.v4.core.DatasetVersion",
                "openminds.v4.core.MetaDataModelVersion",
                "openminds.v4.core.ModelVersion",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.publications.Book",
                "openminds.v4.publications.Chapter",
                "openminds.v4.publications.LearningResource",
                "openminds.v4.publications.LivePaperVersion",
                "openminds.v4.publications.ScholarlyArticle",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
            ],
            "license",
            reverse="license",
            multiple=True,
            description="reverse of 'license'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("alias",)
    sort_property = "full_name"

    def __init__(
        self,
        name=None,
        alias=None,
        full_name=None,
        is_applied_to=None,
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
            full_name=full_name,
            is_applied_to=is_applied_to,
            legal_code=legal_code,
            short_name=short_name,
            webpages=webpages,
        )
