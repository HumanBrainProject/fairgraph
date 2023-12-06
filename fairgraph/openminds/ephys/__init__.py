import sys
import inspect
from fairgraph.kgobject import KGObject
from fairgraph.embedded import EmbeddedMetadata

from .activity import RecordingActivity, ElectrodePlacement, CellPatching
from .entity import Channel, Recording
from .device import ElectrodeArray, PipetteUsage, Pipette, Electrode, ElectrodeArrayUsage, ElectrodeUsage


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
