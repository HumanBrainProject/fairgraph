"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import Kite as OMKite
from fairgraph import KGEmbedded


class Kite(KGEmbedded, OMKite):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Kite"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("leg_lengths", "symmetry_diagonal_length")

    def __init__(
        self, leg_lengths=None, symmetry_diagonal_length=None, id=None, data=None, space=None, release_status=None
    ):
        return KGEmbedded.__init__(
            self, data=data, leg_lengths=leg_lengths, symmetry_diagonal_length=symmetry_diagonal_length
        )
