"""
This module provides the EmbeddedMetadata class, which is the base class
for representations of structured metadata that do not have their own identifier,
but are rather embedded within another metadata instance.
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

from __future__ import annotations
import logging
from typing import Optional, TYPE_CHECKING, Union
from warnings import warn

from openminds.base import LinkedNodeEmbedding

from .utility import as_list, ActivityLog
from .base import JSONdict
from .node import KGNode

if TYPE_CHECKING:
    from .client import KGClient


logger = logging.getLogger("fairgraph")


class KGEmbedded(KGNode):
    """
    Base class for metadata structures that are embedded in Knowledge Graph objects.

    Args:
        data (dict, optional): a JSON-LD document containing the KG representation of the metadata.
        properties: the metadata properties (property names and values)
    """

    def __init__(self, data: Optional[JSONdict] = None, **properties):
        super().__init__(data=data, **properties)

    @property
    def space(self) -> Union[str, None]:
        """The KG space the metadata is stored in."""
        return None

    @property
    def default_space(self) -> Union[str, None]:
        """The KG space new metadata will be stored in if no space is specified."""
        return None

    def __repr__(self):
        template_parts = (
            "{}={{self.{}!r}}".format(prop.name, prop.name)
            for prop in self.properties
            if getattr(self, prop.name, None) is not None
        )
        template = "{self.__class__.__name__}(" + ", ".join(template_parts) + ")"
        return template.format(self=self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.to_jsonld(embed_linked_nodes=LinkedNodeEmbedding.NEVER) == other.to_jsonld(
            embed_linked_nodes=LinkedNodeEmbedding.NEVER
        )

    @classmethod
    def from_jsonld(cls, data: JSONdict) -> Union[None, KGEmbedded]:
        """Create an instance of the class from a JSON-LD document."""
        if "@id" in data:
            warn("Expected embedded metadata, but received @id")
            return None
        deserialized_data = cls._deserialize_data(data)
        return cls(data=data, **deserialized_data)

    def save(
        self,
        client: KGClient,
        space: Optional[str] = None,
        recursive: bool = True,
        activity_log: Optional[ActivityLog] = None,
        replace: bool = False,
        ignore_duplicates: bool = False,
    ):
        """
        Save to the KG any sub-components of the metadata object that are KGObjects.
        """
        for prop in self.properties:
            values = getattr(self, prop.name)
            for value in as_list(values):
                if isinstance(value, KGNode):
                    if value.space:
                        target_space = value.space
                    elif (
                        value.__class__.default_space == "controlled"
                        and value.exists(client, ignore_duplicates=ignore_duplicates)
                        and value.space == "controlled"
                    ):
                        continue
                    elif space is None and self.space is not None:
                        target_space = self.space
                    else:
                        assert space is not None  # for type checking
                        target_space = space
                    if target_space == "controlled":
                        if value.exists(client, ignore_duplicates=ignore_duplicates) and value.space == "controlled":
                            continue
                        else:
                            raise Exception("Cannot write to controlled space")
                    value.save(
                        client,
                        space=target_space,
                        recursive=recursive,
                        activity_log=activity_log,
                        ignore_duplicates=ignore_duplicates,
                    )


# Deprecated alias
EmbeddedMetadata = KGEmbedded
