"""

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - deterministic atlas
         - A 'deterministic atlas' is an anatomical or anatomopathological atlases based on a definite composite of a single specimen.
       * - `parcellation scheme <http://uri.neuinfo.org/nif/nifstd/nlx_144019>`_
         - A 'parcellation scheme' is a set of parcels occupying a part or all of an anatomical entity that has been delineated or annotated using a common approach or set of criteria.
       * - probabilistic atlas
         - A 'probabilistic atlas' is an anatomical or anatomopathological atlases based on statistically-weighted composites of many specimens.

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class AtlasType(KGObject):
    """

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - deterministic atlas
         - A 'deterministic atlas' is an anatomical or anatomopathological atlases based on a definite composite of a single specimen.
       * - `parcellation scheme <http://uri.neuinfo.org/nif/nifstd/nlx_144019>`_
         - A 'parcellation scheme' is a set of parcels occupying a part or all of an anatomical entity that has been delineated or annotated using a common approach or set of criteria.
       * - probabilistic atlas
         - A 'probabilistic atlas' is an anatomical or anatomopathological atlases based on statistically-weighted composites of many specimens.

    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/AtlasType"]
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
            doc="Word or phrase that constitutes the distinctive designation of the atlas type.",
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
            doc="Longer statement or account giving the characteristics of the atlas type.",
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
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "^vocab:keyword",
            reverse="keywords",
            multiple=True,
            doc="reverse of 'keyword'",
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
        )
