"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import RegularTimeSeries as OMRegularTimeSeries
from fairgraph import KGObject


class RegularTimeSeries(KGObject, OMRegularTimeSeries):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/RegularTimeSeries"
    default_space = "in-depth"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "next_regular_time_series",
            "openminds.v5.core.RegularTimeSeries",
            "previousRegularTimeSeries",
            reverse="previous_regular_time_series",
            multiple=True,
            description="reverse of 'previous_regular_time_series'",
        ),
    ]
    existence_query_properties = ("channels", "data_location", "sampling_frequency")

    def __init__(
        self,
        name=None,
        additional_remarks=None,
        channels=None,
        data_location=None,
        internal_identifier=None,
        next_regular_time_series=None,
        obtained_with=None,
        previous_regular_time_series=None,
        sampling_frequency=None,
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
            additional_remarks=additional_remarks,
            channels=channels,
            data_location=data_location,
            internal_identifier=internal_identifier,
            next_regular_time_series=next_regular_time_series,
            obtained_with=obtained_with,
            previous_regular_time_series=previous_regular_time_series,
            sampling_frequency=sampling_frequency,
        )
