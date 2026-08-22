"""
This module contains base classes that define interfaces
and contain code common to sub-classes, to avoid code duplication.
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
from typing import TYPE_CHECKING, Optional, Dict, List, Any, Union
from enum import Enum
import logging
from uuid import UUID
from warnings import warn

from .errors import AuthorizationError

if TYPE_CHECKING:
    from .client import KGClient

OPENMINDS_VERSION = "v4"

logger = logging.getLogger("fairgraph")

JSONdict = Dict[str, Any]  # see https://github.com/python/typing/issues/182 for some possible improvements


class ErrorHandling(str, Enum):
    error = "error"
    warning = "warning"
    log = "log"
    none = "none"

    @classmethod
    def handle_violation(cls, value, errmsg=""):
        if value == cls.error:
            raise ValueError(errmsg)
        elif value == cls.warning:
            warn(errmsg)
        elif value == cls.log:
            logger.warning(errmsg)


class Resolvable:  # all
    def resolve(
        self,
        client: KGClient,
        release_status: Optional[str] = None,
        use_cache: bool = True,
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        pass


class Releasable(Resolvable):  # KGObject, KGProxy
    id: Optional[str]
    remote_data: Optional[JSONdict]

    @property
    def uuid(self) -> Union[str, None]:
        if self.id is not None:
            value = self.id.split("/")[-1]
            return str(UUID(value))
        else:
            return None

    def children(
        self, client: KGClient, follow_links: Optional[Dict[str, Any]] = None
    ) -> List[Releasable]:
        pass

    def is_released(self, client: KGClient, with_children: bool = False) -> bool:
        """Release status of the node"""
        try:
            return client.is_released(self.id, with_children=with_children)
        except AuthorizationError:
            # for unprivileged users
            if self.remote_data and "https://core.kg.ebrains.eu/vocab/meta/firstReleasedAt" in self.remote_data:
                return True
            return False

    def release(self, client: KGClient, with_children: bool = False):
        """Release this node (make it available in public search)."""
        if not self.is_released(client, with_children=with_children):
            if with_children:
                for child in self.children(client):
                    if not child.is_released(client, with_children=False):
                        client.release(child.id)
            return client.release(self.id)

    def unrelease(self, client: KGClient, with_children: bool = False):
        """Un-release this node (remove it from public search)."""
        response = client.unrelease(self.id)
        if with_children:
            for child in self.children(client):
                client.unrelease(child.id)
        return response


# Deprecated aliases
RepresentsSingleObject = Releasable
