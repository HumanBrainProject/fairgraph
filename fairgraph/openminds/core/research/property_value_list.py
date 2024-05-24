"""
An identifiable list of property-value pairs.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class PropertyValueList(KGObject):
    """
    An identifiable list of property-value pairs.
    """

    default_space = "dataset"
    type_ = "https://openminds.ebrains.eu/core/PropertyValueList"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "property_value_pairs",
            ["openminds.core.NumericalProperty", "openminds.core.StringProperty"],
            "vocab:propertyValuePair",
            multiple=True,
            required=True,
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
            "defines_environment_of",
            "openminds.computation.LaunchConfiguration",
            "^vocab:environmentVariable",
            reverse="environment_variables",
            multiple=True,
            doc="reverse of 'environmentVariable'",
        ),
        Property(
            "is_configuration_of",
            "openminds.computation.ValidationTestVersion",
            "^vocab:configuration",
            reverse="configurations",
            multiple=True,
            doc="reverse of 'configuration'",
        ),
        Property(
            "specifies",
            ["openminds.sands.CustomAnnotation", "openminds.stimulation.EphysStimulus"],
            "^vocab:specification",
            reverse="specifications",
            multiple=True,
            doc="reverse of 'specification'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        defines_environment_of=None,
        is_configuration_of=None,
        property_value_pairs=None,
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
            defines_environment_of=defines_environment_of,
            is_configuration_of=is_configuration_of,
            property_value_pairs=property_value_pairs,
            specifies=specifies,
        )
