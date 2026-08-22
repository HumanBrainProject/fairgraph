"""
Python client for the EBRAINS Knowledge Graph

Authors: Andrew Davison et al., CNRS (see authors.rst)


Copyright 2018-2024 CNRS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from openminds import IRI
from .client import KGClient
from .kgobject import KGObject
from .embedded import KGEmbedded, EmbeddedMetadata  # EmbeddedMetadata is a deprecated alias
from .kgproxy import KGProxy
from .kgquery import KGQuery
from .collection import Collection
from . import client, errors, openminds, utility

__version__ = "0.15.0.dev0"

utility.initialise_instances(
    [
        openminds.sands.BrainAtlas,
        openminds.sands.BrainAtlasVersion,
        openminds.sands.CommonCoordinateSpace,
        openminds.sands.CommonCoordinateSpaceVersion,
        openminds.core.ContentType,
        openminds.core.License,
        openminds.sands.ParcellationEntity,
        openminds.sands.ParcellationEntityVersion,
    ]
    + openminds.controlled_terms.list_kg_classes()
)

utility.initialise_instances(
    [
        openminds.v5.sands.AnatomicalAtlas,
        openminds.v5.sands.AnatomicalAtlasVersion,
        openminds.v5.sands.CommonCoordinateFramework,
        openminds.v5.sands.CommonCoordinateFrameworkVersion,
        openminds.v5.core.ContentType,
        openminds.v5.core.License,
        openminds.v5.sands.ParcellationEntity,
        openminds.v5.sands.ParcellationEntityVersion,
    ]
    + openminds.v5.controlled_terms.list_kg_classes()
)


def set_error_handling(value):
    """Set error handling globally for all modules"""
    openminds.set_error_handling(value)
