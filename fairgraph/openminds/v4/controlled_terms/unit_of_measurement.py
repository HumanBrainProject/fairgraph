"""
Structured information on the unit of measurement.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.controlled_terms import UnitOfMeasurement as OMUnitOfMeasurement
from fairgraph import KGObject


from openminds import IRI


class UnitOfMeasurement(KGObject, OMUnitOfMeasurement):
    """
    Structured information on the unit of measurement.
    """

    type_ = "https://openminds.om-i.org/types/UnitOfMeasurement"
    default_space = "controlled"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
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
            ],
            "keyword",
            reverse="keywords",
            multiple=True,
            description="reverse of 'keywords'",
        ),
        Property(
            "used_by",
            ["openminds.v4.sands.CommonCoordinateSpaceVersion", "openminds.v4.sands.CustomCoordinateSpace"],
            "nativeUnit",
            reverse="native_unit",
            multiple=True,
            description="reverse of 'native_unit'",
        ),
        Property(
            "used_in",
            "openminds.v4.ephys.Channel",
            "unit",
            reverse="unit",
            multiple=True,
            description="reverse of 'unit'",
        ),
        Property(
            "value",
            "openminds.v4.core.QuantitativeValueArray",
            "unit",
            reverse="unit",
            multiple=True,
            description="reverse of 'unit'",
        ),
    ]
    existence_query_properties = ("name",)

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
        used_by=None,
        used_in=None,
        value=None,
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
            used_by=used_by,
            used_in=used_in,
            value=value,
        )
