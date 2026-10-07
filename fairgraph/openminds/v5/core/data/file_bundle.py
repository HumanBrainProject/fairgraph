"""
Structured information on a bundle of file instances.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v5.core import FileBundle as OMFileBundle
from fairgraph import KGObject


class FileBundle(KGObject, OMFileBundle):
    """
    Structured information on a bundle of file instances.
    """

    type_ = "https://openminds.om-i.org/types/FileBundle"
    default_space = "files"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.v5.ephys.ElectrodeArrayUsage",
                "openminds.v5.ephys.ElectrodeUsage",
                "openminds.v5.ephys.PipetteUsage",
                "openminds.v5.neuroimaging.MRICoilUsage",
                "openminds.v5.neuroimaging.MRIScannerUsage",
                "openminds.v5.specimen_prep.SlicingDeviceUsage",
            ],
            "metadataLocation",
            reverse="metadata_locations",
            multiple=True,
            description="reverse of 'metadata_locations'",
        ),
        Property(
            "has_parts",
            ["openminds.v5.core.File", "openminds.v5.core.FileBundle"],
            "isPartOf",
            reverse="is_part_of",
            multiple=True,
            description="reverse of 'is_part_of'",
        ),
        Property(
            "is_also_part_of",
            "openminds.v5.computation.WorkflowRecipeVersion",
            "hasPart",
            reverse="has_parts",
            multiple=True,
            description="reverse of 'has_parts'",
        ),
        Property(
            "is_input_to",
            "openminds.v5.core.DatasetVersion",
            "inputData",
            reverse="input_data",
            multiple=True,
            description="reverse of 'input_data'",
        ),
        Property(
            "is_location_of",
            [
                "openminds.v5.core.GridImage",
                "openminds.v5.core.GridImageSequence",
                "openminds.v5.core.GridImageStack",
                "openminds.v5.core.GridVolume",
                "openminds.v5.core.GridVolumeSequence",
                "openminds.v5.core.RegularTimeSeries",
                "openminds.v5.core.ServiceLink",
            ],
            "dataLocation",
            reverse="data_location",
            multiple=True,
            description="reverse of 'data_location'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.v5.computation.DataAnalysis",
                "openminds.v5.computation.DataCopy",
                "openminds.v5.computation.GenericComputation",
                "openminds.v5.computation.ModelValidation",
                "openminds.v5.computation.Optimization",
                "openminds.v5.computation.Simulation",
                "openminds.v5.computation.Visualization",
                "openminds.v5.core.ModelVersion",
                "openminds.v5.core.ProtocolExecution",
                "openminds.v5.ephys.RecordingActivity",
                "openminds.v5.stimulation.StimulationActivity",
            ],
            ["output", "outputData"],
            reverse=["output_data", "outputs"],
            multiple=True,
            description="reverse of output_data, outputs",
        ),
        Property(
            "is_reference_for",
            "openminds.v5.computation.ValidationTestVersion",
            "referenceData",
            reverse="reference_data",
            multiple=True,
            description="reverse of 'reference_data'",
        ),
        Property(
            "specifies",
            "openminds.v5.stimulation.EphysStimulus",
            "specification",
            reverse="specifications",
            multiple=True,
            description="reverse of 'specifications'",
        ),
    ]
    existence_query_properties = ("is_part_of", "name")

    def __init__(
        self,
        name=None,
        content_description=None,
        describes=None,
        format=None,
        grouped_by=None,
        grouping_types=None,
        has_parts=None,
        hash=None,
        is_also_part_of=None,
        is_input_to=None,
        is_location_of=None,
        is_output_of=None,
        is_part_of=None,
        is_reference_for=None,
        specifies=None,
        storage_size=None,
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
            content_description=content_description,
            describes=describes,
            format=format,
            grouped_by=grouped_by,
            grouping_types=grouping_types,
            has_parts=has_parts,
            hash=hash,
            is_also_part_of=is_also_part_of,
            is_input_to=is_input_to,
            is_location_of=is_location_of,
            is_output_of=is_output_of,
            is_part_of=is_part_of,
            is_reference_for=is_reference_for,
            specifies=specifies,
            storage_size=storage_size,
        )
