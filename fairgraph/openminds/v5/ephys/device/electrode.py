"""
Structured information on an electrode.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.ephys import Electrode as OMElectrode
from fairgraph import KGObject


class Electrode(KGObject, OMElectrode):
    """
    Structured information on an electrode.
    """

    type_ = "https://openminds.om-i.org/types/Electrode"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_part_of",
            "openminds.v5.core.Setup",
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "usage",
            "openminds.v5.ephys.ElectrodeUsage",
            "device",
            reverse="device",
            multiple=True,
            description="reverse of 'device'",
        ),
    ]
    existence_query_properties = ("contributions", "name", "type")

    def __init__(
        self,
        name=None,
        conductor_material=None,
        contributions=None,
        description=None,
        insulator_material=None,
        internal_identifier=None,
        intrinsic_resistance=None,
        is_part_of=None,
        serial_number=None,
        type=None,
        usage=None,
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
            name=name,
            conductor_material=conductor_material,
            contributions=contributions,
            description=description,
            insulator_material=insulator_material,
            internal_identifier=internal_identifier,
            intrinsic_resistance=intrinsic_resistance,
            is_part_of=is_part_of,
            serial_number=serial_number,
            type=type,
            usage=usage,
        )
