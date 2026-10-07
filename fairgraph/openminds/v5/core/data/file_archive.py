"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import FileArchive as OMFileArchive
from fairgraph import KGObject


from openminds import IRI


class FileArchive(KGObject, OMFileArchive):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/FileArchive"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_location_of",
            "openminds.v5.core.ServiceLink",
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
            ],
            "output",
            reverse="outputs",
            multiple=True,
            description="reverse of 'outputs'",
        ),
    ]
    existence_query_properties = ("iri", "format")

    def __init__(
        self,
        format=None,
        iri=None,
        is_location_of=None,
        is_output_of=None,
        source_data=None,
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
            format=format,
            iri=iri,
            is_location_of=is_location_of,
            is_output_of=is_output_of,
            source_data=source_data,
        )
