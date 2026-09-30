"""
Structured information on the quality type of the defined criteria for a measurement.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.controlled_terms import CriteriaQualityType as OMCriteriaQualityType
from fairgraph import KGObject


from openminds import IRI


class CriteriaQualityType(KGObject, OMCriteriaQualityType):
    """
    Structured information on the quality type of the defined criteria for a measurement.
    """

    type_ = "https://openminds.om-i.org/types/CriteriaQualityType"
    default_space = "controlled"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v5.computation.ValidationTest",
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.DatasetVersion",
                "openminds.v5.core.HardwareProduct",
                "openminds.v5.core.Interface",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.Service",
                "openminds.v5.core.Software",
                "openminds.v5.core.SoftwareVersion",
                "openminds.v5.publications.Book",
                "openminds.v5.publications.Chapter",
                "openminds.v5.publications.LearningResource",
                "openminds.v5.publications.LivePaper",
                "openminds.v5.publications.LivePaperVersion",
                "openminds.v5.publications.ScholarlyArticle",
                "openminds.v5.sands.AnatomicalAtlas",
                "openminds.v5.sands.AnatomicalAtlasVersion",
                "openminds.v5.sands.CommonCoordinateFramework",
                "openminds.v5.sands.CommonCoordinateFrameworkVersion",
            ],
            "keyword",
            reverse="keywords",
            multiple=True,
            description="reverse of 'keywords'",
        ),
        Property(
            "used_by_annotation",
            ["openminds.v5.sands.AtlasAnnotation", "openminds.v5.sands.CustomAnnotation"],
            "criteriaQualityType",
            reverse="criteria_quality_type",
            multiple=True,
            description="reverse of 'criteria_quality_type'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        describes=None,
        description=None,
        other_cross_references=None,
        other_ontology_identifiers=None,
        preferred_cross_reference=None,
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
            other_cross_references=other_cross_references,
            other_ontology_identifiers=other_ontology_identifiers,
            preferred_cross_reference=preferred_cross_reference,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
            used_by_annotation=used_by_annotation,
        )
