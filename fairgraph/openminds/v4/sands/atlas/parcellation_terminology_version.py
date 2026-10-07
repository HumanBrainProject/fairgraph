"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.sands import ParcellationTerminologyVersion as OMParcellationTerminologyVersion
from fairgraph import KGEmbedded


class ParcellationTerminologyVersion(KGEmbedded, OMParcellationTerminologyVersion):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ParcellationTerminologyVersion"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("short_name", "version_identifier")

    def __init__(
        self,
        data_locations=None,
        has_entities=None,
        ontology_identifiers=None,
        id=None,
        data=None,
        space=None,
        release_status=None,
    ):
        return KGEmbedded.__init__(
            self,
            data=data,
            data_locations=data_locations,
            has_entities=has_entities,
            ontology_identifiers=ontology_identifiers,
        )
