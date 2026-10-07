"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.ephys import PipetteUsage as OMPipetteUsage
from fairgraph import KGObject


class PipetteUsage(KGObject, OMPipetteUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/PipetteUsage"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "generation_device",
            "openminds.v4.stimulation.EphysStimulus",
            "generatedBy",
            reverse="generated_by",
            multiple=True,
            description="reverse of 'generated_by'",
        ),
        Property(
            "placed_by",
            "openminds.v4.ephys.ElectrodePlacement",
            "device",
            reverse="devices",
            multiple=True,
            description="reverse of 'devices'",
        ),
        Property(
            "used_in",
            ["openminds.v4.ephys.CellPatching", "openminds.v4.ephys.RecordingActivity"],
            "device",
            reverse="devices",
            multiple=True,
            description="reverse of 'devices'",
        ),
        Property(
            "used_to_measure",
            "openminds.v4.core.Measurement",
            "measuredWith",
            reverse="measured_with",
            multiple=True,
            description="reverse of 'measured_with'",
        ),
        Property(
            "used_to_record",
            "openminds.v4.ephys.Recording",
            "recordedWith",
            reverse="recorded_with",
            multiple=True,
            description="reverse of 'recorded_with'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        anatomical_location=None,
        chloride_reversal_potentials=None,
        compensation_current=None,
        device=None,
        end_membrane_potential=None,
        generation_device=None,
        holding_potential=None,
        input_resistance=None,
        labeling_compound=None,
        liquid_junction_potential=None,
        metadata_locations=None,
        pipette_resistance=None,
        pipette_solution=None,
        placed_by=None,
        seal_resistance=None,
        series_resistance=None,
        spatial_location=None,
        start_membrane_potential=None,
        used_in=None,
        used_specimen=None,
        used_to_measure=None,
        used_to_record=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            lookup_label=lookup_label,
            anatomical_location=anatomical_location,
            chloride_reversal_potentials=chloride_reversal_potentials,
            compensation_current=compensation_current,
            device=device,
            end_membrane_potential=end_membrane_potential,
            generation_device=generation_device,
            holding_potential=holding_potential,
            input_resistance=input_resistance,
            labeling_compound=labeling_compound,
            liquid_junction_potential=liquid_junction_potential,
            metadata_locations=metadata_locations,
            pipette_resistance=pipette_resistance,
            pipette_solution=pipette_solution,
            placed_by=placed_by,
            seal_resistance=seal_resistance,
            series_resistance=series_resistance,
            spatial_location=spatial_location,
            start_membrane_potential=start_membrane_potential,
            used_in=used_in,
            used_specimen=used_specimen,
            used_to_measure=used_to_measure,
            used_to_record=used_to_record,
        )
