"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ParcellationEntityVersion(KGObject):
    """
    <description not available>
    """

    default_space = "atlas"
    type_ = "https://openminds.ebrains.eu/sands/ParcellationEntityVersion"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("abbreviation", str, "vocab:abbreviation", doc="no description available"),
        Property(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Property("alternate_names", str, "vocab:alternateName", multiple=True, doc="no description available"),
        Property("corrected_name", str, "vocab:correctedName", doc="no description available"),
        Property(
            "has_annotations",
            "openminds.sands.AtlasAnnotation",
            "vocab:hasAnnotation",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "has_parents",
            ["openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"],
            "vocab:hasParent",
            multiple=True,
            doc="Reference to a parent object or legal person.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the parcellation entity version.",
        ),
        Property(
            "ontology_identifiers",
            str,
            "vocab:ontologyIdentifier",
            multiple=True,
            doc="Term or code used to identify the parcellation entity version registered within a particular ontology.",
        ),
        Property(
            "relation_assessments",
            ["openminds.sands.QualitativeRelationAssessment", "openminds.sands.QuantitativeRelationAssessment"],
            "vocab:relationAssessment",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "version_identifier",
            str,
            "vocab:versionIdentifier",
            required=True,
            doc="Term or code used to identify the version of something.",
        ),
        Property(
            "version_innovation",
            str,
            "vocab:versionInnovation",
            doc="Documentation on what changed in comparison to a previously published form of something.",
        ),
        Property(
            "has_children",
            "openminds.sands.ParcellationEntityVersion",
            "^vocab:hasParent",
            reverse="has_parents",
            multiple=True,
            doc="reverse of 'hasParent'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.core.ServiceLink",
                "openminds.core.TissueSample",
                "openminds.core.TissueSampleCollection",
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
            ],
            ["^vocab:anatomicalLocation", "^vocab:anatomicalLocationOfElectrodes", "^vocab:dataLocation"],
            reverse=["anatomical_locations", "anatomical_locations_of_electrodes", "data_locations"],
            multiple=True,
            doc="reverse of anatomicalLocation, anatomicalLocationOfElectrodes, dataLocation",
        ),
        Property(
            "is_part_of",
            "openminds.sands.ParcellationTerminologyVersion",
            "^vocab:hasEntity",
            reverse="has_entities",
            multiple=True,
            doc="reverse of 'hasEntity'",
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
            "is_version_of",
            "openminds.sands.ParcellationEntity",
            "^vocab:hasVersion",
            reverse="has_versions",
            multiple=True,
            doc="reverse of 'hasVersion'",
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
    existence_query_properties = ("name", "version_identifier")

    def __init__(
        self,
        name=None,
        lookup_label=None,
        abbreviation=None,
        additional_remarks=None,
        alternate_names=None,
        corrected_name=None,
        has_annotations=None,
        has_children=None,
        has_parents=None,
        is_location_of=None,
        is_part_of=None,
        is_target_of=None,
        is_used_to_group=None,
        is_version_of=None,
        ontology_identifiers=None,
        relation_assessments=None,
        studied_in=None,
        version_identifier=None,
        version_innovation=None,
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
            lookup_label=lookup_label,
            abbreviation=abbreviation,
            additional_remarks=additional_remarks,
            alternate_names=alternate_names,
            corrected_name=corrected_name,
            has_annotations=has_annotations,
            has_children=has_children,
            has_parents=has_parents,
            is_location_of=is_location_of,
            is_part_of=is_part_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            is_version_of=is_version_of,
            ontology_identifiers=ontology_identifiers,
            relation_assessments=relation_assessments,
            studied_in=studied_in,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
        )
