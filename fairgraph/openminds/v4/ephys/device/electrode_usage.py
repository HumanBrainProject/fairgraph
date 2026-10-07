"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.ephys import ElectrodeUsage as OMElectrodeUsage
from fairgraph import KGObject


class ElectrodeUsage(KGObject, OMElectrodeUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ElectrodeUsage"
    default_space = "in-depth"
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
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        anatomical_location=None,
        contact_resistance=None,
        device=None,
        generation_device=None,
        metadata_locations=None,
        placed_by=None,
        spatial_location=None,
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
            contact_resistance=contact_resistance,
            device=device,
            generation_device=generation_device,
            metadata_locations=metadata_locations,
            placed_by=placed_by,
            spatial_location=spatial_location,
            used_in=used_in,
            used_specimen=used_specimen,
            used_to_measure=used_to_measure,
            used_to_record=used_to_record,
        )
