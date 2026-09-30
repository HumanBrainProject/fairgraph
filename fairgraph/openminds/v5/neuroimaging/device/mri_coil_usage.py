"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.neuroimaging import MRICoilUsage as OMMRICoilUsage
from fairgraph import KGObject


class MRICoilUsage(KGObject, OMMRICoilUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/MRICoilUsage"
    default_space = "in-depth"
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
            ["openminds.v5.ephys.CellPatching", "openminds.v5.neuroimaging.MRIScannerUsage"],
            ["device", "usedCoils"],
            reverse=["devices", "used_coils"],
            multiple=True,
            description="reverse of devices, used_coils",
        ),
    ]
    existence_query_properties = ("lookup_label",)
    sort_property = "lookup_label"

    def __init__(
        self,
        lookup_label=None,
        active_elements=None,
        device=None,
        generation_device=None,
        is_used_to_obtain=None,
        metadata_locations=None,
        mounting_location=None,
        placed_by=None,
        signal_directionality=None,
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
            active_elements=active_elements,
            device=device,
            generation_device=generation_device,
            is_used_to_obtain=is_used_to_obtain,
            metadata_locations=metadata_locations,
            mounting_location=mounting_location,
            placed_by=placed_by,
            signal_directionality=signal_directionality,
            used_in=used_in,
            used_specimen=used_specimen,
        )
