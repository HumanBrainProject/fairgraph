"""
An identifiable list of property-value pairs.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.core import PropertyValueList as OMPropertyValueList
from fairgraph import KGObject


class PropertyValueList(KGObject, OMPropertyValueList):
    """
    An identifiable list of property-value pairs.
    """

    type_ = "https://openminds.om-i.org/types/PropertyValueList"
    default_space = "dataset"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "defines_environment_of",
            "openminds.v4.computation.LaunchConfiguration",
            "environmentVariable",
            reverse="environment_variable",
            multiple=True,
            description="reverse of 'environment_variable'",
        ),
        Property(
            "is_configuration_of",
            "openminds.v4.computation.ValidationTestVersion",
            "configuration",
            reverse="configuration",
            multiple=True,
            description="reverse of 'configuration'",
        ),
        Property(
            "specifies",
            ["openminds.v4.sands.CustomAnnotation", "openminds.v4.stimulation.EphysStimulus"],
            "specification",
            reverse="specification",
            multiple=True,
            description="reverse of 'specification'",
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
            data=data,
            lookup_label=lookup_label,
            defines_environment_of=defines_environment_of,
            is_configuration_of=is_configuration_of,
            property_value_pairs=property_value_pairs,
            specifies=specifies,
        )
