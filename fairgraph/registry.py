"""
Classes and functions for looking up schema classes
based on names and type identifiers.

"""

from __future__ import annotations
from typing import TYPE_CHECKING, Union, List
from warnings import warn

if TYPE_CHECKING:
    from .base import ContainsMetadata

registry: dict = {"names": {}, "types": {}}


def register_class(target_class: ContainsMetadata):
    """Add a class to the registry"""
    if "openminds" in target_class.__module__:
        parts = target_class.__module__.split(".")
        name = ".".join(parts[1:3] + [target_class.__name__])  # e.g. openminds.core.Dataset
    else:
        name = target_class.__module__.split(".")[-1] + "." + target_class.__name__

    registry["names"][name] = target_class
    if hasattr(target_class, "type_"):
        assert isinstance(target_class.type_, str)
        type_ = target_class.type_
        if type_ in registry["types"]:
            if isinstance(registry["types"][type_], list):
                registry["types"][type_].append(target_class)
            else:
                registry["types"][type_] = [registry["types"][type_], target_class]
        else:
            registry["types"][type_] = target_class


def lookup(class_name: str) -> ContainsMetadata:
    """Return the class whose name is given."""
    return registry["names"][class_name]


def lookup_type(class_type: Union[str, List[str]]) -> ContainsMetadata:
    """Return the class whose global type identifier (a URI) is given."""
    if isinstance(class_type, str):
        if class_type in registry["types"]:
            return registry["types"][class_type]
        else:
            return registry["types"][(class_type,)]
    else:
        return registry["types"][tuple(sorted(class_type))]


docstring_template = """
{base}

Args
----
{args}

"""


class Registry(type):
    """Metaclass for registering Knowledge Graph classes."""

    properties = []
    aliases = {}

    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        cls._base_docstring = class_dict.get("__doc__", "").strip()
        cls._property_lookup = {
            prop.name: prop for prop in cls.properties
        }
        register_class(cls)
        return cls

    def _get_doc(cls) -> str:
        """Dynamically generate docstrings"""
        property_docs = []
        if hasattr(cls, "properties"):

            def gen_path(type_):
                if type_.__module__ == "builtins":
                    return type_.__name__
                else:
                    return "~{}.{}".format(type_.__module__, type_.__name__)

            for prop in cls.properties:
                doc = "{} : {}\n    {}".format(prop.name, ", ".join(gen_path(t) for t in prop.types), prop.doc)
                property_docs.append(doc)
        return docstring_template.format(base=cls._base_docstring, args="\n".join(property_docs))

    __doc__ = property(_get_doc)

    @property
    def property_names(cls) -> List[str]:
        return list(cls._property_lookup.keys())

    @property
    def required_property_names(cls) -> List[str]:
        return [f.name for f in cls.properties if f.required]

    @property
    def fields(cls):
        warn(
            "Use of the 'fields' attribute is deprecated, it will be removed in a future release. "
            "Use 'properties' instead",
            DeprecationWarning,
        )
        return cls.properties

    @property
    def field_names(cls):
        warn(
            "Use of the 'field_names' attribute is deprecated, it will be removed in a future release. "
            "Use 'property_names' instead",
            DeprecationWarning,
        )
        return cls.property_names

    @property
    def required_field_names(cls):
        warn(
            "Use of the 'required_field_names' attribute is deprecated, it will be removed in a future release. "
            "Use 'required_property_names' instead",
            DeprecationWarning,
        )
        return cls.property_names

    @property
    def existence_query_fields(cls):
        warn(
            "Use of the 'existence_query_fields' attribute is deprecated, it will be removed in a future release. "
            "Use 'existence_query_properties' instead",
            DeprecationWarning,
        )
        return cls.existence_query_properties
