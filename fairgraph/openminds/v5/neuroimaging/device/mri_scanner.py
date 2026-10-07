"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.neuroimaging import MRIScanner as OMMRIScanner
from fairgraph import KGObject


class MRIScanner(KGObject, OMMRIScanner):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/MRIScanner"
    default_space = "in-depth"
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
            "openminds.v5.neuroimaging.MRIScannerUsage",
            "device",
            reverse="device",
            multiple=True,
            description="reverse of 'device'",
        ),
    ]
    existence_query_properties = ("contributions", "magnetic_field_strength", "name", "type")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        contributions=None,
        description=None,
        internal_identifier=None,
        is_part_of=None,
        magnetic_field_strength=None,
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
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            magnetic_field_strength=magnetic_field_strength,
            serial_number=serial_number,
            type=type,
            usage=usage,
        )
