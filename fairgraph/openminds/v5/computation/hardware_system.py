"""
Structured information about computing hardware.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import HardwareSystem as OMHardwareSystem
from fairgraph import KGObject


class HardwareSystem(KGObject, OMHardwareSystem):
    """
    Structured information about computing hardware.
    """

    type_ = "https://openminds.om-i.org/types/HardwareSystem"
    default_space = "computation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "used_by",
            "openminds.v5.computation.Environment",
            "hardware",
            reverse="hardware",
            multiple=True,
            description="reverse of 'hardware'",
        ),
    ]
    existence_query_properties = ("name",)

    def __init__(
        self,
        name=None,
        description=None,
        used_by=None,
        version_identifier=None,
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
            description=description,
            used_by=used_by,
            version_identifier=version_identifier,
        )
