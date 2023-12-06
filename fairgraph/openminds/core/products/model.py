"""
Structured information on a computational model (concept level).
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from openminds.base import IRI


class Model(KGObject):
    """
    Structured information on a computational model (concept level).
    """

    default_space = "model"
    type_ = ["https://openminds.ebrains.eu/core/Model"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the model."),
        Field("alias", str, "vocab:shortName", required=True, doc="Shortened or fully abbreviated name of the model."),
        Field(
            "abstraction_level",
            "openminds.controlledterms.ModelAbstractionLevel",
            "vocab:abstractionLevel",
            required=True,
            doc="Extent of simplification of physical, spatial, or temporal details or attributes in the study of objects or systems.",
        ),
        Field(
            "custodians",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:custodian",
            multiple=True,
            doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the model.",
        ),
        Field(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            required=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Field(
            "digital_identifier",
            ["openminds.core.DOI", "openminds.core.SWHID"],
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the model."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Field(
            "model_scope",
            "openminds.controlledterms.ModelScope",
            "vocab:scope",
            required=True,
            doc="Extent of something.",
        ),
        Field(
            "study_targets",
            [
                "openminds.controlledterms.AuditoryStimulusType",
                "openminds.controlledterms.BiologicalOrder",
                "openminds.controlledterms.BiologicalSex",
                "openminds.controlledterms.BreedingType",
                "openminds.controlledterms.CellCultureType",
                "openminds.controlledterms.CellType",
                "openminds.controlledterms.Disease",
                "openminds.controlledterms.DiseaseModel",
                "openminds.controlledterms.ElectricalStimulusType",
                "openminds.controlledterms.GeneticStrainType",
                "openminds.controlledterms.GustatoryStimulusType",
                "openminds.controlledterms.Handedness",
                "openminds.controlledterms.MolecularEntity",
                "openminds.controlledterms.OlfactoryStimulusType",
                "openminds.controlledterms.OpticalStimulusType",
                "openminds.controlledterms.Organ",
                "openminds.controlledterms.OrganismSubstance",
                "openminds.controlledterms.OrganismSystem",
                "openminds.controlledterms.Species",
                "openminds.controlledterms.SubcellularEntity",
                "openminds.controlledterms.TactileStimulusType",
                "openminds.controlledterms.TermSuggestion",
                "openminds.controlledterms.TissueSampleType",
                "openminds.controlledterms.UBERONParcellation",
                "openminds.controlledterms.VisualStimulusType",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:studyTarget",
            multiple=True,
            required=True,
            doc="Structure or function that was targeted within a study.",
        ),
        Field(
            "versions",
            "openminds.core.ModelVersion",
            "vocab:hasVersion",
            multiple=True,
            required=True,
            doc="Reference to variants of an original.",
        ),
        Field(
            "comments",
            "openminds.core.Comment",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
        Field(
            "is_part_of",
            ["openminds.core.Project", "openminds.core.ResearchProductGroup"],
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Field(
            "learning_resources",
            "openminds.publications.LearningResource",
            "^vocab:about",
            reverse="about",
            multiple=True,
            doc="reverse of 'about'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        alias=None,
        abstraction_level=None,
        custodians=None,
        description=None,
        developers=None,
        digital_identifier=None,
        homepage=None,
        how_to_cite=None,
        model_scope=None,
        study_targets=None,
        versions=None,
        comments=None,
        is_part_of=None,
        learning_resources=None,
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
            abstraction_level=abstraction_level,
            custodians=custodians,
            description=description,
            developers=developers,
            digital_identifier=digital_identifier,
            homepage=homepage,
            how_to_cite=how_to_cite,
            model_scope=model_scope,
            study_targets=study_targets,
            versions=versions,
            comments=comments,
            is_part_of=is_part_of,
            learning_resources=learning_resources,
        )
