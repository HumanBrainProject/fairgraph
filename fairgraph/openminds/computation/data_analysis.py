"""
Structured information on inspecting, cleansing, transforming, and modelling data.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.fields import Field


from datetime import datetime, time


class DataAnalysis(KGObject):
    """
    Structured information on inspecting, cleansing, transforming, and modelling data.
    """

    default_space = "computation"
    type_ = ["https://openminds.ebrains.eu/computation/DataAnalysis"]
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
            "custom_property_sets",
            "openminds.core.CustomPropertySet",
            "vocab:customPropertySet",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the data analysis.",
        ),
        Field("end_time", [datetime, time], "vocab:endTime", doc="no description available"),
        Field(
            "environment",
            ["openminds.computation.Environment", "openminds.core.WebServiceVersion"],
            "vocab:environment",
            required=True,
            doc="no description available",
        ),
        Field(
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
        Field(
            "launch_configuration",
            "openminds.computation.LaunchConfiguration",
            "vocab:launchConfiguration",
            doc="no description available",
        ),
        Field(
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
        Field(
            "performed_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:performedBy",
            multiple=True,
            doc="no description available",
        ),
        Field("recipe", "openminds.computation.WorkflowRecipeVersion", "vocab:recipe", doc="no description available"),
        Field(
            "resource_usages",
            ["openminds.core.QuantitativeValue", "openminds.core.QuantitativeValueRange"],
            "vocab:resourceUsage",
            multiple=True,
            doc="no description available",
        ),
        Field("start_time", [datetime, time], "vocab:startTime", required=True, doc="no description available"),
        Field(
            "started_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:startedBy",
            doc="no description available",
        ),
        Field("status", "openminds.controlledterms.ActionStatusType", "vocab:status", doc="no description available"),
        Field(
            "study_targets",
            [
                "openminds.controlledterms.AuditoryStimulusType",
                "openminds.controlledterms.BiologicalOrder",
                "openminds.controlledterms.BiologicalSex",
                "openminds.controlledterms.BreedingType",
                "openminds.controlledterms.CellCultureType",
                "openminds.controlledterms.CellType",
                "openminds.controlledterms.Disease",
                "openminds.controlledterms.DiseaseModel",
                "openminds.controlledterms.ElectricalStimulusType",
                "openminds.controlledterms.GeneticStrainType",
                "openminds.controlledterms.GustatoryStimulusType",
                "openminds.controlledterms.Handedness",
                "openminds.controlledterms.MolecularEntity",
                "openminds.controlledterms.OlfactoryStimulusType",
                "openminds.controlledterms.OpticalStimulusType",
                "openminds.controlledterms.Organ",
                "openminds.controlledterms.OrganismSubstance",
                "openminds.controlledterms.OrganismSystem",
                "openminds.controlledterms.Species",
                "openminds.controlledterms.SubcellularEntity",
                "openminds.controlledterms.TactileStimulusType",
                "openminds.controlledterms.TermSuggestion",
                "openminds.controlledterms.TissueSampleType",
                "openminds.controlledterms.UBERONParcellation",
                "openminds.controlledterms.VisualStimulusType",
                "openminds.sands.CustomAnatomicalEntity",
                "openminds.sands.ParcellationEntity",
                "openminds.sands.ParcellationEntityVersion",
            ],
            "vocab:studyTarget",
            multiple=True,
            doc="Structure or function that was targeted within a study.",
        ),
        Field("tags", str, "vocab:tag", multiple=True, doc="no description available"),
        Field(
            "techniques",
            "openminds.controlledterms.AnalysisTechnique",
            "vocab:technique",
            multiple=True,
            doc="Method of accomplishing a desired aim.",
        ),
        Field(
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
        Field(
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
        Field(
            "is_part_of",
            "openminds.computation.WorkflowExecution",
            "^vocab:stage",
            reverse="stages",
            multiple=True,
            doc="reverse of 'stage'",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(
        self,
        lookup_label=None,
        custom_property_sets=None,
        description=None,
        end_time=None,
        environment=None,
        inputs=None,
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
        informed=None,
        is_part_of=None,
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
            inputs=inputs,
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
            informed=informed,
            is_part_of=is_part_of,
        )
