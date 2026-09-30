"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.ephys import Pipette as OMPipette
from fairgraph import KGObject


class Pipette(KGObject, OMPipette):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Pipette"
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
            "openminds.v5.ephys.PipetteUsage",
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
        contributions=None,
        description=None,
        external_diameter=None,
        internal_diameter=None,
        internal_identifier=None,
        is_part_of=None,
        material=None,
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
            contributions=contributions,
            description=description,
            external_diameter=external_diameter,
            internal_diameter=internal_diameter,
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            material=material,
            serial_number=serial_number,
            type=type,
            usage=usage,
        )
