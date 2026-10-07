"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import ResearchProductGroup as OMResearchProductGroup
from fairgraph import KGObject


class ResearchProductGroup(KGObject, OMResearchProductGroup):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ResearchProductGroup"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("context", "has_parts")

    def __init__(self, context=None, has_parts=None, id=None, data=None, space=None, release_status=None):
        return KGObject.__init__(
            self, id=id, space=space, release_status=release_status, data=data, context=context, has_parts=has_parts
        )
