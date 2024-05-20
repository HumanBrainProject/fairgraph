"""
Structured information on inspecting, cleansing, transforming, and modelling data.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


from datetime import datetime, time


class DataAnalysis(KGObject):
    """
    Structured information on inspecting, cleansing, transforming, and modelling data.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/DataAnalysis"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "custom_property_sets",
            "openminds.core.CustomPropertySet",
            "vocab:customPropertySet",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the data analysis.",
        ),
        Property("end_time", [datetime, time], "vocab:endTime", doc="no description available"),
        Property(
            "environment",
            ["openminds.computation.Environment", "openminds.core.WebServiceVersion"],
            "vocab:environment",
            required=True,
            doc="no description available",
        ),
        Property(
            "inputs",
            [
                "openminds.computation.LocalFile",
                "openminds.core.File",
                "openminds.core.FileBundle",
                "openminds.core.SoftwareVersion",
                "openminds.sands.BrainAtlasVersion",
                "openminds.sands.CommonCoordinateSpaceVersion",
            ],
            "vocab:input",
            multiple=True,
            required=True,
            doc="Something or someone that is put into or participates in a process or machine.",
        ),
        Property(
            "launch_configuration",
            "openminds.computation.LaunchConfiguration",
            "vocab:launchConfiguration",
            doc="no description available",
        ),
        Property("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Property(
            "outputs",
            [
                "openminds.computation.LocalFile",
                "openminds.core.File",
                "openminds.core.FileArchive",
                "openminds.core.FileBundle",
            ],
            "vocab:output",
            multiple=True,
            required=True,
            doc="Something or someone that comes out of, is delivered or produced by a process or machine.",
        ),
        Property(
            "performed_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:performedBy",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "recipe", "openminds.computation.WorkflowRecipeVersion", "vocab:recipe", doc="no description available"
        ),
        Property(
            "resource_usages",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:resourceUsage",
            multiple=True,
            doc="no description available",
        ),
        Property("start_time", [datetime, time], "vocab:startTime", required=True, doc="no description available"),
        Property(
            "started_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:startedBy",
            doc="no description available",
        ),
        Property(
            "status", "openminds.controlled_terms.ActionStatusType", "vocab:status", doc="no description available"
        ),
        Property(
            "study_targets",
            [
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
                "openminds.controlled_terms.MolecularEntity",
                "openminds.controlled_terms.OlfactoryStimulusType",
                "openminds.controlled_terms.OpticalStimulusType",
                "openminds.controlled_terms.Organ",
                "openminds.controlled_terms.OrganismSubstance",
                "openminds.controlled_terms.OrganismSystem",
                "openminds.controlled_terms.Species",
                "openminds.controlled_terms.SubcellularEntity",
                "openminds.controlled_terms.TactileStimulusType",
                "openminds.controlled_terms.TermSuggestion",
                "openminds.controlled_terms.TissueSampleType",
                "openminds.controlled_terms.UBERONParcellation",
                "openminds.controlled_terms.VisualStimulusType",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:studyTarget",
            multiple=True,
            doc="Structure or function that was targeted within a study.",
        ),
        Property("tags", str, "vocab:tag", multiple=True, doc="no description available"),
        Property(
            "techniques",
            "openminds.controlled_terms.AnalysisTechnique",
            "vocab:technique",
            multiple=True,
            doc="Method of accomplishing a desired aim.",
        ),
        Property(
            "was_informed_by",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "vocab:wasInformedBy",
            doc="no description available",
        ),
        Property(
            "informed",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "^vocab:wasInformedBy",
            reverse="was_informed_by",
            multiple=True,
            doc="reverse of 'wasInformedBy'",
        ),
        Property(
            "is_part_of",
            "openminds.computation.WorkflowExecution",
            "^vocab:stage",
            reverse="stages",
            multiple=True,
            doc="reverse of 'stage'",
        ),
    ]
    existence_query_properties = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        custom_property_sets=None,
        description=None,
        end_time=None,
        environment=None,
        informed=None,
        inputs=None,
        is_part_of=None,
        launch_configuration=None,
        outputs=None,
        performed_by=None,
        recipe=None,
        resource_usages=None,
        start_time=None,
        started_by=None,
        status=None,
        study_targets=None,
        tags=None,
        techniques=None,
        was_informed_by=None,
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
            custom_property_sets=custom_property_sets,
            description=description,
            end_time=end_time,
            environment=environment,
            informed=informed,
            inputs=inputs,
            is_part_of=is_part_of,
            launch_configuration=launch_configuration,
            outputs=outputs,
            performed_by=performed_by,
            recipe=recipe,
            resource_usages=resource_usages,
            start_time=start_time,
            started_by=started_by,
            status=status,
            study_targets=study_targets,
            tags=tags,
            techniques=techniques,
            was_informed_by=was_informed_by,
        )
