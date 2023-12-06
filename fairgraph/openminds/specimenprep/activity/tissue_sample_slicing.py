"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from datetime import datetime, time


class TissueSampleSlicing(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/specimenPrep/TissueSampleSlicing"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "custom_property_sets",
            "openminds.core.CustomPropertySet",
            "vocab:customPropertySet",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the tissue sample slicing.",
        ),
        Field(
            "device",
            "openminds.specimenprep.SlicingDeviceUsage",
            "vocab:device",
            required=True,
            doc="Piece of equipment or mechanism (hardware) designed to serve a special purpose or perform a special function.",
        ),
        Field("end_time", [datetime, time], "vocab:endTime", doc="no description available"),
        Field(
            "inputs",
            [
                "openminds.core.SubjectState",
                "openminds.core.TissueSampleCollectionState",
                "openminds.core.TissueSampleState",
            ],
            "vocab:input",
            multiple=True,
            required=True,
            doc="Something or someone that is put into or participates in a process or machine.",
        ),
        Field(
            "is_part_of",
            "openminds.core.DatasetVersion",
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Field(
            "outputs",
            ["openminds.core.TissueSampleCollectionState", "openminds.core.TissueSampleState"],
            "vocab:output",
            multiple=True,
            required=True,
            doc="Something or someone that comes out of, is delivered or produced by a process or machine.",
        ),
        Field(
            "performed_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:performedBy",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "preparation_design",
            "openminds.controlledterms.PreparationType",
            "vocab:preparationDesign",
            doc="no description available",
        ),
        Field(
            "protocols",
            "openminds.core.Protocol",
            "vocab:protocol",
            multiple=True,
            required=True,
            doc="Plan that describes the process of a scientific or medical experiment, treatment, or procedure.",
        ),
        Field("start_time", [datetime, time], "vocab:startTime", doc="no description available"),
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
            doc="Structure or function that was targeted within a study.",
        ),
        Field(
            "temperature",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:temperature",
            doc="no description available",
        ),
        Field(
            "tissue_bath_solution",
            "openminds.chemicals.ChemicalMixture",
            "vocab:tissueBathSolution",
            doc="no description available",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        custom_property_sets=None,
        description=None,
        device=None,
        end_time=None,
        inputs=None,
        is_part_of=None,
        outputs=None,
        performed_by=None,
        preparation_design=None,
        protocols=None,
        start_time=None,
        study_targets=None,
        temperature=None,
        tissue_bath_solution=None,
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
            lookup_label=lookup_label,
            custom_property_sets=custom_property_sets,
            description=description,
            device=device,
            end_time=end_time,
            inputs=inputs,
            is_part_of=is_part_of,
            outputs=outputs,
            performed_by=performed_by,
            preparation_design=preparation_design,
            protocols=protocols,
            start_time=start_time,
            study_targets=study_targets,
            temperature=temperature,
            tissue_bath_solution=tissue_bath_solution,
        )
