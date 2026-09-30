"""
Structured information on the quality type of the defined criteria for a measurement.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.controlled_terms import CriteriaQualityType as OMCriteriaQualityType
from fairgraph import KGObject


from openminds import IRI


class CriteriaQualityType(KGObject, OMCriteriaQualityType):
    """
    Structured information on the quality type of the defined criteria for a measurement.
    """

    type_ = "https://openminds.om-i.org/types/CriteriaQualityType"
    default_space = "controlled"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
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
            "keyword",
            reverse="keywords",
            multiple=True,
            description="reverse of 'keywords'",
        ),
        Property(
            "used_by_annotation",
            ["openminds.v4.sands.AtlasAnnotation", "openminds.v4.sands.CustomAnnotation"],
            "criteriaQualityType",
            reverse="criteria_quality_type",
            multiple=True,
            description="reverse of 'criteria_quality_type'",
        ),
    ]
    existence_query_properties = ("name",)
    sort_property = "name"

    def __init__(
        self,
        name=None,
        definition=None,
        describes=None,
        description=None,
        interlex_identifier=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
        used_by_annotation=None,
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
            definition=definition,
            describes=describes,
            description=description,
            interlex_identifier=interlex_identifier,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
            used_by_annotation=used_by_annotation,
        )
