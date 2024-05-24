"""
Structured information about an execution of a computational workflow.
"""

# this file was auto-generated

from fairgraph import KGObject, IRI
from fairgraph.properties import Property


class WorkflowExecution(KGObject):
    """
    Structured information about an execution of a computational workflow.
    """

    default_space = "computation"
    type_ = "https://openminds.ebrains.eu/computation/WorkflowExecution"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    properties = [
        Property(
            "configuration",
            ["openminds.core.Configuration", "openminds.core.File"],
            "vocab:configuration",
            doc="no description available",
        ),
        Property(
            "recipe", "openminds.computation.WorkflowRecipeVersion", "vocab:recipe", doc="no description available"
        ),
        Property(
            "stages",
            [
                "openminds.computation.DataAnalysis",
                "openminds.computation.DataCopy",
                "openminds.computation.GenericComputation",
                "openminds.computation.ModelValidation",
                "openminds.computation.Optimization",
                "openminds.computation.Simulation",
                "openminds.computation.Visualization",
            ],
            "vocab:stage",
            multiple=True,
            doc="no description available",
        ),
        Property(
            "started_by",
            ["openminds.computation.SoftwareAgent", "openminds.core.Person"],
            "vocab:startedBy",
            doc="no description available",
        ),
    ]
    reverse_properties = []
    existence_query_properties = ("stages",)

    def __init__(
        self, configuration=None, recipe=None, stages=None, started_by=None, id=None, data=None, space=None, scope=None
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            configuration=configuration,
            recipe=recipe,
            stages=stages,
            started_by=started_by,
        )
