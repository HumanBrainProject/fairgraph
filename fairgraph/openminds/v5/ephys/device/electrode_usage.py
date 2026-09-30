"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.ephys import ElectrodeUsage as OMElectrodeUsage
from fairgraph import KGObject


class ElectrodeUsage(KGObject, OMElectrodeUsage):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ElectrodeUsage"
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
        contact_resistance=None,
        device=None,
        generation_device=None,
        is_used_to_obtain=None,
        metadata_locations=None,
        placed_by=None,
        spatial_location=None,
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
            contact_resistance=contact_resistance,
            device=device,
            generation_device=generation_device,
            is_used_to_obtain=is_used_to_obtain,
            metadata_locations=metadata_locations,
            placed_by=placed_by,
            spatial_location=spatial_location,
            used_in=used_in,
            used_specimen=used_specimen,
        )
