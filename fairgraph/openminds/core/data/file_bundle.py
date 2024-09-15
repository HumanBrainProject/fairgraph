"""
Structured information on a bundle of file instances.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class FileBundle(KGObject):
    """
    Structured information on a bundle of file instances.
    """

    default_space = "files"
    type_ = "https://openminds.ebrains.eu/core/FileBundle"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property("content_description", str, "vocab:contentDescription", doc="no description available"),
        Property(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Property(
            "grouped_by",
            [
                "openminds.computation.LocalFile",
                "openminds.controlled_terms.AnalysisTechnique",
                "openminds.controlled_terms.AuditoryStimulusType",
                "openminds.controlled_terms.BiologicalOrder",
                "openminds.controlled_terms.BiologicalSex",
                "openminds.controlled_terms.BreedingType",
                "openminds.controlled_terms.CellCultureType",
                "openminds.controlled_terms.CellType",
                "openminds.controlled_terms.Disease",
                "openminds.controlled_terms.DiseaseModel",
                "openminds.controlled_terms.ElectricalStimulusType",
                "openminds.controlled_terms.GeneticStrainType",
                "openminds.controlled_terms.GustatoryStimulusType",
                "openminds.controlled_terms.Handedness",
                "openminds.controlled_terms.MRIPulseSequence",
                "openminds.controlled_terms.MRIWeighting",
                "openminds.controlled_terms.MolecularEntity",
                "openminds.controlled_terms.OlfactoryStimulusType",
                "openminds.controlled_terms.OpticalStimulusType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
                "openminds.controlled_terms.OrganismSystem",
                "openminds.controlled_terms.Species",
                "openminds.controlled_terms.StimulationApproach",
                "openminds.controlled_terms.StimulationTechnique",
                "openminds.controlled_terms.SubcellularEntity",
                "openminds.controlled_terms.TactileStimulusType",
                "openminds.controlled_terms.Technique",
                "openminds.controlled_terms.TermSuggestion",
                "openminds.controlled_terms.TissueSampleType",
                "openminds.controlled_terms.UBERONParcellation",
                "openminds.controlled_terms.VisualStimulusType",
                "openminds.core.BehavioralProtocol",
                "openminds.core.File",
                "openminds.core.FileBundle",
                "openminds.core.Subject",
                "openminds.core.SubjectGroup",
                "openminds.core.SubjectGroupState",
                "openminds.core.SubjectState",
                "openminds.core.TissueSample",
                "openminds.core.TissueSampleCollection",
                "openminds.core.TissueSampleCollectionState",
                "openminds.core.TissueSampleState",
                "openminds.sands.CommonCoordinateSpace",
                "openminds.sands.CommonCoordinateSpaceVersion",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.CustomCoordinateSpace",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:groupedBy",
            multiple=True,
            doc="Reference to the aspect used to group something.",
        ),
        Property(
            "grouping_types",
            "openminds.controlled_terms.FileBundleGrouping",
            "vocab:groupingType",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "hash",
            "openminds.core.Hash",
            "vocab:hash",
            doc="Term used for the process of converting any data into a single value. Often also directly refers to the resulting single value.",
        ),
        Property(
            "is_part_of",
            ["openminds.core.FileBundle", "openminds.core.FileRepository"],
            "vocab:isPartOf",
            required=True,
            doc="Reference to the ensemble of multiple things or beings.",
        ),
        Property(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the file bundle.",
        ),
        Property(
            "storage_size",
            "openminds.core.QuantitativeValue",
            "vocab:storageSize",
            doc="Quantitative value defining how much disk space is used by an object on a computer system.",
        ),
    ]
    reverse_properties = [
        Property(
            "describes",
            [
                "openminds.ephys.ElectrodeArrayUsage",
                "openminds.ephys.ElectrodeUsage",
                "openminds.ephys.PipetteUsage",
                "openminds.specimen_prep.SlicingDeviceUsage",
            ],
            "^vocab:metadataLocation",
            reverse="metadata_locations",
            multiple=True,
            doc="reverse of 'metadataLocation'",
        ),
        Property(
            "has_parts",
            ["openminds.core.File", "openminds.core.FileBundle"],
            "^vocab:isPartOf",
            reverse="is_part_of",
            multiple=True,
            doc="reverse of 'isPartOf'",
        ),
        Property(
            "is_also_part_of",
            "openminds.computation.WorkflowRecipeVersion",
            "^vocab:hasPart",
            reverse="has_parts",
            multiple=True,
            doc="reverse of 'hasPart'",
        ),
        Property(
            "is_input_to",
            "openminds.core.DatasetVersion",
            "^vocab:inputData",
            reverse="input_data",
            multiple=True,
            doc="reverse of 'inputData'",
        ),
        Property(
            "is_location_of",
            ["openminds.core.ServiceLink", "openminds.ephys.Recording"],
            "^vocab:dataLocation",
            reverse="data_locations",
            multiple=True,
            doc="reverse of 'dataLocation'",
        ),
        Property(
            "is_output_of",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
                "openminds.core.ModelVersion",
                "openminds.core.ProtocolExecution",
                "openminds.ephys.RecordingActivity",
                "openminds.stimulation.StimulationActivity",
            ],
            ["^vocab:output", "^vocab:outputData"],
            reverse=["output_data", "outputs"],
            multiple=True,
            doc="reverse of output, outputData",
        ),
        Property(
            "is_reference_for",
            "openminds.computation.ValidationTestVersion",
            "^vocab:referenceData",
            reverse="reference_data",
            multiple=True,
            doc="reverse of 'referenceData'",
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
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
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
