"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class CustomAnatomicalEntity(KGObject):
    """
    <description not available>
    """

    default_space = "spatial"
    type_ = ["https://openminds.ebrains.eu/sands/CustomAnatomicalEntity"]
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
            doc="Word or phrase that constitutes the distinctive designation of the custom anatomical entity.",
        ),
        Field(
            "has_annotations",
            "openminds.sands.CustomAnnotation",
            "vocab:hasAnnotation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "related_uberon_term",
            ["openminds.controlledterms.Organ", "openminds.controlledterms.UBERONParcellation"],
            "vocab:relatedUBERONTerm",
            doc="no description available",
        ),
        Field(
            "relation_assessments",
            ["openminds.sands.QualitativeRelationAssessment", "openminds.sands.QuantitativeRelationAssessment"],
            "vocab:relationAssessment",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "is_location_of",
            [
                "openminds.core.TissueSample",
                "openminds.core.TissueSampleCollection",
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
            ],
            ["^vocab:anatomicalLocation", "^vocab:anatomicalLocationOfElectrodes"],
            reverse=["anatomical_locations", "anatomical_locations_of_electrodes"],
            multiple=True,
            doc="reverse of anatomicalLocation, anatomicalLocationOfElectrodes",
        ),
        Field(
            "is_target_of",
            "openminds.sands.AnatomicalTargetPosition",
            "^vocab:anatomicalTarget",
            reverse="anatomical_targets",
            multiple=True,
            doc="reverse of 'anatomicalTarget'",
        ),
        Field(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Field(
            "studied_in",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.ValidationTest",
                "openminds.computation.Visualization",
                "openminds.core.DatasetVersion",
                "openminds.core.Model",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.ephys.RecordingActivity",
                "openminds.specimenprep.CranialWindowPreparation",
                "openminds.specimenprep.TissueCulturePreparation",
                "openminds.specimenprep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:studyTarget",
            reverse="study_targets",
            multiple=True,
            doc="reverse of 'studyTarget'",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        has_annotations=None,
        related_uberon_term=None,
        relation_assessments=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        studied_in=None,
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
            has_annotations=has_annotations,
            related_uberon_term=related_uberon_term,
            relation_assessments=relation_assessments,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            studied_in=studied_in,
        )
