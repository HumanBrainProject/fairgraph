"""
Structured information on a tissue sample.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class TissueSample(KGObject):
    """
    Structured information on a tissue sample.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/TissueSample"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
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
            "biological_sex",
            "openminds.controlled_terms.BiologicalSex",
            "vocab:biologicalSex",
            doc="Differentiation of individuals of most species (animals and plants) based on the type of gametes they produce.",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the tissue sample within a particular product.",
        ),
        Property(
            "is_part_of",
            "openminds.core.TissueSampleCollection",
            "vocab:isPartOf",
            multiple=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Property(
            "lateralities",
            "openminds.controlled_terms.Laterality",
            "vocab:laterality",
            multiple=True,
            doc="Differentiation between a pair of lateral homologous parts of the body.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "origin",
            [
                "openminds.controlled_terms.CellType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
            ],
            "vocab:origin",
            required=True,
            doc="Source at which something begins or rises, or from which something derives.",
        ),
        Property(
            "species",
            ["openminds.controlled_terms.Species", "openminds.core.Strain"],
            "vocab:species",
            required=True,
            doc="Category of biological classification comprising related organisms or populations potentially capable of interbreeding, and being designated by a binomial that consists of the name of a genus followed by a Latin or latinized uncapitalized noun or adjective.",
        ),
        Property(
            "studied_states",
            "openminds.core.TissueSampleState",
            "vocab:studiedState",
            multiple=True,
            required=True,
            doc="Reference to a point in time at which the tissue sample was studied in a particular mode or condition.",
        ),
        Property(
            "type",
            "openminds.controlled_terms.TissueSampleType",
            "vocab:type",
            required=True,
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
    ]
    reverse_properties = [
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
        anatomical_locations=None,
        biological_sex=None,
        has_study_results_in=None,
        internal_identifier=None,
        is_part_of=None,
        is_used_to_group=None,
        lateralities=None,
        origin=None,
        species=None,
        studied_states=None,
        type=None,
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
            anatomical_locations=anatomical_locations,
            biological_sex=biological_sex,
            has_study_results_in=has_study_results_in,
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            is_used_to_group=is_used_to_group,
            lateralities=lateralities,
            origin=origin,
            species=species,
            studied_states=studied_states,
            type=type,
            used_in=used_in,
        )
