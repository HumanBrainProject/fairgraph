"""
Structured information about the launch of a computational process.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class LaunchConfiguration(KGObject):
    """
    Structured information about the launch of a computational process.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/LaunchConfiguration"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("arguments", str, "vocab:argument", multiple=True, doc="no description available"),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the launch configuration.",
        ),
        Property(
            "environment_variables",
            "openminds.core.PropertyValueList",
            "vocab:environmentVariable",
            doc="no description available",
        ),
        Property("executable", str, "vocab:executable", required=True, doc="no description available"),
        Property(
            "name",
            str,
            "vocab:name",
            doc="Word or phrase that constitutes the distinctive designation of the launch configuration.",
        ),
    ]
    reverse_properties = [
        Property(
            "is_launch_configuration_of",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "^vocab:launchConfiguration",
            reverse="launch_configurations",
            multiple=True,
            doc="reverse of 'launchConfiguration'",
        ),
    ]
    existence_query_properties = ("executable", "name")

    def __init__(
        self,
        name=None,
        arguments=None,
        description=None,
        environment_variables=None,
        executable=None,
        is_launch_configuration_of=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            arguments=arguments,
            description=description,
            environment_variables=environment_variables,
            executable=executable,
            is_launch_configuration_of=is_launch_configuration_of,
        )
