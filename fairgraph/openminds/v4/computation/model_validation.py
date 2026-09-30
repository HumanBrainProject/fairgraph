"""
Structured information about a process of validating a computational model.
"""

# this file was auto-generated

from openminds.properties import Property
from openminds.v4.computation import ModelValidation as OMModelValidation
from fairgraph import KGObject


from datetime import datetime, time
from numbers import Real


class ModelValidation(KGObject, OMModelValidation):
    """
    Structured information about a process of validating a computational model.
    """

    type_ = "https://openminds.om-i.org/types/ModelValidation"
    default_space = "computation"
    SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    # forward properties are defined in the parent class (in openMINDS-Python)
    reverse_properties = [
        Property(
            "informed",
            [
                "openminds.v4.computation.DataAnalysis",
                "openminds.v4.computation.DataCopy",
                "openminds.v4.computation.GenericComputation",
                "openminds.v4.computation.ModelValidation",
                "openminds.v4.computation.Optimization",
                "openminds.v4.computation.Simulation",
                "openminds.v4.computation.Visualization",
            ],
            "wasInformedBy",
            reverse="was_informed_by",
            multiple=True,
            description="reverse of 'was_informed_by'",
        ),
        Property(
            "is_part_of",
            "openminds.v4.computation.WorkflowExecution",
            "stage",
            reverse="stages",
            multiple=True,
            description="reverse of 'stages'",
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
        score=None,
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
        release_status=None,
    ):
        return KGObject.__init__(
            self,
            id=id,
            space=space,
            release_status=release_status,
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
            score=score,
            start_time=start_time,
            started_by=started_by,
            status=status,
            study_targets=study_targets,
            tags=tags,
            techniques=techniques,
            was_informed_by=was_informed_by,
        )
