"""
Structured information on the unit of measurement.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class UnitOfMeasurement(KGObject):
    """
    Structured information on the unit of measurement.
    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/UnitOfMeasurement"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the unit of measurement.",
        ),
        Field(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the unit of measurement.",
        ),
        Field(
            "interlex_identifier",
            IRI,
            "vocab:interlexIdentifier",
            doc="Persistent identifier for a term registered in the InterLex project.",
        ),
        Field(
            "knowledge_space_link",
            IRI,
            "vocab:knowledgeSpaceLink",
            doc="Persistent link to an encyclopedia entry in the Knowledge Space project.",
        ),
        Field(
            "preferred_ontology_identifier",
            IRI,
            "vocab:preferredOntologyIdentifier",
            doc="Persistent identifier of a preferred ontological term.",
        ),
        Field(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
        Field(
            "describes",
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
            ],
            "^vocab:keyword",
            reverse="keywords",
            multiple=True,
            doc="reverse of 'keyword'",
        ),
        Field(
            "used_by",
            ["openminds.sands.CommonCoordinateSpaceVersion", "openminds.sands.CustomCoordinateSpace"],
            "^vocab:nativeUnit",
            reverse="native_units",
            multiple=True,
            doc="reverse of 'nativeUnit'",
        ),
        Field(
            "used_in",
            "openminds.ephys.Channel",
            "^vocab:unit",
            reverse="units",
            multiple=True,
            doc="reverse of 'unit'",
        ),
        Field(
            "value",
            "openminds.core.QuantitativeValueArray",
            "^vocab:unit",
            reverse="units",
            multiple=True,
            doc="reverse of 'unit'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        description=None,
        interlex_identifier=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
        describes=None,
        used_by=None,
        used_in=None,
        value=None,
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
            definition=definition,
            description=description,
            interlex_identifier=interlex_identifier,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
            describes=describes,
            used_by=used_by,
            used_in=used_in,
            value=value,
        )
