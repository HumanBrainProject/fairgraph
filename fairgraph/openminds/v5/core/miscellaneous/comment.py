"""
Structured information about a short text expressing an opinion on, or giving information about some entity.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Comment as OMComment
from fairgraph import KGObject


from datetime import datetime


class Comment(KGObject, OMComment):
    """
    Structured information about a short text expressing an opinion on, or giving information about some entity.
    """

    type_ = "https://openminds.om-i.org/types/Comment"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("about", "comment", "commenter", "timestamp")

    def __init__(
        self,
        about=None,
        comment=None,
        commenter=None,
        timestamp=None,
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
            about=about,
            comment=comment,
            commenter=commenter,
            timestamp=timestamp,
        )
