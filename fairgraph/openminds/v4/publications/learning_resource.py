"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.publications import LearningResource as OMLearningResource
from fairgraph import KGObject


from datetime import date
from openminds import IRI


class LearningResource(KGObject, OMLearningResource):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/LearningResource"
    default_space = "livepapers"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("about", "name", "publication_date")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        about=None,
        abstract=None,
        authors=None,
        cited_publications=None,
        copyright=None,
        creation_date=None,
        custodians=None,
        digital_identifier=None,
        editors=None,
        educational_level=None,
        funding=None,
        iri=None,
        keywords=None,
        learning_outcome=None,
        license=None,
        modification_date=None,
        order=None,
        prerequisite=None,
        publication_date=None,
        publisher=None,
        required_time=None,
        topic=None,
        type=None,
        version_identifier=None,
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
            about=about,
            abstract=abstract,
            authors=authors,
            cited_publications=cited_publications,
            copyright=copyright,
            creation_date=creation_date,
            custodians=custodians,
            digital_identifier=digital_identifier,
            editors=editors,
            educational_level=educational_level,
            funding=funding,
            iri=iri,
            keywords=keywords,
            learning_outcome=learning_outcome,
            license=license,
            modification_date=modification_date,
            order=order,
            prerequisite=prerequisite,
            publication_date=publication_date,
            publisher=publisher,
            required_time=required_time,
            topic=topic,
            type=type,
            version_identifier=version_identifier,
        )
