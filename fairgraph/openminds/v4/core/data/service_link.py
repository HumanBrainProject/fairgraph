"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ServiceLink as OMServiceLink
from fairgraph import KGObject


from openminds import IRI


class ServiceLink(KGObject, OMServiceLink):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ServiceLink"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("data_location", "open_data_in", "service")

    def __init__(
        self,
        data_location=None,
        display_label=None,
        open_data_in=None,
        preview_image=None,
        service=None,
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
            data_location=data_location,
            display_label=display_label,
            open_data_in=open_data_in,
            preview_image=preview_image,
            service=service,
        )
