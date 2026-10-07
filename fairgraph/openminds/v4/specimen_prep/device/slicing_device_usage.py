"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.specimen_prep import SlicingDeviceUsage as OMSlicingDeviceUsage
from fairgraph import KGObject


class SlicingDeviceUsage(KGObject, OMSlicingDeviceUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/SlicingDeviceUsage"
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
            "used_for",
            "openminds.v4.specimen_prep.TissueSampleSlicing",
            "device",
            reverse="device",
            multiple=True,
            description="reverse of 'device'",
        ),
        Property(
            "used_in",
            "openminds.v4.ephys.CellPatching",
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
        device=None,
        generation_device=None,
        metadata_locations=None,
        oscillation_amplitude=None,
        placed_by=None,
        slice_thickness=None,
        slicing_angles=None,
        slicing_plane=None,
        slicing_speed=None,
        used_for=None,
        used_in=None,
        used_specimen=None,
        used_to_measure=None,
        used_to_record=None,
        vibration_frequency=None,
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
            device=device,
            generation_device=generation_device,
            metadata_locations=metadata_locations,
            oscillation_amplitude=oscillation_amplitude,
            placed_by=placed_by,
            slice_thickness=slice_thickness,
            slicing_angles=slicing_angles,
            slicing_plane=slicing_plane,
            slicing_speed=slicing_speed,
            used_for=used_for,
            used_in=used_in,
            used_specimen=used_specimen,
            used_to_measure=used_to_measure,
            used_to_record=used_to_record,
            vibration_frequency=vibration_frequency,
        )
