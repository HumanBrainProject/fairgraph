"""
This module provides the KGObject class, which is the base class
for representations of structured metadata that have a globally
unique identifier (a URI).
"""

# Copyright 2018-2024 CNRS

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
from collections import defaultdict
import logging
from uuid import UUID
from warnings import warn
from typing import Any, Tuple, Dict, List, Optional, TYPE_CHECKING, Union

from requests.exceptions import HTTPError

try:
    from tabulate import tabulate

    have_tabulate = True
except ImportError:
    have_tabulate = False
from .utility import expand_uri, as_list, expand_filter, ActivityLog
from .registry import lookup_type
from .queries import Query
from .errors import AuthorizationError, ResourceExistsError, CannotBuildExistenceQuery
from .caching import object_cache, save_cache, generate_cache_key
from .base import RepresentsSingleObject, ContainsMetadata, SupportsQuerying, IRI, JSONdict
from .kgproxy import KGProxy
from .kgquery import KGQuery

if TYPE_CHECKING:
    from .properties import Property
    from .client import KGClient


logger = logging.getLogger("fairgraph")


class KGObject(ContainsMetadata, RepresentsSingleObject, SupportsQuerying):
    """
    Base class for Knowledge Graph objects.

    Should not be instantiated directly, intended to be subclassed.
    """

    properties: List[Property] = []
    existence_query_properties: Tuple[str, ...] = ("name",)
    # Note that this default value of existence_query_properties should in
    # many cases be over-ridden.
    # It assumes that "name" is unique within instances of a given type,
    # which may often not be the case.

    def __init__(
        self,
        id: Optional[str] = None,
        data: Optional[JSONdict] = None,
        space: Optional[str] = None,
        scope: Optional[str] = None,
        **properties,
    ):
        self.id = id
        self._space = space
        self.scope = scope
        self.allow_update = True
        super().__init__(data=data, **properties)
        for prop in self.reverse_properties:
            if not hasattr(self, prop.name):
                query = KGQuery(
                    prop.types, {prop.reverse: self.id}, callback=lambda value: setattr(self, prop.name, value)
                )
                setattr(self, prop.name, query)

    def __repr__(self):
        template_parts = (
            "{}={{self.{}!r}}".format(prop.name, prop.name)
            for prop in self.__class__.all_properties
            if getattr(self, prop.name) is not None
        )
        template = "{self.__class__.__name__}(" + ", ".join(template_parts) + ", space={self.space}, id={self.id})"
        return template.format(self=self)

    @property
    def space(self) -> Union[str, None]:
        if self._raw_remote_data:
            if "https://schema.hbp.eu/myQuery/space" in self._raw_remote_data:
                self._space = self._raw_remote_data["https://schema.hbp.eu/myQuery/space"]
            elif "https://core.kg.ebrains.eu/vocab/meta/space" in self._raw_remote_data:
                self._space = self._raw_remote_data["https://core.kg.ebrains.eu/vocab/meta/space"]
        return self._space

    @classmethod
    def from_kg_instance(cls, data: JSONdict, client: KGClient, scope: Optional[str] = None):
        """Create an instance of the class from a JSON-LD document."""
        deserialized_data = cls._deserialize_data(data, client, include_id=True)
        return cls(id=data["@id"], data=data, scope=scope, **deserialized_data)

    # @classmethod
    # def _fix_keys(cls, data):
    #     """
    #     The KG Query API does not allow the same property name to be used twice in a document.
    #     This is a problem when resolving linked nodes which use the same property names
    #     as the 'parent'. As a workaround, we prefix the property names in the linked node
    #     with the class name.
    #     This method removes this prefix.
    #     This feels like a kludge, and I'd be happy to find a better solution.
    #     """
    #     prefix = cls.__name__ + "__"
    #     for key in list(data):
    #         # need to use list() in previous line to avoid
    #         # "dictionary keys changed during iteration" error in Python 3.8+
    #         if key.startswith(prefix):
    #             fixed_key = key.replace(prefix, "")
    #             data[fixed_key] = data.pop(key)
    #     return data

    @classmethod
    def from_uri(
        cls,
        uri: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its URI.

        Args:
            uri (str): long-form identifier for the KG instance (a full URI)
            client: a KGClient
            scope (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        if follow_links:
            query = cls.generate_query(space=None, client=client, filters=None, follow_links=follow_links)
            results = client.query(query, instance_id=client.uuid_from_uri(uri), size=1, scope=scope).data
            if results:
                data = results[0]
                data["@context"] = cls.context
            else:
                data = None
        else:
            data = client.instance_from_full_uri(uri, use_cache=use_cache, scope=scope)
        if data is None:
            return None
        else:
            return cls.from_kg_instance(data, client, scope=scope)

    @classmethod
    def from_uuid(
        cls,
        uuid: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its UUID.

        Args:
            uuid (str): short-form identifier for the KG instance (a UUID).
            client: a KGClient
            scope (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        logger.info("Attempting to retrieve {} with uuid {}".format(cls.__name__, uuid))
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        try:
            val = UUID(uuid, version=4)  # check validity of uuid
        except ValueError as err:
            raise ValueError("{} - {}".format(err, uuid))
        uri = cls.uri_from_uuid(uuid, client)
        return cls.from_uri(uri, client, use_cache=use_cache, scope=scope, follow_links=follow_links)

    @classmethod
    def from_id(
        cls,
        id: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on either its URI or UUID.

        Args:
            id (str): short-form (UUID) or long-form (URI) identifier for the KG instance.
            client: a KGClient
            scope (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        if hasattr(cls, "type_") and cls.type_:
            if id.startswith("http"):
                return cls.from_uri(id, client, use_cache=use_cache, scope=scope, follow_links=follow_links)
            else:
                return cls.from_uuid(id, client, use_cache=use_cache, scope=scope, follow_links=follow_links)
        else:
            # if we don't know the type
            if id.startswith("http"):
                uri = id
            else:
                uri = client.uri_from_uuid(id)
            if follow_links is not None:
                raise NotImplementedError
            data = client.instance_from_full_uri(uri, use_cache=use_cache, scope=scope)
            cls_from_data = lookup_type(data["@type"][0])
            return cls_from_data.from_kg_instance(data, client, scope=scope)

    @classmethod
    def from_alias(
        cls,
        alias: str,
        client: KGClient,
        space: Optional[str] = None,
        scope: str = "released",
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its alias/short name.

        Note that not all metadata classes have an alias.

        Args:
            alias (str): a short name used to identify a KG instance.
            client: a KGClient
            space (str, optional): the KG space to look in. Default is to look in all available spaces.
            scope (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        # todo: move this to openminds generation, and include only in those subclasses
        # that have an alias
        # todo: also count 'lookup_name' as an alias
        if "short_name" not in cls.property_names:
            raise AttributeError(f"{cls.__name__} doesn't have an 'alias' or 'short_name' property")
        candidates = as_list(
            cls.list(
                client,
                size=20,
                from_index=0,
                api="query",
                scope=scope,
                space=space,
                alias=alias,
                follow_links=follow_links,
            )
        )
        if len(candidates) == 0:
            return None
        elif len(candidates) == 1:
            return candidates[0]
        else:  # KG query does a "contains" lookup, so can get multiple results
            for candidate in candidates:
                if candidate.alias == alias:
                    return candidate
            warn(
                "Multiple objects found with a similar alias, but none match exactly." "Returning the first one found."
            )
            return candidates[0]

    @property
    def uuid(self) -> Union[str, None]:
        # todo: consider using client._kg_client.uuid_from_absolute_id
        if self.id is not None:
            return self.id.split("/")[-1]
        else:
            return None

    @classmethod
    def uri_from_uuid(cls, uuid: str, client: KGClient) -> str:
        """Convert an instances short-form identifier (a UUID) into the long-form (a URI)"""
        return client.uri_from_uuid(uuid)

    @classmethod
    def list(
        cls,
        client: KGClient,
        size: int = 100,
        from_index: int = 0,
        api: str = "auto",
        scope: str = "released",
        space: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        **filters,
    ) -> List[KGObject]:
        """
        List all objects of this type in the Knowledge Graph

        Args:
            client: KGClient object that handles the communication with the KG.
            size (int, optional): The maximum number of instances to return. Default is 100.
            from_index (int, optional): The index of the first instance to return. Default is 0.
            api (str): The KG API to use for the query. Can be 'query', 'core', or 'auto'. Default is 'auto'.
            scope (str, optional): The scope to use for the query. Can be 'released', 'in progress', or 'all'. Default is 'released'.
            space (str, optional): The KG space to be queried. If not specified, results from all accessible spaces will be included.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            filters: Optional keyword arguments representing filters to apply to the query.

        Returns:
            A list of instances of this class representing the objects returned by the KG query.

        Raises:
            ValueError: If invalid arguments are passed to the method.
            NotImplementedError: If 'follow_links' is used with api='core'.

        Example:

            >>> from fairgraph import KGClient
            >>> import fairgraph.openminds.controlled_terms as terms
            >>> interneuron_types = terms.CellType.list(client, name="interneuron")
            >>> for ct in interneuron_types[:4]:
            ...     print(f"{ct.name:<30} {ct.definition}")
            cerebellar interneuron         None
            cholinergic interneuron        An inhibitory interneuron which mainly uses the neurotrasmitter acetylcholine (ACh).
            cortical interneuron           None
            fast spiking interneuron       A parvalbumin positive GABAergic interneuron with a high-frequency firing pattern.

        """

        if api == "auto":
            if filters:
                api = "query"
            else:
                api = "core"

        if api == "query":
            query = cls.generate_query(space=space, client=client, filters=filters, follow_links=follow_links)
            instances = client.query(
                query=query,
                from_index=from_index,
                size=size,
                scope=scope,
            ).data
            for instance in instances:
                instance["@context"] = cls.context
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            if follow_links:
                raise NotImplementedError("Following links with api='core' not yet implemented")
            instances = client.list(cls.type_, space=space, from_index=from_index, size=size, scope=scope).data
        else:
            raise ValueError("'api' must be either 'query', 'core', or 'auto'")

        return [cls.from_kg_instance(instance, client, scope=scope) for instance in instances]

    @classmethod
    def count(
        cls,
        client: KGClient,
        api: str = "auto",
        scope: str = "released",
        space: Optional[str] = None,
        **filters,
    ) -> int:
        """
        Count the number of objects of a given type and (optionally) matching a given set of filters.

        Args:
            client: KGClient object that handles the communication with the KG.
            api (str): The KG API to use for the query. Can be 'query', 'core', or 'auto'. Default is 'auto'.
            scope (str, optional): The scope to use for the query. Can be 'released', 'in progress', or 'all'. Default is 'released'.
            space (str, optional): The KG space to be queried. If not specified, results from all accessible spaces will be counted.
            filters: Optional keyword arguments representing filters to apply to the query.

        Returns:
            The number of instances of this class in the given space that would match the given filters,
            or the total number of instances if no filters are provided.

        Raises:
            ValueError: If invalid arguments are passed to the method.
            NotImplementedError: If 'follow_links' is used with api='core'.

        Example:

            >>> from fairgraph import KGClient
            >>> import fairgraph.openminds.controlled_terms as terms
            >>> terms.CellType.count(client, name="interneuron")
            8

        """
        if api == "auto":
            if filters:
                api = "query"
            else:
                api = "core"
        if api == "query":
            query = cls.generate_query(space=space, client=client, filters=filters)
            response = client.query(query=query, from_index=0, size=1, scope=scope)
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            response = client.list(cls.type_, space=space, scope=scope, from_index=0, size=1)
        return response.total

    def _update_empty_properties(self, data: JSONdict, client: KGClient):
        """Replace any empty properties (value None) with the supplied data"""
        cls = self.__class__
        deserialized_data = cls._deserialize_data(data, client, include_id=True)
        for prop in cls.all_properties:
            current_value = getattr(self, prop.name, None)
            if current_value is None:
                value = deserialized_data[prop.name]
                setattr(self, prop.name, value)
        assert self.remote_data is not None
        for key, value in data.items():
            if not key.startswith("Q"):
                expanded_path = expand_uri(key, cls.context)
                assert isinstance(expanded_path, str)
                self.remote_data[expanded_path] = data[key]

    def __eq__(self, other):
        return not self.__ne__(other)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        if self.id and other.id and self.id != other.id:
            return True
        for prop in self.properties:
            assert prop.intrinsic
            val_self = getattr(self, prop.name)
            val_other = getattr(other, prop.name)
            if val_self != val_other:
                return True
        return False

    def diff(self, other):
        """
        Return a dictionary containing the differences between two metadata objects.
        """
        differences = defaultdict(dict)
        if not isinstance(other, self.__class__):
            differences["type"] = (self.__class__, other.__class__)
        else:
            if self.id != other.id:
                differences["id"] = (self.id, other.id)
            for prop in self.properties:
                assert prop.intrinsic
                val_self = getattr(self, prop.name)
                val_other = getattr(other, prop.name)
                if val_self != val_other:
                    differences["properties"][prop.name] = (val_self, val_other)
        return differences

    def exists(self, client: KGClient) -> bool:
        """Check if this object already exists in the KnowledgeGraph"""

        if self.id:
            # Since the KG now allows user-specified IDs we can't assume that the presence of
            # an id means the object exists
            data = client.instance_from_full_uri(
                self.id, use_cache=True, scope=self.scope or "any", require_full_data=False
            )
            if self._raw_remote_data is None:
                self._raw_remote_data = data
            obj_exists = bool(data)
            if obj_exists:
                self._update_empty_properties(data, client)  # also updates `remote_data`
            return obj_exists
        else:
            try:
                query_filter = self._build_existence_query()
            except CannotBuildExistenceQuery:
                return False

            if query_filter is None:
                # if there's no existence query and no ID, we allow
                # duplicate entries
                return False
            else:
                query_cache_key = generate_cache_key(query_filter)
                if query_cache_key in save_cache[self.__class__]:
                    # Because the KnowledgeGraph is only eventually consistent, an instance
                    # that has just been written to the KG may not appear in the query.
                    # Therefore we cache the query when creating an instance and
                    # where exists() returns True
                    self.id = save_cache[self.__class__][query_cache_key]
                    cached_obj = object_cache.get(self.id)
                    if cached_obj and cached_obj.remote_data:
                        self._raw_remote_data = cached_obj._raw_remote_data
                        self.remote_data = cached_obj.remote_data  # copy or update needed?
                    return True

                query = self.__class__.generate_query(
                    space=None,
                    client=client,
                    filters=query_filter,
                )
                instances = client.query(query=query, size=1, scope="any").data

                if instances:
                    self.id = instances[0]["@id"]
                    assert isinstance(self.id, str)
                    save_cache[self.__class__][query_cache_key] = self.id
                    self._update_empty_properties(instances[0], client)  # also updates `remote_data`
                return bool(instances)

    def modified_data(self) -> JSONdict:
        """
        Return a dict containing the properties that have been modified locally
        from the values originally obtained from the Knowledge Graph.
        """
        current_data = self.to_jsonld(include_empty_properties=True, follow_links=False)
        modified_data = {}
        for key, current_value in current_data.items():
            if not key.startswith("@"):
                assert key.startswith("http")  # keys should all be expanded by this point
                assert self.remote_data is not None
                remote_value = self.remote_data.get(key, None)
                if current_value != remote_value:
                    modified_data[key] = current_value
        return modified_data

    def save(
        self,
        client: KGClient,
        space: Optional[str] = None,
        recursive: bool = True,
        activity_log: Optional[ActivityLog] = None,
        replace: bool = False,
        ignore_auth_errors: bool = False,
    ):
        """
        Store the current object in the Knowledge Graph, either updating an existing instance
        or creating a new one as appropriate.

        Args:
            client: KGClient object that handles the communication with the KG.
            space (str, optional): The KG space to save the object in. If not provided, a default space is used depending on the object type.
            recursive (bool, optional): Whether to recursively save any children of this object. Defaults to True.
            activity_log (ActivityLog, optional): An `ActivityLog` instance to log the operations performed during the save operation.
                This is particularly helpful with `recursive=True`.
            replace (bool, optional): Whether to completely replace an existing KG instance with this one, or just update the existing object
                with any modified properties. Defaults to False.
            ignore_auth_errors (bool, optional): Whether to continue silently when encountering authentication errors. Defaults to False.

        Raises:
            - An `AuthorizationError` if the current user is not authorized to perform the requested operation.

        """
        if recursive:
            for prop in self.properties:
                assert prop.intrinsic
                # we do not save reverse properties, those objects must be saved separately
                # this could be revisited, but we'll have to be careful about loops
                # if saving recursively
                values = getattr(self, prop.name)
                for value in as_list(values):
                    if isinstance(value, ContainsMetadata):
                        target_space: Optional[str]
                        if value.space:
                            target_space = value.space
                        elif (
                            isinstance(value, KGObject)
                            and value.__class__.default_space == "controlled"
                            and value.exists(client)
                            and value.space == "controlled"
                        ):
                            continue
                        elif space is None and self.space is not None:
                            target_space = self.space
                        else:
                            target_space = space
                        if target_space == "controlled":
                            assert isinstance(value, KGObject)  # for type checking
                            if value.exists(client) and value.space == "controlled":
                                continue
                            else:
                                raise AuthorizationError("Cannot write to controlled space")
                        value.save(
                            client,
                            space=target_space,
                            recursive=True,
                            activity_log=activity_log,
                        )
        if space is None:
            if self.space is None:
                space = self.__class__.default_space
            else:
                space = self.space
        logger.info(f"Saving a {self.__class__.__name__} in space {space}")
        if self.exists(client):
            if not self.allow_update:
                logger.info(f"  - not updating {self.__class__.__name__}(id={self.id}), update not allowed by user")
                if activity_log:
                    activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
            else:
                # update
                local_data = self.to_jsonld()
                if replace:
                    logger.info(f"  - replacing - {self.__class__.__name__}(id={self.id})")
                    if activity_log:
                        activity_log.update(item=self, delta=local_data, space=space, entry_type="replacement")
                    try:
                        client.replace_instance(self.uuid, local_data)
                        # what does this return? Can we use it to update `remote_data`?
                    except AuthorizationError as err:
                        if ignore_auth_errors:
                            logger.error(str(err))
                        else:
                            raise
                    else:
                        self.remote_data = local_data
                else:
                    modified_data = self.modified_data()
                    if modified_data:
                        logger.info(
                            f"  - updating - {self.__class__.__name__}(id={self.id}) - properties changed: {modified_data.keys()}"
                        )
                        skip_update = False
                        if "vocab:storageSize" in modified_data:
                            warn("Removing storage size from update because this prop is currently locked by the KG")
                            modified_data.pop("vocab:storageSize")
                            skip_update = len(modified_data) == 0

                        if skip_update:
                            if activity_log:
                                activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
                        else:
                            try:
                                client.update_instance(self.uuid, modified_data)
                            except AuthorizationError as err:
                                if ignore_auth_errors:
                                    logger.error(str(err))
                                else:
                                    raise
                            else:
                                self.remote_data = local_data
                            if activity_log:
                                activity_log.update(
                                    item=self,
                                    delta=modified_data,
                                    space=space,
                                    entry_type="update",
                                )
                    else:
                        logger.info(f"  - not updating {self.__class__.__name__}(id={self.id}), unchanged")
                        if activity_log:
                            activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
        else:
            # create new
            local_data = self.to_jsonld()
            logger.info("  - creating instance with data {}".format(local_data))
            try:
                instance_data = client.create_new_instance(
                    local_data, space or self.__class__.default_space, instance_id=self.uuid
                )
            except (AuthorizationError, ResourceExistsError) as err:
                if ignore_auth_errors:
                    logger.error(str(err))
                    if activity_log:
                        activity_log.update(
                            item=self,
                            delta=local_data,
                            space=self.space,
                            entry_type="create-error",
                        )
                else:
                    raise
            else:
                self.id = instance_data["@id"]
                self._raw_remote_data = instance_data
                self.remote_data = local_data
                if activity_log:
                    activity_log.update(item=self, delta=instance_data, space=self.space, entry_type="create")
        # not handled yet: save existing object to new space - requires changing uuid
        if self.id:
            logger.debug("Updating cache for object {}. Current state: {}".format(self.id, self.to_jsonld()))
            object_cache[self.id] = self
        else:
            logger.warning("Object has no id - see log for the underlying error")

    def delete(self, client: KGClient, ignore_not_found: bool = True):
        """Delete the current metadata object from the KG.

        If `ignore_not_found` is False, an exception will be raised if the object does
        not exist. Otherwise, the method will finish silently.
        """
        client.delete_instance(self.uuid, ignore_not_found=ignore_not_found)
        if self.id in object_cache:
            object_cache.pop(self.id)

    @classmethod
    def by_name(
        cls,
        name: str,
        client: KGClient,
        match: str = "equals",
        all: bool = False,
        space: Optional[str] = None,
        scope: str = "released",
        follow_links: Optional[Dict[str, Any]] = None,
    ) -> Union[KGObject, List[KGObject], None]:
        """
        Retrieve an instance from the Knowledge Graph based on its name.

        Note that not all metadata classes have a name property.

        Args:
            name (str): a string to search for in the name property.
            client: a KGClient
            match (str, optional): either "equals" (exact match - default) or "contains".
            all (bool, optional): Whether to return all objects that match the name, or only the first. Defaults to False.
            space (str, optional): the KG space to search in. Default is to search in all available spaces.
            scope (str, optional): The scope of the search. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        # todo: move this to openminds generation, and include only in those subclasses
        # that have a name
        # todo: also count 'lookup_name', "family_name", "given_name" as a name
        objects = cls.list(client, space=space, scope=scope, api="query", name=name, follow_links=follow_links)
        if match == "equals":
            objects = [obj for obj in objects if hasattr(obj, "name") and obj.name == name]
        if len(objects) == 0:
            return None
        elif len(objects) == 1:
            return objects[0]
        elif all:
            return objects
        else:
            warn("Multiple objects with the same name, returning the first. " "Use 'all=True' to retrieve them all")
            return objects[0]

    def show(self, max_width: Optional[int] = None, include_empty_properties=False):
        """
        Print a table showing the metadata contained in this object.
        """
        if not have_tabulate:
            raise Exception("You need to install the tabulate module to use the `show()` method")
        data = [
            ("id", str(self.id)),
            ("space", str(self.space)),
            ("type", self.type_),
        ]
        for prop in self.__class__.all_properties:
            value = getattr(self, prop.name, None)
            if include_empty_properties or not isinstance(value, (type(None), KGQuery)):
                data.append((prop.name, str(value)))
        if max_width:
            value_column_width = max_width - max(len(item[0]) for item in data)

            def fit_column(value):
                strv = value
                if len(strv) > value_column_width:
                    strv = strv[: value_column_width - 4] + " ..."
                return strv

            data = [(k, fit_column(v)) for k, v in data]
        print(tabulate(data, tablefmt="plain"))
        # return tabulate(data, tablefmt='html') - also see  https://bitbucket.org/astanin/python-tabulate/issues/57/html-class-options-for-tables

    @classmethod
    def generate_query(
        cls,
        client: KGClient,
        space: Union[str, None],
        filters: Optional[Dict[str, Any]] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        label: Optional[str] = None,
    ) -> Union[Dict[str, Any], None]:
        """
        Generate a KG query definition as a JSON-LD document.

        Args:
            client: KGClient object that handles the communication with the KG.
            space (str, optional): if provided, restrict the query to metadata stored in the given KG space.
            filters (dict): A dictonary defining search parameters for the query.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            label (str, optional): a label for the query

        Returns:
            A JSON-LD document containing the KG query definition.

        """
        if space == "myspace":
            real_space = client._private_space
        else:
            real_space = space

        if filters:
            normalized_filters = cls.normalize_filter(expand_filter(filters))
        else:
            normalized_filters = None
        # first pass, we build the basic structure
        query = Query(
            node_type=cls.type_,
            label=label,
            space=real_space,
            properties=cls.generate_query_properties(follow_links),
        )
        # second pass, we add filters
        query.properties.extend(cls.generate_query_filter_properties(normalized_filters))
        # third pass, we add sorting, which can only happen at the top level
        for prop in query.properties:
            if prop.name in ("vocab:name", "vocab:fullName", "vocab:lookupLabel"):
                prop.sorted = True
        # implementation note: the three-pass approach generates queries that are sometimes more verbose
        #                      than necessary, but it makes the logic easier to understand.
        return query.serialize()

    def children(
        self, client: KGClient, follow_links: Optional[Dict[str, Any]] = None
    ) -> List[RepresentsSingleObject]:
        """Return a list of child objects."""
        if follow_links:
            self.resolve(client, follow_links=follow_links)
        all_children = []
        for prop in self.properties:
            assert prop.intrinsic
            if prop.is_link:
                children = as_list(getattr(self, prop.name))
                all_children.extend(children)
                if follow_links:
                    for child in children:
                        all_children.extend(child.children(client))
        return all_children

    def export(self, path: str, single_file: bool = False):
        """
        Export metadata as files in JSON-LD format.

        If any objects do not have IDs, these will be generated.

        If `single_file` is False, then `path` must be the path to a directory,
        and each object will be exported as a file named for the object ID.

        If `single_file` is True, then `path` should be the path to a file
        with extension ".jsonld". This file will contain metadata for all objects.
        """
        raise NotImplementedError("todo")
