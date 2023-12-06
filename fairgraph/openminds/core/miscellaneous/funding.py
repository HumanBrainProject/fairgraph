"""
Structured information on used funding.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Funding(KGObject):
    """
    Structured information on used funding.
    """

    default_space = "common"
    type_ = ["https://openminds.ebrains.eu/core/Funding"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "acknowledgement",
            str,
            "vocab:acknowledgement",
            doc="Official declaration or avowal of appreciation of an act or achievement.",
        ),
        Field(
            "award_number",
            str,
            "vocab:awardNumber",
            doc="Machine-readable identifier for a benefit that is conferred or bestowed on the basis of merit or need.",
        ),
        Field(
            "award_title",
            str,
            "vocab:awardTitle",
            doc="Human-readable identifier for a benefit that is conferred or bestowed on the basis of merit or need.",
        ),
        Field(
            "funder",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:funder",
            required=True,
            doc="Legal person that provides money for a particular purpose.",
        ),
        Field(
            "funded",
            [
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowRecipeVersion",
                "openminds.core.DatasetVersion",
                "openminds.core.MetaDataModelVersion",
                "openminds.core.ModelVersion",
                "openminds.core.SoftwareVersion",
                "openminds.core.WebServiceVersion",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.LearningResource",
                "openminds.publications.LivePaperVersion",
                "openminds.publications.ScholarlyArticle",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:funding",
            reverse="funding",
            multiple=True,
            doc="reverse of 'funding'",
        ),
    ]
    existence_query_fields = ("funder",)

    def __init__(
        self,
        acknowledgement=None,
        award_number=None,
        award_title=None,
        funder=None,
        funded=None,
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
            acknowledgement=acknowledgement,
            award_number=award_number,
            award_title=award_title,
            funder=funder,
            funded=funded,
        )
