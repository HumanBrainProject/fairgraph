"""
Structured information on a used license.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from fairgraph.base import IRI


class License(KGObject):
    """
    Structured information on a used license.
    """

    default_space = "controlled"
    type_ = "https://openminds.ebrains.eu/core/License"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("full_name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the license."),
        Property(
            "legal_code",
            IRI,
            "vocab:legalCode",
            required=True,
            doc="Type of legislation that claims to cover the law system (complete or parts) as it existed at the time the code was enacted.",
        ),
        Property(
            "short_name",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the license.",
        ),
        Property(
            "webpages",
            str,
            "vocab:webpage",
            multiple=True,
            doc="Hypertext document (block of information) found on the World Wide Web.",
        ),
    ]
    reverse_properties = [
        Property(
            "is_applied_to",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.LivePaperVersion",
                "openminds.publications.ScholarlyArticle",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:license",
            reverse="licenses",
            multiple=True,
            doc="reverse of 'license'",
        ),
    ]
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("alias",)

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
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            alias=alias,
            full_name=full_name,
            is_applied_to=is_applied_to,
            legal_code=legal_code,
            short_name=short_name,
            webpages=webpages,
        )
