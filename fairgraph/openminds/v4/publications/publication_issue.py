"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.publications import PublicationIssue as OMPublicationIssue
from fairgraph import KGObject


class PublicationIssue(KGObject, OMPublicationIssue):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/PublicationIssue"
    default_space = "livepapers"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "has_parts",
            "openminds.v4.publications.ScholarlyArticle",
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
    ]
    existence_query_properties = ("is_part_of", "issue_number")

    def __init__(
        self, has_parts=None, is_part_of=None, issue_number=None, id=None, data=None, space=None, release_status=None
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            has_parts=has_parts,
            is_part_of=is_part_of,
            issue_number=issue_number,
        )
