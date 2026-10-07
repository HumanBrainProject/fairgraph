"""
Structured information on the technique.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.controlled_terms import Technique as OMTechnique
from fairgraph import KGObject


from openminds import IRI


class Technique(KGObject, OMTechnique):
    """
    Structured information on the technique.
    """

    type_ = "https://openminds.om-i.org/types/Technique"
    default_space = "controlled"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v5.computation.ValidationTestVersion",
                "openminds.v5.computation.WorkflowRecipe",
                "openminds.v5.computation.WorkflowRecipeVersion",
                "openminds.v5.core.Dataset",
                "openminds.v5.core.Interface",
                "openminds.v5.core.InterfaceVersion",
                "openminds.v5.core.MetaDataModel",
                "openminds.v5.core.MetaDataModelVersion",
                "openminds.v5.core.Model",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.Software",
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
            "is_reference_for",
            "openminds.v5.computation.ValidationTest",
            "referenceDataAcquisition",
            reverse="reference_data_acquisitions",
            multiple=True,
            description="reverse of 'reference_data_acquisitions'",
        ),
        Property(
            "is_scope_of",
            ["openminds.v5.core.HardwareProduct", "openminds.v5.core.Service", "openminds.v5.core.SoftwareVersion"],
            "scope",
            reverse="scopes",
            multiple=True,
            description="reverse of 'scopes'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v5.core.FileBundle",
            "groupedBy",
            reverse="grouped_by",
            multiple=True,
            description="reverse of 'grouped_by'",
        ),
        Property(
            "used_in",
            ["openminds.v5.core.DatasetVersion", "openminds.v5.core.Protocol"],
            "technique",
            reverse="techniques",
            multiple=True,
            description="reverse of 'techniques'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        describes=None,
        description=None,
        is_reference_for=None,
        is_scope_of=None,
        is_used_to_group=None,
        other_cross_references=None,
        other_ontology_identifiers=None,
        preferred_cross_reference=None,
        preferred_ontology_identifier=None,
        synonyms=None,
        used_in=None,
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
            is_reference_for=is_reference_for,
            is_scope_of=is_scope_of,
            is_used_to_group=is_used_to_group,
            other_cross_references=other_cross_references,
            other_ontology_identifiers=other_ontology_identifiers,
            preferred_cross_reference=preferred_cross_reference,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
            used_in=used_in,
        )
