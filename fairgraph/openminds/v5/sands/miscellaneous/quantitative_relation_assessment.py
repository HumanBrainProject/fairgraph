"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.sands import QuantitativeRelationAssessment as OMQuantitativeRelationAssessment
from fairgraph import KGEmbedded


class QuantitativeRelationAssessment(KGEmbedded, OMQuantitativeRelationAssessment):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/QuantitativeRelationAssessment"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("in_relation_to", "quantitative_overlap")

    def __init__(
        self,
        criteria=None,
        in_relation_to=None,
        quantitative_overlap=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            criteria=criteria,
            in_relation_to=in_relation_to,
            quantitative_overlap=quantitative_overlap,
        )
