"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.publications import Periodical as OMPeriodical
from fairgraph import KGObject


class Periodical(KGObject, OMPeriodical):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Periodical"
    default_space = "livepapers"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_parts",
            "openminds.v4.publications.PublicationVolume",
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
    ]
    existence_query_properties = ("abbreviation",)
    sort_property = "name"

    def __init__(
        self,
        name=None,
        abbreviation=None,
        digital_identifier=None,
        has_parts=None,
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
            abbreviation=abbreviation,
            digital_identifier=digital_identifier,
            has_parts=has_parts,
        )
