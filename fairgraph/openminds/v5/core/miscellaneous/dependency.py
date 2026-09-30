"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Dependency as OMDependency
from fairgraph import KGEmbedded


class Dependency(KGEmbedded, OMDependency):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/Dependency"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("fulfilled_by",)

    def __init__(self, failure_impacts=None, fulfilled_by=None, id=None, data=None, space=None, release_status=None):
        return KGEmbedded.__init__(self, data=data, failure_impacts=failure_impacts, fulfilled_by=fulfilled_by)
