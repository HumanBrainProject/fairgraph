"""
<description not available>
"""

# this file was auto-generated

from fairgraph import EmbeddedMetadata, IRI
from fairgraph.fields import Field


class AnatomicalTargetPosition(EmbeddedMetadata):
    """
    <description not available>
    """

    type_ = ["https://openminds.ebrains.eu/sands/AnatomicalTargetPosition"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Field(
            "anatomical_targets",
            [
                "openminds.controlledterms.CellType",
                "openminds.controlledterms.Organ",
                "openminds.controlledterms.OrganismSubstance",
                "openminds.controlledterms.SubcellularEntity",
                "openminds.controlledterms.UBERONParcellation",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:anatomicalTarget",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Field(
            "spatial_locations",
            "openminds.sands.CoordinatePoint",
            "vocab:spatialLocation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "target_identification_type",
            "openminds.controlledterms.AnatomicalIdentificationType",
            "vocab:targetIdentificationType",
            required=True,
            doc="no description available",
        ),
    ]

    def __init__(
        self,
        additional_remarks=None,
        anatomical_targets=None,
        spatial_locations=None,
        target_identification_type=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            data=data,
            additional_remarks=additional_remarks,
            anatomical_targets=anatomical_targets,
            spatial_locations=spatial_locations,
            target_identification_type=target_identification_type,
        )
