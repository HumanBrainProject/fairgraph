"""
Structured information on a research project.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import Project as OMProject
from fairgraph import KGObject


from openminds import IRI


class Project(KGObject, OMProject):
    """
    Structured information on a research project.
    """

    type_ = "https://openminds.om-i.org/types/Project"
    default_space = "common"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    aliases = {"name": "full_name", "alias": "short_name"}
    existence_query_properties = ("short_name",)

    def __init__(
        self,
        name=None,
        alias=None,
        contributions=None,
        description=None,
        full_name=None,
        has_parts=None,
        homepage=None,
        short_name=None,
        type=None,
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
            alias=alias,
            contributions=contributions,
            description=description,
            full_name=full_name,
            has_parts=has_parts,
            homepage=homepage,
            short_name=short_name,
            type=type,
        )
