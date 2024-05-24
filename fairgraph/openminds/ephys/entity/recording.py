"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class Recording(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = "https://openminds.ebrains.eu/ephys/Recording"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "additional_remarks",
            str,
            "vocab:additionalRemarks",
            doc="Mention of what deserves additional attention or notice.",
        ),
        Property(
            "channels",
            "openminds.ephys.Channel",
            "vocab:channel",
            multiple=True,
            required=True,
            doc="no description available",
        ),
        Property(
            "data_location",
            ["openminds.core.File", "openminds.core.FileBundle"],
            "vocab:dataLocation",
            required=True,
            doc="no description available",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            doc="Term or code that identifies the recording within a particular product.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            doc="Word or phrase that constitutes the distinctive designation of the recording.",
        ),
        Property(
            "previous_recording",
            "openminds.ephys.Recording",
            "vocab:previousRecording",
            doc="no description available",
        ),
        Property(
            "recorded_with",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            "vocab:recordedWith",
            required=True,
            doc="no description available",
        ),
        Property(
            "sampling_frequency",
            "openminds.core.QuantitativeValue",
            "vocab:samplingFrequency",
            required=True,
            doc="no description available",
        ),
    ]
    reverse_properties = [
        Property(
            "next_recording",
            "openminds.ephys.Recording",
            "^vocab:previousRecording",
            reverse="previous_recordings",
            multiple=True,
            doc="reverse of 'previousRecording'",
        ),
    ]
    existence_query_properties = ("channels", "data_location", "recorded_with", "sampling_frequency")

    def __init__(
        self,
        name=None,
        additional_remarks=None,
        channels=None,
        data_location=None,
        internal_identifier=None,
        next_recording=None,
        previous_recording=None,
        recorded_with=None,
        sampling_frequency=None,
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
            additional_remarks=additional_remarks,
            channels=channels,
            data_location=data_location,
            internal_identifier=internal_identifier,
            next_recording=next_recording,
            previous_recording=previous_recording,
            recorded_with=recorded_with,
            sampling_frequency=sampling_frequency,
        )
