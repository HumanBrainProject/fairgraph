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
from .embedded import EmbeddedMetadata
from .kgproxy import KGProxy
from .kgquery import KGQuery
from .collection import Collection
from . import client, errors, openminds, utility

__version__ = "0.13.2"

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


def set_error_handling(value):
    """Set error handling globally for all modules"""
    for module in (
        openminds.chemicals,
        openminds.computation,
        openminds.controlled_terms,
        openminds.core,
        openminds.ephys,
        openminds.publications,
        openminds.sands,
        openminds.specimen_prep,
        openminds.stimulation,
    ):
        module.set_error_handling(value)
