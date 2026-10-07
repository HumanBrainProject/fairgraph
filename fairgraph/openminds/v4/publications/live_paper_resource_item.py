"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.publications import LivePaperResourceItem as OMLivePaperResourceItem
from fairgraph import KGObject


from openminds import IRI


class LivePaperResourceItem(KGObject, OMLivePaperResourceItem):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/LivePaperResourceItem"
    default_space = "livepapers"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_location_of",
            "openminds.v4.core.ServiceLink",
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
    ]
    existence_query_properties = ("name", "iri", "is_part_of")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        hosted_by=None,
        iri=None,
        is_location_of=None,
        is_part_of=None,
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
            hosted_by=hosted_by,
            iri=iri,
            is_location_of=is_location_of,
            is_part_of=is_part_of,
        )
