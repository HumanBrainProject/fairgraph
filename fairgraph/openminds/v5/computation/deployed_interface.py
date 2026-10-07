"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import DeployedInterface as OMDeployedInterface
from fairgraph import KGEmbedded


class DeployedInterface(KGEmbedded, OMDeployedInterface):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/DeployedInterface"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("accessibility", "entry_point", "interface")

    def __init__(
        self, accessibility=None, entry_point=None, interface=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, accessibility=accessibility, entry_point=entry_point, interface=interface
        )
