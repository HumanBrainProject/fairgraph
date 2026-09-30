"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import AtlasAnnotation as OMAtlasAnnotation
from fairgraph import KGEmbedded


class AtlasAnnotation(KGEmbedded, OMAtlasAnnotation):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/AtlasAnnotation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("criteria_quality_type", "criteria_type", "type")

    def __init__(
        self,
        criteria=None,
        criteria_quality_type=None,
        criteria_type=None,
        inspired_by=None,
        internal_identifier=None,
        lateralities=None,
        preferred_visualization=None,
        specification=None,
        type=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            criteria=criteria,
            criteria_quality_type=criteria_quality_type,
            criteria_type=criteria_type,
            inspired_by=inspired_by,
            internal_identifier=internal_identifier,
            lateralities=lateralities,
            preferred_visualization=preferred_visualization,
            specification=specification,
            type=type,
        )
