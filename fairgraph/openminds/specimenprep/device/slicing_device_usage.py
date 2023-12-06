"""
<description not available>
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class SlicingDeviceUsage(KGObject):
    """
    <description not available>
    """

    default_space = "in-depth"
    type_ = ["https://openminds.ebrains.eu/specimenPrep/SlicingDeviceUsage"]
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
            "device",
            "openminds.specimenprep.SlicingDevice",
            "vocab:device",
            required=True,
            doc="Piece of equipment or mechanism (hardware) designed to serve a special purpose or perform a special function.",
        ),
        Field(
            "metadata_locations",
            ["openminds.core.File", "openminds.core.FileBundle"],
            "vocab:metadataLocation",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "oscillation_amplitude",
            "openminds.core.QuantitativeValue",
            "vocab:oscillationAmplitude",
            doc="no description available",
        ),
        Field(
            "slice_thickness",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:sliceThickness",
            required=True,
            doc="no description available",
        ),
        Field(
            "slicing_angles",
            ["openminds.core.QuantitativeValue", "openminds.core.NumericalProperty"],
            "vocab:slicingAngle",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "slicing_plane",
            "openminds.controlledterms.AnatomicalPlane",
            "vocab:slicingPlane",
            required=True,
            doc="no description available",
        ),
        Field(
            "slicing_speed", "openminds.core.QuantitativeValue", "vocab:slicingSpeed", doc="no description available"
        ),
        Field(
            "used_specimen",
            ["openminds.core.SubjectState", "openminds.core.TissueSampleState"],
            "vocab:usedSpecimen",
            doc="no description available",
        ),
        Field(
            "vibration_frequency",
            "openminds.core.QuantitativeValue",
            "vocab:vibrationFrequency",
            doc="no description available",
        ),
        Field(
            "generation_device",
            "openminds.stimulation.EphysStimulus",
            "^vocab:generatedBy",
            reverse="generated_by",
            multiple=True,
            doc="reverse of 'generatedBy'",
        ),
        Field(
            "placed_by",
            "openminds.ephys.ElectrodePlacement",
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
        Field(
            "used_for",
            "openminds.specimenprep.TissueSampleSlicing",
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
        Field(
            "used_in",
            "openminds.ephys.CellPatching",
            "^vocab:device",
            reverse="devices",
            multiple=True,
            doc="reverse of 'device'",
        ),
        Field(
            "used_to_measure",
            "openminds.core.Measurement",
            "^vocab:measuredWith",
            reverse="measured_with",
            multiple=True,
            doc="reverse of 'measuredWith'",
        ),
        Field(
            "used_to_record",
            "openminds.ephys.Recording",
            "^vocab:recordedWith",
            reverse="recorded_with",
            multiple=True,
            doc="reverse of 'recordedWith'",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        device=None,
        metadata_locations=None,
        oscillation_amplitude=None,
        slice_thickness=None,
        slicing_angles=None,
        slicing_plane=None,
        slicing_speed=None,
        used_specimen=None,
        vibration_frequency=None,
        generation_device=None,
        placed_by=None,
        used_for=None,
        used_in=None,
        used_to_measure=None,
        used_to_record=None,
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
            device=device,
            metadata_locations=metadata_locations,
            oscillation_amplitude=oscillation_amplitude,
            slice_thickness=slice_thickness,
            slicing_angles=slicing_angles,
            slicing_plane=slicing_plane,
            slicing_speed=slicing_speed,
            used_specimen=used_specimen,
            vibration_frequency=vibration_frequency,
            generation_device=generation_device,
            placed_by=placed_by,
            used_for=used_for,
            used_in=used_in,
            used_to_measure=used_to_measure,
            used_to_record=used_to_record,
        )
