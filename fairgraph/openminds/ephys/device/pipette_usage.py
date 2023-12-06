"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class PipetteUsage(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/ephys/PipetteUsage"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "anatomical_location",
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
            "vocab:anatomicalLocation",
            doc="no description available",
        ),
        Field(
            "chloride_reversal_potentials",
            "openminds.core.Measurement",
            "vocab:chlorideReversalPotential",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "compensation_current",
            "openminds.core.Measurement",
            "vocab:compensationCurrent",
            doc="no description available",
        ),
        Field(
            "device",
            "openminds.ephys.Pipette",
            "vocab:device",
            required=True,
            doc="Piece of equipment or mechanism (hardware) designed to serve a special purpose or perform a special function.",
        ),
        Field(
            "end_membrane_potential",
            "openminds.core.Measurement",
            "vocab:endMembranePotential",
            doc="no description available",
        ),
        Field(
            "holding_potential", "openminds.core.Measurement", "vocab:holdingPotential", doc="no description available"
        ),
        Field(
            "input_resistance", "openminds.core.Measurement", "vocab:inputResistance", doc="no description available"
        ),
        Field(
            "labeling_compound",
            [
                "openminds.chemicals.ChemicalMixture",
                "openminds.chemicals.ChemicalSubstance",
                "openminds.controlledterms.MolecularEntity",
            ],
            "vocab:labelingCompound",
            doc="no description available",
        ),
        Field(
            "liquid_junction_potential",
            "openminds.core.Measurement",
            "vocab:liquidJunctionPotential",
            doc="no description available",
        ),
        Field(
            "metadata_locations",
            ["openminds.core.File", "openminds.core.FileBundle"],
            "vocab:metadataLocation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "pipette_resistance",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:pipetteResistance",
            doc="no description available",
        ),
        Field(
            "pipette_solution",
            "openminds.chemicals.ChemicalMixture",
            "vocab:pipetteSolution",
            required=True,
            doc="no description available",
        ),
        Field("seal_resistance", "openminds.core.Measurement", "vocab:sealResistance", doc="no description available"),
        Field(
            "series_resistance", "openminds.core.Measurement", "vocab:seriesResistance", doc="no description available"
        ),
        Field(
            "spatial_location",
            "openminds.sands.CoordinatePoint",
            "vocab:spatialLocation",
            doc="no description available",
        ),
        Field(
            "start_membrane_potential",
            "openminds.core.Measurement",
            "vocab:startMembranePotential",
            doc="no description available",
        ),
        Field(
            "used_specimen",
            ["openminds.core.SubjectState", "openminds.core.TissueSampleState"],
            "vocab:usedSpecimen",
            doc="no description available",
        ),
        Field(
            "generation_device",
            "openminds.stimulation.EphysStimulus",
            "^vocab:generatedBy",
            reverse="generated_by",
            multiple=True,
            doc="reverse of 'generatedBy'",
        ),
        Field(
            "placed_by",
            "openminds.ephys.ElectrodePlacement",
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
        Field(
            "used_in",
            ["openminds.ephys.CellPatching", "openminds.ephys.RecordingActivity"],
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
        Field(
            "used_to_measure",
            "openminds.core.Measurement",
            "^vocab:measuredWith",
            reverse="measured_with",
            multiple=True,
            doc="reverse of 'measuredWith'",
        ),
        Field(
            "used_to_record",
            "openminds.ephys.Recording",
            "^vocab:recordedWith",
            reverse="recorded_with",
            multiple=True,
            doc="reverse of 'recordedWith'",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        anatomical_location=None,
        chloride_reversal_potentials=None,
        compensation_current=None,
        device=None,
        end_membrane_potential=None,
        holding_potential=None,
        input_resistance=None,
        labeling_compound=None,
        liquid_junction_potential=None,
        metadata_locations=None,
        pipette_resistance=None,
        pipette_solution=None,
        seal_resistance=None,
        series_resistance=None,
        spatial_location=None,
        start_membrane_potential=None,
        used_specimen=None,
        generation_device=None,
        placed_by=None,
        used_in=None,
        used_to_measure=None,
        used_to_record=None,
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
            anatomical_location=anatomical_location,
            chloride_reversal_potentials=chloride_reversal_potentials,
            compensation_current=compensation_current,
            device=device,
            end_membrane_potential=end_membrane_potential,
            holding_potential=holding_potential,
            input_resistance=input_resistance,
            labeling_compound=labeling_compound,
            liquid_junction_potential=liquid_junction_potential,
            metadata_locations=metadata_locations,
            pipette_resistance=pipette_resistance,
            pipette_solution=pipette_solution,
            seal_resistance=seal_resistance,
            series_resistance=series_resistance,
            spatial_location=spatial_location,
            start_membrane_potential=start_membrane_potential,
            used_specimen=used_specimen,
            generation_device=generation_device,
            placed_by=placed_by,
            used_in=used_in,
            used_to_measure=used_to_measure,
            used_to_record=used_to_record,
        )
