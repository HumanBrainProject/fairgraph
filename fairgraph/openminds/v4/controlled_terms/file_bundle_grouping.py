"""
Structured information on the grouping mechanism of a file bundle.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.controlled_terms import FileBundleGrouping as OMFileBundleGrouping
from fairgraph import KGObject


from openminds import IRI


class FileBundleGrouping(KGObject, OMFileBundleGrouping):
    """
    Structured information on the grouping mechanism of a file bundle.
    """

    type_ = "https://openminds.om-i.org/types/FileBundleGrouping"
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
            "is_defined_by",
            "openminds.v4.core.FilePathPattern",
            "groupingType",
            reverse="grouping_types",
            multiple=True,
            description="reverse of 'grouping_types'",
        ),
        Property(
            "is_used_to_group",
            "openminds.v4.core.FileBundle",
            "groupingType",
            reverse="grouping_types",
            multiple=True,
            description="reverse of 'grouping_types'",
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
        is_defined_by=None,
        is_used_to_group=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
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
            is_defined_by=is_defined_by,
            is_used_to_group=is_used_to_group,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
        )
