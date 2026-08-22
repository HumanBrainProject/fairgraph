"""
This module provides the KGProxy class, which represents a
KGObject whose type and identifier are known but whose other metadata
have not been retrieved from the KG.
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
from typing import List, Optional, Tuple, Union, Dict, Any, TYPE_CHECKING

from openminds.base import Link
from openminds.registry import lookup

from .errors import ResolutionFailure
from .caching import object_cache
from .base import Releasable

if TYPE_CHECKING:
    from .client import KGClient
    from .kgobject import KGObject


logger = logging.getLogger("fairgraph")


class KGProxy(Releasable, Link):
    """
    Representation of an KGObject whose identifier, and possibly type, are known but whose
    other metadata have not been retrieved from the KG.

    Args:
        cls (str, KGObject, List[KGObject]): the possible types of the associated KG object, defined by a KGObject subclass
            or by the name of the subclass.
        uri (URI): The global identifier of the KG object.
        preferred_release_status (str, optional): The preferred scope used to resolve the proxy.
            Valid values are "released", "in progress", or "any".

    Example:
        >>> import fairgraph.openminds
        >>> proxy = KGProxy("openminds.core.Person", "https://kg.ebrains.eu/api/instances/bd554312-9829-4148-8803-cb873d0b32f9")
        >>> person = proxy.resolve(kg_client)
        >>> type(person)
        <class 'fairgraph.openminds.core.actors.person.Person'>
        >>> person.given_name
        Andrew P.
    """

    # todo: rename uri to id, for consistency?

    def __init__(
        self,
        classes: Union[str, KGObject, List[KGObject], Tuple[KGObject]],
        uri: str,
        preferred_release_status: str = "released",
    ):
        self.classes: List[KGObject]  # todo: make this a set?
        if isinstance(classes, str):
            resolved_cls = lookup(classes)
            if TYPE_CHECKING:
                assert isinstance(resolved_cls, KGObject)
            self.classes = [resolved_cls]
        elif isinstance(classes, (list, tuple)):
            self.classes = list(classes)
        else:
            self.classes = [classes]
        if TYPE_CHECKING:
            assert all(isinstance(cls, KGObject) for cls in self.classes)
        self.id = uri
        self.preferred_release_status = preferred_release_status
        self.remote_data = None
        Link.__init__(self, self.id, allowed_types=self.classes)

    @property
    def type(self) -> List[str]:
        """
        Provide the global identifiers of the object type (as a list of URIs).
        """
        try:
            return [cls.type_ for cls in self.classes]
        except AttributeError as err:
            raise AttributeError(f"{err} self.classes={self.classes}")

    @property
    def cls(self):
        """
        For backwards compatibility
        """
        if len(self.classes) == 1:
            return self.classes[0]
        else:
            raise AttributeError("This KGProxy has multiple possible types, use the 'classes' attribute instead")

    def to_jsonld(self, **kwargs):
        return {"@id": self.id}

    def resolve(
        self,
        client: KGClient,
        release_status: Optional[str] = None,
        use_cache: bool = True,
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve the full metadata for the KGObject represented by this proxy.

        Args:
            client: a KGClient
            release_status (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                If not provided, the "preferred_release_status" provided when creating the proxy object will be used.
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.

        Returns:
            a KGObject instance, of the appropriate subclass.
        """
        if use_cache and self.id in object_cache:
            obj = object_cache[self.id]
        else:
            release_status = release_status or self.preferred_release_status
            obj = None
            for cls in self.classes:
                # this is inefficient, we should just get the data from the id, then get the correct type from the data
                try:
                    obj = cls.from_uri(self.id, client, release_status=release_status)
                except TypeError:
                    pass
                else:
                    break
            if obj is None:
                raise ResolutionFailure(f"Cannot resolve proxy object of type {self.classes} with id {self.uuid}")
            object_cache[self.id] = obj
        if follow_links:
            return obj.resolve(client, release_status=release_status, use_cache=use_cache, follow_links=follow_links)
        else:
            return obj

    def __repr__(self):
        return f"""{self.__class__.__name__}([{", ".join(cls.__name__ for cls in self.classes)}], id="{self.id.split('/')[-1]}")"""

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and set(self.classes).intersection(other.classes) and self.id == other.id
        )

    def __ne__(self, other):
        return (
            not isinstance(other, self.__class__) or set(self.classes).isdisjoint(other.classes) or self.id != other.id
        )

    def delete(self, client: KGClient, ignore_not_found: bool = True):
        """Delete the instance which this proxy represents"""
        try:
            obj = self.resolve(client, release_status="in progress")
        except ResolutionFailure as err:
            logger.warning(str(err))
            obj = None
        if obj:
            obj.delete(client, ignore_not_found=ignore_not_found)
        elif not ignore_not_found:
            raise ResolutionFailure("Couldn't resolve object to delete")
