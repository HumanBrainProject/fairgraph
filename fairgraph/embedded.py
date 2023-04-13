"""

"""

# Copyright 2018-2020 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from warnings import warn

from .utility import as_list, normalize_data
from .errors import ResolutionFailure
from .base import Resolvable, ContainsMetadata, RepresentsSingleObject
from .kgobject import KGObject

logger = logging.getLogger("fairgraph")


class EmbeddedMetadata(ContainsMetadata, Resolvable):
    """Base class for metadata structures that are embedded in Knowledge Graph objects"""
    fields = []

    def __init__(self, data=None, **properties):
        super().__init__(data=data, **properties)

    @property
    def space(self):
        return None

    @property
    def default_space(self):
        return None

    def __repr__(self):
        template_parts = ("{}={{self.{}!r}}".format(field.name, field.name)
                            for field in self.fields if getattr(self, field.name) is not None)
        template = "{self.__class__.__name__}(" + ", ".join(template_parts) + ")"
        return template.format(self=self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.to_jsonld() == other.to_jsonld()

    @classmethod
    def from_kg_instance(cls, data, client):
        if "@id" in data:
            warn("Expected embedded metadata, but received @id")
            return None
        deserialized_data = cls._deserialize_data(data, client)
        return cls(data=data, **deserialized_data)

    def save(self, client, space=None, recursive=True, activity_log=None, replace=False):
        for field in self.fields:
            if field.intrinsic:
                values = getattr(self, field.name)
                for value in as_list(values):
                    if isinstance(value, ContainsMetadata):
                        if value.space:
                            target_space = value.space
                        elif value.__class__.default_space == "controlled" and value.exists(client) and value.space == "controlled":
                            continue
                        elif space is None and self.space is not None:
                            target_space = self.space
                        else:
                            target_space = space
                        if target_space == "controlled":
                            if value.exists(client) and value.space == "controlled":
                                continue
                            else:
                                raise Exception("Cannot write to controlled space")
                        value.save(client, space=target_space, recursive=True,
                                    activity_log=activity_log)
