"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class TissueSampleCollection(KGObject):
    """
    <description not available>
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/TissueSampleCollection"
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
            "anatomical_locations",
            [
                "openminds.controlled_terms.CellType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
                "openminds.controlled_terms.SubcellularEntity",
                "openminds.controlled_terms.UBERONParcellation",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:anatomicalLocation",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "biological_sexes",
            "openminds.controlled_terms.BiologicalSex",
            "vocab:biologicalSex",
            multiple=True,
            doc="Differentiation of individuals of most species (animals and plants) based on the type of gametes they produce.",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the tissue sample collection within a particular product.",
        ),
        Property(
            "lateralities",
            "openminds.controlled_terms.Laterality",
            "vocab:laterality",
            multiple=True,
            doc="Differentiation between a pair of lateral homologous parts of the body.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property("number_of_tissue_samples", int, "vocab:numberOfTissueSamples", doc="no description available"),
        Property(
            "origins",
            [
                "openminds.controlled_terms.CellType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
            ],
            "vocab:origin",
            multiple=True,
            required=True,
            doc="Source at which something begins or rises, or from which something derives.",
        ),
        Property(
            "species",
            ["openminds.controlled_terms.Species", "openminds.core.Strain"],
            "vocab:species",
            multiple=True,
            required=True,
            doc="Category of biological classification comprising related organisms or populations potentially capable of interbreeding, and being designated by a binomial that consists of the name of a genus followed by a Latin or latinized uncapitalized noun or adjective.",
        ),
        Property(
            "studied_states",
            "openminds.core.TissueSampleCollectionState",
            "vocab:studiedState",
            multiple=True,
            required=True,
            doc="Reference to a point in time at which the tissue sample collection was studied in a particular mode or condition.",
        ),
        Property(
            "types",
            "openminds.controlled_terms.TissueSampleType",
            "vocab:type",
            multiple=True,
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
    ]
    reverse_properties = [
        Property(
            "has_parts",
            "openminds.core.TissueSample",
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
        Property(
            "has_study_results_in",
            "openminds.core.DatasetVersion",
            "^vocab:studiedSpecimen",
            reverse="studied_specimens",
            multiple=True,
            doc="reverse of 'studiedSpecimen'",
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
            ["openminds.sands.BrainAtlasVersion", "openminds.sands.CommonCoordinateSpaceVersion"],
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
        anatomical_locations=None,
        biological_sexes=None,
        has_parts=None,
        has_study_results_in=None,
        internal_identifier=None,
        is_used_to_group=None,
        lateralities=None,
        number_of_tissue_samples=None,
        origins=None,
        species=None,
        studied_states=None,
        types=None,
        used_in=None,
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
            anatomical_locations=anatomical_locations,
            biological_sexes=biological_sexes,
            has_parts=has_parts,
            has_study_results_in=has_study_results_in,
            internal_identifier=internal_identifier,
            is_used_to_group=is_used_to_group,
            lateralities=lateralities,
            number_of_tissue_samples=number_of_tissue_samples,
            origins=origins,
            species=species,
            studied_states=studied_states,
            types=types,
            used_in=used_in,
        )
