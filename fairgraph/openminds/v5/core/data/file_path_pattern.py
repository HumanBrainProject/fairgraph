"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import FilePathPattern as OMFilePathPattern
from fairgraph import KGEmbedded


class FilePathPattern(KGEmbedded, OMFilePathPattern):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/FilePathPattern"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("grouping_types", "regex")

    def __init__(self, grouping_types=None, regex=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, grouping_types=grouping_types, regex=regex)
