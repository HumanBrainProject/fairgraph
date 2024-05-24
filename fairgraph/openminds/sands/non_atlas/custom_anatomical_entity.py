"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class CustomAnatomicalEntity(KGObject):
    """
    <description not available>
    """

    default_space = "spatial"
    type_ = "https://openminds.ebrains.eu/sands/CustomAnatomicalEntity"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "has_annotations",
            "openminds.sands.CustomAnnotation",
            "vocab:hasAnnotation",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the custom anatomical entity.",
        ),
        Property(
            "related_uberon_term",
            ["openminds.controlled_terms.Organ", "openminds.controlled_terms.UBERONParcellation"],
            "vocab:relatedUBERONTerm",
            doc="no description available",
        ),
        Property(
            "relation_assessments",
            ["openminds.sands.QualitativeRelationAssessment", "openminds.sands.QuantitativeRelationAssessment"],
            "vocab:relationAssessment",
            multiple=True,
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
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
        Property(
            "is_target_of",
            "openminds.sands.AnatomicalTargetPosition",
            "^vocab:anatomicalTarget",
            reverse="anatomical_targets",
            multiple=True,
            doc="reverse of 'anatomicalTarget'",
        ),
        Property(
            "is_used_to_group",
            "openminds.core.FileBundle",
            "^vocab:groupedBy",
            reverse="grouped_by",
            multiple=True,
            doc="reverse of 'groupedBy'",
        ),
        Property(
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
                "openminds.specimen_prep.CranialWindowPreparation",
                "openminds.specimen_prep.TissueCulturePreparation",
                "openminds.specimen_prep.TissueSampleSlicing",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:studyTarget",
            reverse="study_targets",
            multiple=True,
            doc="reverse of 'studyTarget'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        has_annotations=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        related_uberon_term=None,
        relation_assessments=None,
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
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            related_uberon_term=related_uberon_term,
            relation_assessments=relation_assessments,
            studied_in=studied_in,
        )
