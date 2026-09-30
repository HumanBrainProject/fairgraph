"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.neuroimaging import MRICoil as OMMRICoil
from fairgraph import KGObject


class MRICoil(KGObject, OMMRICoil):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/MRICoil"
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
            "openminds.v5.neuroimaging.MRICoilUsage",
            "device",
            reverse="device",
            multiple=True,
            description="reverse of 'device'",
        ),
    ]
    existence_query_properties = ("contributions", "element_count", "mounting_type", "name", "type")

    def __init__(
        self,
        name=None,
        contributions=None,
        description=None,
        element_count=None,
        intended_mounting_location=None,
        internal_identifier=None,
        is_part_of=None,
        mounting_type=None,
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
            element_count=element_count,
            intended_mounting_location=intended_mounting_location,
            internal_identifier=internal_identifier,
            is_part_of=is_part_of,
            mounting_type=mounting_type,
            serial_number=serial_number,
            type=type,
            usage=usage,
        )
