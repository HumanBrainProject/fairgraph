"""
Helpers for introspecting a module to discover and configure its KG classes.

These are used by the per-domain ``fairgraph.openminds`` submodules to expose
module-scoped ``list_kg_classes()``, ``list_embedded_metadata_classes()`` and
``set_error_handling()`` functions.
"""

# Copyright 2018-2026 CNRS and fairgraph authors and/or their employers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect

from .kgobject import KGObject
from .embedded import KGEmbedded


def list_kg_classes(module):
    """List all KG classes defined in the given module."""
    return [obj for name, obj in inspect.getmembers(module)
            if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__.startswith(module.__name__)]


def list_embedded_metadata_classes(module):
    """List all embedded metadata classes defined in the given module."""
    return [obj for name, obj in inspect.getmembers(module)
            if inspect.isclass(obj) and issubclass(obj, KGEmbedded) and obj.__module__.startswith(module.__name__)]


def set_error_handling(value, module):
    """
    Control validation for all classes in the given module.

    Args:
        value (str): action to follow when there is a validation failure.
            (e.g. if a required property is not provided).
            Possible values: "error", "warning", "log", None
        module: the module whose classes should be updated.
    """
    for cls in list_kg_classes(module) + list_embedded_metadata_classes(module):
        cls.set_error_handling(value)
