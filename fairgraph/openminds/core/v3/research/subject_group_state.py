"""

"""

# this file was auto-generated


from fairgraph.base import KGObject
from fairgraph.fields import Field


class SubjectGroupState(KGObject):
    """
    
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/core/SubjectGroupState"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("age_categorys", "openminds.controlledTerms.AgeCategory", "vocab:ageCategory", multiple=True, required=True,
              doc="Distinct life cycle class that is defined by a similar age or age range (developmental stage) within a group of individual beings."),
        Field("handednesss", "openminds.controlledTerms.Handedness", "vocab:handedness", multiple=True, required=False,
              doc="Degree to which an organism prefers one hand or foot over the other hand or foot during the performance of a task."),
        Field("additional_remarks", str, "vocab:additionalRemarks", multiple=False, required=False,
              doc="Mention of what deserves additional attention or notice."),
        Field("age", ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"], "vocab:age", multiple=False, required=False,
              doc="Time of life or existence at which some particular qualification, capacity or event arises."),
        Field("pathologys", ["openminds.controlledTerms.Disease", "openminds.controlledTerms.DiseaseModel"], "vocab:pathology", multiple=True, required=False,
              doc="Structural and functional deviation from the normal that constitutes a disease or characterizes a particular disease."),
        Field("weight", ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"], "vocab:weight", multiple=False, required=False,
              doc="Amount that a thing or being weighs."),
        
    ]
    existence_query_fields = ('name',)