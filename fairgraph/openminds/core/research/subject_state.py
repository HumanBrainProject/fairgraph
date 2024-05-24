"""
Structured information on a temporary state of a subject.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class SubjectState(KGObject):
    """
    Structured information on a temporary state of a subject.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/SubjectState"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Property(
            "age",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:age",
            doc="Time of life or existence at which some particular qualification, capacity or event arises.",
        ),
        Property(
            "age_category",
            "openminds.controlled_terms.AgeCategory",
            "vocab:ageCategory",
            required=True,
            doc="Distinct life cycle class that is defined by a similar age or age range (developmental stage) within a group of individual beings.",
        ),
        Property(
            "attributes",
            "openminds.controlled_terms.SubjectAttribute",
            "vocab:attribute",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "descended_from", "openminds.core.SubjectState", "vocab:descendedFrom", doc="no description available"
        ),
        Property(
            "handedness",
            "openminds.controlled_terms.Handedness",
            "vocab:handedness",
            doc="Degree to which an organism prefers one hand or foot over the other hand or foot during the performance of a task.",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the subject state within a particular product.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "pathologies",
            ["openminds.controlled_terms.Disease", "openminds.controlled_terms.DiseaseModel"],
            "vocab:pathology",
            multiple=True,
            doc="Structural and functional deviation from the normal that constitutes a disease or characterizes a particular disease.",
        ),
        Property(
            "relative_time_indication",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:relativeTimeIndication",
            doc="no description available",
        ),
        Property(
            "weight",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:weight",
            doc="Amount that a thing or being weighs.",
        ),
    ]
    reverse_properties = [
        Property(
            "has_children",
            [
                "openminds.core.SubjectState",
                "openminds.core.TissueSampleCollectionState",
                "openminds.core.TissueSampleState",
            ],
            "^vocab:descendedFrom",
            reverse="descended_from",
            multiple=True,
            doc="reverse of 'descendedFrom'",
        ),
        Property(
            "is_input_to",
            [
                "openminds.ephys.RecordingActivity",
                "openminds.specimen_prep.TissueCulturePreparation",
                "openminds.specimen_prep.TissueSampleSlicing",
            ],
            "^vocab:input",
            reverse="inputs",
            multiple=True,
            doc="reverse of 'input'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.core.ProtocolExecution",
                "openminds.ephys.CellPatching",
                "openminds.ephys.ElectrodePlacement",
                "openminds.specimen_prep.CranialWindowPreparation",
                "openminds.stimulation.StimulationActivity",
            ],
            "^vocab:output",
            reverse="outputs",
            multiple=True,
            doc="reverse of 'output'",
        ),
        Property(
            "is_state_of",
            "openminds.core.Subject",
            "^vocab:studiedState",
            reverse="studied_states",
            multiple=True,
            doc="reverse of 'studiedState'",
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
            "used_in",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            "^vocab:usedSpecimen",
            reverse="used_specimens",
            multiple=True,
            doc="reverse of 'usedSpecimen'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        additional_remarks=None,
        age=None,
        age_category=None,
        attributes=None,
        descended_from=None,
        handedness=None,
        has_children=None,
        internal_identifier=None,
        is_input_to=None,
        is_output_of=None,
        is_state_of=None,
        is_used_to_group=None,
        pathologies=None,
        relative_time_indication=None,
        used_in=None,
        weight=None,
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
            additional_remarks=additional_remarks,
            age=age,
            age_category=age_category,
            attributes=attributes,
            descended_from=descended_from,
            handedness=handedness,
            has_children=has_children,
            internal_identifier=internal_identifier,
            is_input_to=is_input_to,
            is_output_of=is_output_of,
            is_state_of=is_state_of,
            is_used_to_group=is_used_to_group,
            pathologies=pathologies,
            relative_time_indication=relative_time_indication,
            used_in=used_in,
            weight=weight,
        )
