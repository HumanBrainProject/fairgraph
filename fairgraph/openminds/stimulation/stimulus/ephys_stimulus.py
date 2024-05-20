"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class EphysStimulus(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = "https://openminds.ebrains.eu/stimulation/EphysStimulus"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "delivered_by",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            "vocab:deliveredBy",
            doc="no description available",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the ephys stimulus.",
        ),
        Property("epoch", "openminds.core.QuantitativeValue", "vocab:epoch", doc="no description available"),
        Property(
            "generated_by",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            "vocab:generatedBy",
            doc="no description available",
        ),
        Property(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            required=True,
            doc="Term or code that identifies the ephys stimulus within a particular product.",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "specifications",
            [
                "openminds.core.Configuration",
                "openminds.core.File",
                "openminds.core.FileBundle",
                "openminds.core.PropertyValueList",
            ],
            "vocab:specification",
            multiple=True,
            doc="Detailed and precise presentation of, or proposal for something.",
        ),
        Property(
            "type",
            "openminds.controlled_terms.ElectricalStimulusType",
            "vocab:type",
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Property(
            "is_stimulus_for",
            "openminds.stimulation.StimulationActivity",
            "^vocab:stimulus",
            reverse="stimuli",
            multiple=True,
            doc="reverse of 'stimulus'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        delivered_by=None,
        description=None,
        epoch=None,
        generated_by=None,
        internal_identifier=None,
        is_stimulus_for=None,
        specifications=None,
        type=None,
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
            delivered_by=delivered_by,
            description=description,
            epoch=epoch,
            generated_by=generated_by,
            internal_identifier=internal_identifier,
            is_stimulus_for=is_stimulus_for,
            specifications=specifications,
            type=type,
        )
