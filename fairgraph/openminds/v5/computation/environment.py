"""
Structured information on the computer system or set of systems in which a computation is deployed and executed.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.computation import Environment as OMEnvironment
from fairgraph import KGObject


class Environment(KGObject, OMEnvironment):
    """
    Structured information on the computer system or set of systems in which a computation is deployed and executed.
    """

    type_ = "https://openminds.om-i.org/types/Environment"
    default_space = "computation"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "used_for",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.SoftwareAgent",
                "openminds.v5.computation.Visualization",
            ],
            "environment",
            reverse="environment",
            multiple=True,
            description="reverse of 'environment'",
        ),
    ]
    existence_query_properties = ("hardware", "name")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        configuration=None,
        description=None,
        hardware=None,
        software=None,
        used_for=None,
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
            configuration=configuration,
            description=description,
            hardware=hardware,
            software=software,
            used_for=used_for,
        )
