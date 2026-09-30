"""
<description not available>
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import ServiceDeployment as OMServiceDeployment
from fairgraph import KGObject


from datetime import datetime


class ServiceDeployment(KGObject, OMServiceDeployment):
    """
    <description not available>
    """

    type_ = "https://openminds.om-i.org/types/ServiceDeployment"
    default_space = "computation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = []
    existence_query_properties = ("name", "provides", "service", "start_time")

    def __init__(
        self,
        name=None,
        depends_on=None,
        deployment_type=None,
        end_time=None,
        provides=None,
        service=None,
        start_time=None,
        uses=None,
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
            depends_on=depends_on,
            deployment_type=deployment_type,
            end_time=end_time,
            provides=provides,
            service=service,
            start_time=start_time,
            uses=uses,
        )
