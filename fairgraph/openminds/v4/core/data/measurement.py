"""
Structured information about a measurement performed during a scientific experiment.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import Measurement as OMMeasurement
from fairgraph import KGEmbedded


from datetime import datetime


class Measurement(KGEmbedded, OMMeasurement):
    """
    Structured information about a measurement performed during a scientific experiment.
    """

    type_ = "https://openminds.om-i.org/types/Measurement"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("measured_quantity", "values")

    def __init__(
        self,
        additional_remarks=None,
        measured_quantity=None,
        measured_with=None,
        timestamp=None,
        values=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            additional_remarks=additional_remarks,
            measured_quantity=measured_quantity,
            measured_with=measured_with,
            timestamp=timestamp,
            values=values,
        )
