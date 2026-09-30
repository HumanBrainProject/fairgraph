"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import HardwareProduct as OMHardwareProduct
from fairgraph import KGObject


class HardwareProduct(KGObject, OMHardwareProduct):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/HardwareProduct"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_type_of",
            [
                "openminds.v5.ephys.Electrode",
                "openminds.v5.ephys.ElectrodeArray",
                "openminds.v5.ephys.Pipette",
                "openminds.v5.neuroimaging.MRICoil",
                "openminds.v5.neuroimaging.MRIScanner",
                "openminds.v5.specimen_prep.SlicingDevice",
            ],
            "type",
            reverse="type",
            multiple=True,
            description="reverse of 'type'",
        ),
    ]
    existence_query_properties = ("contributions", "name", "scopes", "type")

    def __init__(
        self,
        name=None,
        contributions=None,
        copyright=None,
        description=None,
        digital_identifier=None,
        is_type_of=None,
        keywords=None,
        scopes=None,
        specification=None,
        type=None,
        usage_conditions=None,
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
            copyright=copyright,
            description=description,
            digital_identifier=digital_identifier,
            is_type_of=is_type_of,
            keywords=keywords,
            scopes=scopes,
            specification=specification,
            type=type,
            usage_conditions=usage_conditions,
        )
