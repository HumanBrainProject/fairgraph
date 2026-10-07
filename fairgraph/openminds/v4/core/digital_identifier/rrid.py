"""
A persistent identifier for a research resource provided by the Resource Identification Initiative.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import RRID as OMRRID
from fairgraph import KGObject


class RRID(KGObject, OMRRID):
    """
    A persistent identifier for a research resource provided by the Resource Identification Initiative.
    """

    type_ = "https://openminds.om-i.org/types/RRID"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "identifies",
            [
                "openminds.v4.chemicals.ProductSource",
                "openminds.v4.core.Organization",
                "openminds.v4.core.Software",
                "openminds.v4.core.SoftwareVersion",
                "openminds.v4.core.Strain",
                "openminds.v4.ephys.Electrode",
                "openminds.v4.ephys.ElectrodeArray",
                "openminds.v4.ephys.Pipette",
                "openminds.v4.sands.BrainAtlas",
                "openminds.v4.sands.BrainAtlasVersion",
                "openminds.v4.sands.CommonCoordinateSpace",
                "openminds.v4.sands.CommonCoordinateSpaceVersion",
                "openminds.v4.specimen_prep.SlicingDevice",
            ],
            "digitalIdentifier",
            reverse="digital_identifier",
            multiple=True,
            description="reverse of 'digital_identifier'",
        ),
    ]
    existence_query_properties = ("identifier",)

    def __init__(self, identifier=None, identifies=None, id=None, data=None, space=None, release_status=None):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            identifier=identifier,
            identifies=identifies,
        )
