"""
Structured information about the launch of a computational process.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.computation import LaunchConfiguration as OMLaunchConfiguration
from fairgraph import KGObject


class LaunchConfiguration(KGObject, OMLaunchConfiguration):
    """
    Structured information about the launch of a computational process.
    """

    type_ = "https://openminds.om-i.org/types/LaunchConfiguration"
    default_space = "computation"
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "is_launch_configuration_of",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.Visualization",
            ],
            "launchConfiguration",
            reverse="launch_configuration",
            multiple=True,
            description="reverse of 'launch_configuration'",
        ),
    ]
    aliases = {"environment_variables": "environment_variable"}
    existence_query_properties = ("executable", "name")
    sort_property = "name"

    def __init__(
        self,
        name=None,
        arguments=None,
        description=None,
        environment_variable=None,
        environment_variables=None,
        executable=None,
        is_launch_configuration_of=None,
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
            arguments=arguments,
            description=description,
            environment_variable=environment_variable,
            environment_variables=environment_variables,
            executable=executable,
            is_launch_configuration_of=is_launch_configuration_of,
        )
