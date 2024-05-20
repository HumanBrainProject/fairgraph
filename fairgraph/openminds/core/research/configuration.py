"""
Structured information about the properties or parameters of an entity or process.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class Configuration(KGObject):
    """
    Structured information about the properties or parameters of an entity or process.
    """

    default_space = "common"
    type_ = "https://openminds.ebrains.eu/core/Configuration"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("configuration", str, "vocab:configuration", required=True, doc="no description available"),
        Property(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            required=True,
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "is_configuration_of",
            [
                "openminds.computation.Environment",
                "openminds.computation.ValidationTestVersion",
                "openminds.computation.WorkflowExecution",
            ],
            "^vocab:configuration",
            reverse="configurations",
            multiple=True,
            doc="reverse of 'configuration'",
        ),
        Property(
            "specifies",
            "openminds.stimulation.EphysStimulus",
            "^vocab:specification",
            reverse="specifications",
            multiple=True,
            doc="reverse of 'specification'",
        ),
    ]
    existence_query_properties = ("configuration",)

    def __init__(
        self,
        lookup_label=None,
        configuration=None,
        format=None,
        is_configuration_of=None,
        specifies=None,
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
            lookup_label=lookup_label,
            configuration=configuration,
            format=format,
            is_configuration_of=is_configuration_of,
            specifies=specifies,
        )
