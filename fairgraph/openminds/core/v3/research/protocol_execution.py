"""
Structured information on a protocol execution.
"""

# this file was auto-generated


from fairgraph.base import KGObject
from fairgraph.fields import Field


class ProtocolExecution(KGObject):
    """
    Structured information on a protocol execution.
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/core/ProtocolExecution"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the protocol execution."),
        Field("inputs", ["openminds.core.FileBundle", "openminds.core.File", "openminds.core.SubjectGroupState", "openminds.core.SubjectState", "openminds.core.TissueSampleCollectionState", "openminds.core.TissueSampleState"], "vocab:input", multiple=True, required=True,
              doc="Something or someone that is put into or participates in a process or machine."),
        Field("outputs", ["openminds.core.FileBundle", "openminds.core.File", "openminds.core.SubjectGroupState", "openminds.core.SubjectState", "openminds.core.TissueSampleCollectionState", "openminds.core.TissueSampleState"], "vocab:output", multiple=True, required=True,
              doc="Something or someone that comes out of, is delivered or produced by a process or machine."),
        Field("parameter_sets", "openminds.core.ParameterSet", "vocab:parameterSet", multiple=True, required=False,
              doc="Manner, position, or direction in which digital or physical properties are set to determine a particular function, characteristics or behavior of something."),
        Field("preparation_type", "openminds.controlledTerms.PreparationType", "vocab:preparationType", multiple=False, required=False,
              doc="Distinct class of actions or processes that make something ready for use or service."),
        Field("protocol", "openminds.core.Protocol", "vocab:protocol", multiple=False, required=True,
              doc="Plan that describes the process of a scientific or medical experiment, treatment, or procedure."),
        Field("semantically_anchored_tos", "openminds.sands.AnatomicalEntity", "vocab:semanticallyAnchoredTo", multiple=True, required=False,
              doc="Reference to a related anatomical structure without providing a quantitative proof of the claimed relation."),
        Field("study_targets", ["openminds.sands.AnatomicalEntity", "openminds.controlledTerms.CellType", "openminds.controlledTerms.Organ", "openminds.controlledTerms.Strain", "openminds.controlledTerms.Species", "openminds.controlledTerms.BiologicalSex", "openminds.controlledTerms.TermSuggestion", "openminds.controlledTerms.Disease", "openminds.controlledTerms.Handedness", "openminds.controlledTerms.DiseaseModel", "openminds.controlledTerms.Phenotype"], "vocab:studyTarget", multiple=True, required=False,
              doc="Structure or function that was targeted within a study."),
        
    ]
    existence_query_fields = ('name',)