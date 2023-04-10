"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import KGObject, IRI
from fairgraph.fields import Field




class TissueCulturePreparation(KGObject):
    """

    """
    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/specimenPrep/TissueCulturePreparation"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", multiple=False, required=False,
              doc="no description available"),
        Field("culture_medium", "openminds.chemicals.ChemicalMixture", "vocab:cultureMedium", multiple=False, required=True,
              doc="no description available"),
        Field("culture_type", "openminds.controlledterms.CellCultureType", "vocab:cultureType", multiple=False, required=True,
              doc="no description available"),
        Field("custom_property_sets", "openminds.core.CustomPropertySet", "vocab:customPropertySet", multiple=True, required=False,
              doc="no description available"),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the tissue culture preparation."),
        Field("end_time", datetime, "vocab:endTime", multiple=False, required=False,
              doc="no description available"),
        Field("inputs", ["openminds.core.SubjectGroupState", "openminds.core.SubjectState", "openminds.core.TissueSampleCollectionState", "openminds.core.TissueSampleState"], "vocab:input", multiple=True, required=True,
              doc="Something or someone that is put into or participates in a process or machine."),
        Field("is_part_of", "openminds.core.DatasetVersion", "vocab:isPartOf", multiple=False, required=True,
              doc="Reference to the ensemble of multiple things or beings."),
        Field("outputs", "openminds.core.TissueSampleState", "vocab:output", multiple=True, required=True,
              doc="Something or someone that comes out of, is delivered or produced by a process or machine."),
        Field("performed_by", ["openminds.computation.SoftwareAgent", "openminds.core.Person"], "vocab:performedBy", multiple=True, required=False,
              doc="no description available"),
        Field("preparation_design", "openminds.controlledterms.PreparationType", "vocab:preparationDesign", multiple=False, required=False,
              doc="no description available"),
        Field("protocols", "openminds.core.Protocol", "vocab:protocol", multiple=True, required=True,
              doc="Plan that describes the process of a scientific or medical experiment, treatment, or procedure."),
        Field("start_time", datetime, "vocab:startTime", multiple=False, required=False,
              doc="no description available"),
        Field("study_targets", ["openminds.controlledterms.AuditoryStimulusType", "openminds.controlledterms.BiologicalOrder", "openminds.controlledterms.BiologicalSex", "openminds.controlledterms.BreedingType", "openminds.controlledterms.CellCultureType", "openminds.controlledterms.CellType", "openminds.controlledterms.Disease", "openminds.controlledterms.DiseaseModel", "openminds.controlledterms.ElectricalStimulusType", "openminds.controlledterms.GeneticStrainType", "openminds.controlledterms.GustatoryStimulusType", "openminds.controlledterms.Handedness", "openminds.controlledterms.MolecularEntity", "openminds.controlledterms.OlfactoryStimulusType", "openminds.controlledterms.OpticalStimulusType", "openminds.controlledterms.Organ", "openminds.controlledterms.OrganismSubstance", "openminds.controlledterms.OrganismSystem", "openminds.controlledterms.Species", "openminds.controlledterms.SubcellularEntity", "openminds.controlledterms.TactileStimulusType", "openminds.controlledterms.TermSuggestion", "openminds.controlledterms.UBERONParcellation", "openminds.controlledterms.VisualStimulusType", "openminds.sands.CustomAnatomicalEntity", "openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"], "vocab:studyTarget", multiple=True, required=False,
              doc="Structure or function that was targeted within a study."),

    ]
    existence_query_fields = ('lookup_label',)

    def __init__(self, lookup_label=None, culture_medium=None, culture_type=None, custom_property_sets=None, description=None, end_time=None, inputs=None, is_part_of=None, outputs=None, performed_by=None, preparation_design=None, protocols=None, start_time=None, study_targets=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, data=data, space=space, scope=scope, lookup_label=lookup_label, culture_medium=culture_medium, culture_type=culture_type, custom_property_sets=custom_property_sets, description=description, end_time=end_time, inputs=inputs, is_part_of=is_part_of, outputs=outputs, performed_by=performed_by, preparation_design=preparation_design, protocols=protocols, start_time=start_time, study_targets=study_targets)