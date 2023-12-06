import sys
import inspect
from fairgraph.kgobject import KGObject
from fairgraph.embedded import EmbeddedMetadata

from .data_analysis import DataAnalysis
from .data_copy import DataCopy
from .environment import Environment
from .generic_computation import GenericComputation
from .hardware_system import HardwareSystem
from .launch_configuration import LaunchConfiguration
from .local_file import LocalFile
from .model_validation import ModelValidation
from .optimization import Optimization
from .simulation import Simulation
from .software_agent import SoftwareAgent
from .validation_test import ValidationTest
from .validation_test_version import ValidationTestVersion
from .visualization import Visualization
from .workflow_execution import WorkflowExecution
from .workflow_recipe import WorkflowRecipe
from .workflow_recipe_version import WorkflowRecipeVersion


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__.startswith(__name__)
    ]


def list_embedded_metadata_classes():
    """List all embedded metadata classes defined in this module"""
    return [
        obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(obj) and issubclass(obj, EmbeddedMetadata) and obj.__module__.startswith(__name__)
    ]


def set_error_handling(value):
    """
    Control validation for all classes in this module.

    Args:
        value (str): action to follow when there is a validation failure.
            (e.g. if a required field is not provided).
            Possible values: "error", "warning", "log", None
    """
    for cls in list_kg_classes() + list_embedded_metadata_classes():
        cls.set_error_handling(value)
