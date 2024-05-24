"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class ParcellationEntity(KGObject):
    """
    <description not available>
    """

    default_space = "atlas"
    type_ = "https://openminds.ebrains.eu/sands/ParcellationEntity"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("abbreviation", str, "vocab:abbreviation", doc="no description available"),
        Property("alternate_names", str, "vocab:alternateName", multiple=True, doc="no description available"),
        Property(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Property(
            "has_parents",
            "openminds.sands.ParcellationEntity",
            "vocab:hasParent",
            multiple=True,
            doc="Reference to a parent object or legal person.",
        ),
        Property(
            "has_versions",
            "openminds.sands.ParcellationEntityVersion",
            "vocab:hasVersion",
            multiple=True,
            doc="Reference to variants of an original.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the parcellation entity.",
        ),
        Property(
            "ontology_identifiers",
            str,
            "vocab:ontologyIdentifier",
            multiple=True,
            doc="Term or code used to identify the parcellation entity registered within a particular ontology.",
        ),
        Property(
            "related_uberon_term",
            ["openminds.controlled_terms.Organ", "openminds.controlled_terms.UBERONParcellation"],
            "vocab:relatedUBERONTerm",
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
            "has_children",
            ["openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"],
            "^vocab:hasParent",
            reverse="has_parents",
            multiple=True,
            doc="reverse of 'hasParent'",
        ),
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
    aliases = {"versions": "has_versions"}
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        lookup_label=None,
        abbreviation=None,
        alternate_names=None,
        definition=None,
        has_children=None,
        has_parents=None,
        has_versions=None,
        is_location_of=None,
        is_target_of=None,
        is_used_to_group=None,
        ontology_identifiers=None,
        related_uberon_term=None,
        studied_in=None,
        versions=None,
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
            alternate_names=alternate_names,
            definition=definition,
            has_children=has_children,
            has_parents=has_parents,
            has_versions=has_versions,
            is_location_of=is_location_of,
            is_target_of=is_target_of,
            is_used_to_group=is_used_to_group,
            ontology_identifiers=ontology_identifiers,
            related_uberon_term=related_uberon_term,
            studied_in=studied_in,
            versions=versions,
        )
