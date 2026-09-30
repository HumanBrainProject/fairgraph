"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.ephys import PipetteUsage as OMPipetteUsage
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
            "openminds.v5.stimulation.EphysStimulus",
            "generatedBy",
            reverse="generated_by",
            multiple=True,
            description="reverse of 'generated_by'",
        ),
        Property(
            "is_used_to_obtain",
            [
                "openminds.v5.core.GridImage",
                "openminds.v5.core.GridImageSequence",
                "openminds.v5.core.GridImageStack",
                "openminds.v5.core.GridVolume",
                "openminds.v5.core.GridVolumeSequence",
                "openminds.v5.core.Measurement",
                "openminds.v5.core.RegularTimeSeries",
            ],
            "obtainedWith",
            reverse="obtained_with",
            multiple=True,
            description="reverse of 'obtained_with'",
        ),
        Property(
            "placed_by",
            "openminds.v5.ephys.ElectrodePlacement",
            "device",
            reverse="devices",
            multiple=True,
            description="reverse of 'devices'",
        ),
        Property(
            "used_in",
            ["openminds.v5.ephys.CellPatching", "openminds.v5.ephys.RecordingActivity"],
            "device",
            reverse="devices",
            multiple=True,
            description="reverse of 'devices'",
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
        is_used_to_obtain=None,
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
            is_used_to_obtain=is_used_to_obtain,
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
        )
