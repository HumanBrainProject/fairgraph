"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class EphysStimulus(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/stimulation/EphysStimulus"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "delivered_by",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimenprep.SlicingDeviceUsage",
            ],
            "vocab:deliveredBy",
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the ephys stimulus.",
        ),
        Field("epoch", "openminds.core.QuantitativeValue", "vocab:epoch", doc="no description available"),
        Field(
            "generated_by",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimenprep.SlicingDeviceUsage",
            ],
            "vocab:generatedBy",
            doc="no description available",
        ),
        Field(
            "internal_identifier",
            str,
            "vocab:internalIdentifier",
            required=True,
            doc="Term or code that identifies the ephys stimulus within a particular product.",
        ),
        Field(
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
        Field(
            "type",
            "openminds.controlledterms.ElectricalStimulusType",
            "vocab:type",
            doc="Distinct class to which a group of entities or concepts with similar characteristics or attributes belong to.",
        ),
        Field(
            "is_stimulus_for",
            "openminds.stimulation.StimulationActivity",
            "^vocab:stimulus",
            reverse="stimuli",
            multiple=True,
            doc="reverse of 'stimulus'",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        delivered_by=None,
        description=None,
        epoch=None,
        generated_by=None,
        internal_identifier=None,
        specifications=None,
        type=None,
        is_stimulus_for=None,
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
            specifications=specifications,
            type=type,
            is_stimulus_for=is_stimulus_for,
        )
