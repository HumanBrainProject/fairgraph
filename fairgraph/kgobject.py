"""
This module provides the KGObject class, which is the base class
for representations of structured metadata that have a globally
unique identifier (a URI).
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
from collections import defaultdict
from contextvars import ContextVar
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

from openminds.registry import lookup_type
from openminds import IRI, LinkedMetadata
from openminds.base import LinkedNodeEmbedding

from .utility import expand_uri, as_list, expand_filter, ActivityLog, normalize_data, handle_scope_keyword
from .queries import Query, QueryProperty, Regex
from .errors import AuthorizationError, ResourceExistsError, CannotBuildExistenceQuery, KGConnectionError
from .caching import generate_cache_key
from .base import ErrorHandling, Releasable, JSONdict
from .utility.name_matching import (
    KG_NAMELIKE_PROPERTIES,
    MATCH_TYPES,
    build_name_regex,
    names_equivalent,
    narrow_by_name,
)
from .node import KGNode, check_existence_match
from .kgproxy import KGProxy
from .kgquery import KGQuery

if TYPE_CHECKING:
    from .properties import Property
    from .client import KGClient


logger = logging.getLogger("fairgraph")

# Number of results requested by existence queries, which must be more than one, to detect duplicates.
# If more instances match, they are all retrieved in a second query.
EXISTENCE_QUERY_SIZE = 2

# Set while deserializing a document read with `ignore_unexpected_keys=True`, so that the linked nodes
# embedded in it, which openMINDS deserializes with the default, are read in the same way.
_ignoring_unexpected_keys: ContextVar[bool] = ContextVar("_ignoring_unexpected_keys", default=False)


class KGObject(KGNode, Releasable):
    """
    Base class for Knowledge Graph objects.

    Should not be instantiated directly, intended to be subclassed.
    """

    existence_query_properties: Tuple[str, ...] = ("name",)
    # Note that this default value of existence_query_properties should in
    # many cases be over-ridden.
    # It assumes that "name" is unique within instances of a given type,
    # which may often not be the case.
    sort_property: Optional[str] = None
    # The property by which results of KG queries are sorted, if any.
    # Set in the generated subclasses; see builder/update_openminds.py

    def __init__(
        self,
        id: Optional[str] = None,
        data: Optional[JSONdict] = None,
        space: Optional[str] = None,
        release_status: Optional[str] = None,
        **properties,
    ):
        self.id = id
        self._space = space
        self.release_status = release_status
        self.allow_update = True
        super().__init__(data=data, **properties)

        self._raw_remote_data = None
        self.remote_data = {}
        if self.id and self.id.startswith("http"):
            # we store the original remote data in `_raw_remote_data`
            # and a normalized version in `remote_data`
            self._raw_remote_data = data  # for debugging
            if data:
                try:
                    self.remote_data = normalize_data(
                        self.to_jsonld(include_empty_properties=False, embed_linked_nodes=LinkedNodeEmbedding.NEVER),
                        data.get("@context", self.context),
                    )
                except ValueError as err:
                    # ideally, we should handle errors at the level of individual properties
                    # but that requires some changes to openMINDS-Python
                    ErrorHandling.handle_violation(self.error_handling, str(err))
                    self.remote_data = None

    def __repr__(self):
        template_parts = (
            "{}={{self.{}!r}}".format(prop.name, prop.name)
            for prop in self.__class__.all_properties
            if getattr(self, prop.name, None) is not None
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
    def from_jsonld(
        cls, data: JSONdict, ignore_unexpected_keys: Optional[bool] = False, release_status: Optional[str] = None
    ) -> KGObject:
        """
        Create an instance of the class from a JSON-LD document.

        By default, a NameError is raised if the document contains keys that are neither properties
        of this class nor "@context", "@id" or "@type", which catches mistakes in documents written by hand.
        Documents from the Knowledge Graph contain other keys (e.g. the space), so fairgraph
        always reads them with `ignore_unexpected_keys=True`, and you should too.
        The choice applies to the whole document, including any linked nodes embedded in it.
        """
        if ignore_unexpected_keys:
            token = _ignoring_unexpected_keys.set(True)
            try:
                deserialized_data = cls._deserialize_data(data, include_id=True)
            finally:
                _ignoring_unexpected_keys.reset(token)
        else:
            if not _ignoring_unexpected_keys.get():
                cls._check_for_unexpected_keys(data)
            deserialized_data = cls._deserialize_data(data, include_id=True)
        return cls(id=data.get("@id", None), data=data, release_status=release_status, **deserialized_data)

    @classmethod
    def _check_for_unexpected_keys(cls, data: JSONdict):
        expected_paths = {expand_uri(prop.path, cls.context) for prop in cls.all_properties}
        unexpected = []
        for key in data:
            if key in ("@context", "@id", "@type"):
                continue
            try:
                expanded_key = expand_uri(key, cls.context)
            except ValueError:  # a prefix that is not in the context
                expanded_key = key
            if expanded_key not in expected_paths:
                unexpected.append(key)
        if unexpected:
            raise NameError(f"Unexpected arguments for {cls}: {tuple(unexpected)}")

    @classmethod
    def from_uri(
        cls,
        uri: str,
        client: KGClient,
        use_cache: bool = True,
        release_status: str = "released",
        scope: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        with_reverse_properties: Optional[bool] = False,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its URI.

        Args:
            uri (str): long-form identifier for the KG instance (a full URI)
            client: a KGClient
            release_status (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            with_reverse_properties (bool): Whether to get the values of reverse properties (links to this object
                from other objects) as `KGProxy` objects (or None if there are none). Only has an effect together with `follow_links`.
                Otherwise, each reverse property holds a `KGQuery`, which is only sent when you call its
                `resolve()` method. To get resolved objects, name the reverse property in `follow_links` instead.
                Defaults to False.
        """
        release_status = handle_scope_keyword(scope, release_status)
        if follow_links:
            query = cls.generate_query(
                space=None,
                client=client,
                filters=None,
                follow_links=follow_links,
                with_reverse_properties=with_reverse_properties,
            )
            results = client.query(
                query, instance_id=client.uuid_from_uri(uri), size=1, release_status=release_status
            ).data
            if results:
                data = results[0]
            else:
                data = None
        else:
            data = client.instance_from_full_uri(uri, use_cache=use_cache, release_status=release_status)
        if data is None:
            return None
        else:
            return cls.from_jsonld(data, ignore_unexpected_keys=True, release_status=release_status)

    @classmethod
    def from_uuid(
        cls,
        uuid: str,
        client: KGClient,
        use_cache: bool = True,
        release_status: str = "released",
        scope: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        with_reverse_properties: Optional[bool] = False,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its UUID.

        Args:
            uuid (str): short-form identifier for the KG instance (a UUID).
            client: a KGClient
            release_status (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            with_reverse_properties (bool): Whether to get the values of reverse properties (links to this object
                from other objects) as `KGProxy` objects (or None if there are none). Only has an effect together with `follow_links`.
                Otherwise, each reverse property holds a `KGQuery`, which is only sent when you call its
                `resolve()` method. To get resolved objects, name the reverse property in `follow_links` instead.
                Defaults to False.

        """
        release_status = handle_scope_keyword(scope, release_status)
        logger.info("Attempting to retrieve {} with uuid {}".format(cls.__name__, uuid))
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        try:
            val = UUID(uuid, version=4)  # check validity of uuid
        except ValueError as err:
            raise ValueError("{} - {}".format(err, uuid))
        uri = cls.uri_from_uuid(uuid, client)
        return cls.from_uri(
            uri,
            client,
            use_cache=use_cache,
            release_status=release_status,
            follow_links=follow_links,
            with_reverse_properties=with_reverse_properties,
        )

    @classmethod
    def from_id(
        cls,
        id: str,
        client: KGClient,
        use_cache: bool = True,
        release_status: str = "released",
        scope: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        with_reverse_properties: Optional[bool] = False,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on either its URI or UUID.

        Args:
            id (str): short-form (UUID) or long-form (URI) identifier for the KG instance.
            client: a KGClient
            release_status (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            use_cache (bool): Whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            with_reverse_properties (bool): Whether to get the values of reverse properties (links to this object
                from other objects) as `KGProxy` objects (or None if there are none). Only has an effect together with `follow_links`.
                Otherwise, each reverse property holds a `KGQuery`, which is only sent when you call its
                `resolve()` method. To get resolved objects, name the reverse property in `follow_links` instead.
                Defaults to False.

        Returns:
            Either a KGObject of the correct type, or None.
            A return value of None means either the object doesn't exist
            or the user doesn't have permission to access it.
        """
        release_status = handle_scope_keyword(scope, release_status)
        if hasattr(cls, "type_") and cls.type_:
            if id.startswith("http"):
                fn = cls.from_uri
            else:
                fn = cls.from_uuid
            return fn(
                id,
                client,
                use_cache=use_cache,
                release_status=release_status,
                follow_links=follow_links,
                with_reverse_properties=with_reverse_properties,
            )
        else:
            # if we don't know the type
            if id.startswith("http"):
                uri = id
            else:
                uri = client.uri_from_uuid(id)
            if follow_links is not None:
                raise NotImplementedError
            data = client.instance_from_full_uri(uri, use_cache=use_cache, release_status=release_status)
            if data is None:
                return None
            type_ = data["@type"]
            if isinstance(type_, list):
                assert len(type_) == 1
                type_ = type_[0]
            cls_from_data = lookup_type(type_, client.openminds_version)
            return cls_from_data.from_jsonld(data, ignore_unexpected_keys=True, release_status=release_status)

    @classmethod
    def from_alias(
        cls,
        alias: str,
        client: KGClient,
        space: Optional[str] = None,
        release_status: str = "released",
        scope: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Retrieve an instance from the Knowledge Graph based on its alias/short name.

        Note that not all metadata classes have an alias.

        Args:
            alias (str): a short name used to identify a KG instance.
            client: a KGClient
            space (str, optional): the KG space to look in. Default is to look in all available spaces.
            release_status (str, optional): The scope of the lookup. Valid values are "released", "in progress", or "any".
                Defaults to "released".
            follow_links (dict): The links in the graph to follow. Defaults to None.

        """
        release_status = handle_scope_keyword(scope, release_status)
        # todo: move this to openminds generation, and include only in those subclasses
        # that have a short_name property
        if "short_name" not in cls.property_names:
            raise AttributeError(f"{cls.__name__} doesn't have an 'alias' or 'short_name' property")
        candidates = as_list(
            cls.list(
                client,
                size=20,
                from_index=0,
                api="query",
                release_status=release_status,
                space=space,
                short_name=alias,
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
        release_status: str = "released",
        scope: Optional[str] = None,
        space: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
        with_reverse_properties: Optional[bool] = False,
        **filters,
    ) -> List[KGObject]:
        """
        List all objects of this type in the Knowledge Graph

        Filtering on a link to a node is slow for types with very many instances, above all `File`,
        and can fail with a `KGConnectionError`. It is often much faster to start from the node
        at the other end of the link and follow it with `follow_links`. For example, to get the files
        in a dataset version's repository, use

            DatasetVersion.from_id(dataset_version_id, client, follow_links={"repository": {"files": {}}})

        rather than `File.list(client, file_repository=repository)`.

        Args:
            client: KGClient object that handles the communication with the KG.
            size (int, optional): The maximum number of instances to return. Default is 100.
            from_index (int, optional): The index of the first instance to return. Default is 0.
            api (str): The KG API to use for the query. Can be 'query', 'core', or 'auto'. Default is 'auto'.
            release_status (str, optional): The scope to use for the query. Can be 'released', 'in progress', or 'all'. Default is 'released'.
            space (str, optional): The KG space to be queried. If not specified, results from all accessible spaces will be included.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            with_reverse_properties (bool): Whether to get the values of reverse properties (links to this object
                from other objects) as `KGProxy` objects (or None if there are none). Only has an effect when the query API is used (with `follow_links` or filters, or with `api="query"`).
                Otherwise, each reverse property holds a `KGQuery`, which is only sent when you call its
                `resolve()` method. To get resolved objects, name the reverse property in `follow_links` instead.
                Defaults to False.
            filters: Optional keyword arguments representing filters to apply to the query.

        Returns:
            A list of instances of this class representing the objects returned by the KG query.
            With the query API, results are sorted in ascending order, ignoring case, by the property
            named in the class's `sort_property` attribute, if it has one.
            The core API does not sort results, and is used by default when there are no filters and
            no `follow_links`: pass `api="query"` for sorted results.

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
        release_status = handle_scope_keyword(scope, release_status)

        if api == "auto":
            if filters or follow_links:
                api = "query"
            else:
                api = "core"

        if api == "query":
            query = cls.generate_query(
                space=space,
                client=client,
                filters=filters,
                follow_links=follow_links,
                with_reverse_properties=with_reverse_properties,
            )
            instances = client.query(
                query=query,
                from_index=from_index,
                size=size,
                release_status=release_status,
            ).data
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            if follow_links:
                raise NotImplementedError("Following links with api='core' not yet implemented")
            instances = client.list(
                cls.type_, space=space, from_index=from_index, size=size, release_status=release_status
            ).data
        else:
            raise ValueError("'api' must be either 'query', 'core', or 'auto'")
        return [
            cls.from_jsonld(data=instance, ignore_unexpected_keys=True, release_status=release_status)
            for instance in instances
        ]

    @classmethod
    def count(
        cls,
        client: KGClient,
        api: str = "auto",
        release_status: str = "released",
        scope: Optional[str] = None,
        space: Optional[str] = None,
        **filters,
    ) -> int:
        """
        Count the number of objects of a given type and (optionally) matching a given set of filters.

        Args:
            client: KGClient object that handles the communication with the KG.
            api (str): The KG API to use for the query. Can be 'query', 'core', or 'auto'. Default is 'auto'.
            release_status (str, optional): The scope to use for the query. Can be 'released', 'in progress', or 'all'. Default is 'released'.
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
        release_status = handle_scope_keyword(scope, release_status)
        if api == "auto":
            if filters:
                api = "query"
            else:
                api = "core"
        if api == "query":
            query = cls.generate_query(space=space, client=client, filters=filters)
            response = client.query(query=query, from_index=0, size=1, release_status=release_status)
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            response = client.list(cls.type_, space=space, release_status=release_status, from_index=0, size=1)
        return response.total

    def _update_empty_properties(self, data: JSONdict):
        """
        Replace any empty properties (value None) with the supplied data
        unless the property was deliberately set to None.
        """
        cls = self.__class__
        locally_modified = self.modified_data()
        deserialized_data = cls._deserialize_data(data, include_id=True)
        for prop in cls.all_properties:
            expanded_path = expand_uri(prop.path, cls.context)
            if expanded_path not in locally_modified:
                current_value = getattr(self, prop.name, None)
                if current_value is None:
                    value = deserialized_data.get(prop.name, None)
                    if value is not None:
                        setattr(self, prop.name, value)
        assert self.remote_data is not None
        for key, value in data.items():
            if not (key.startswith("Q") or key == "@context"):
                expanded_path = expand_uri(key, cls.context)
                assert isinstance(expanded_path, str)
                self.remote_data[expanded_path] = data[key]
        if self.space is None and "https://core.kg.ebrains.eu/vocab/meta/space" in data:
            self._space = data["https://core.kg.ebrains.eu/vocab/meta/space"]

    def __eq__(self, other):
        return not self.__ne__(other)

    # Defining __eq__ would otherwise make instances unhashable, and openMINDS' by_name(),
    # which we delegate to, de-duplicates its results with dict.fromkeys(), which hashes by identity.
    __hash__ = object.__hash__

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        if self.id and other.id and self.id != other.id:
            return True
        for prop in self.properties:
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
                val_self = getattr(self, prop.name)
                val_other = getattr(other, prop.name)
                if val_self != val_other:
                    differences["properties"][prop.name] = (val_self, val_other)
        return differences

    def exists(
        self,
        client: KGClient,
        ignore_duplicates: bool = False,
        in_spaces: Optional[List[str]] = None,
        existence_match: str = "equals",
    ) -> bool:
        """
        Check if this object already exists in the KnowledgeGraph.

        Args:
            client: KGClient object that handles the communication with the KG.
            ignore_duplicates (bool, optional): Whether to ignore the existence of multiple objects with the same properties
                (and consider only the first in the list), or to raise an Exception. Defaults to False.
            in_spaces (list of str, optional): If provided, only look for the object in these spaces.
            existence_match (str, optional): How string properties are compared when looking for the object.
                Either "equals" (the value in the KG must be the same as the local value, ignoring case - the default),
                "contains" (it is enough for the value in the KG to contain the local value,
                so an object with the name "FOO" will match an existing object with the name "FOO-BAR"),
                or "normalized" (the values must be the same, ignoring case, accents and differences in whitespace,
                so "Emilie du  Chatelet" will match "Émilie du Châtelet"). If several instances match
                with "normalized", but only one of them matches exactly (ignoring case), that one is used.
                Some classes also look for a match in other ways with "normalized";
                for example, `Person` first looks for a person with the same ORCID.
        """
        check_existence_match(existence_match)
        obj_exists = self._exists_without_query(client, existence_match)
        if obj_exists is not None:
            return obj_exists
        instances = self._find_matching_instances(client, in_spaces=in_spaces, existence_match=existence_match)
        if not instances:
            return False
        self._check_for_duplicates(instances, ignore_duplicates, existence_match)
        return self._use_matching_instance(client, instances[0], existence_match)

    def _existence_cache_keys(self, existence_match: str) -> List[Tuple]:
        """
        The keys under which the save cache may hold the ID of an object matching this one.

        An object that matches exactly also matches with "contains" or "normalized", but not the other way round,
        so a "contains" or "normalized" lookup may use either key while an "equals" lookup may use only the first.
        """
        equals_key = generate_cache_key(self._build_existence_query("equals"))
        if existence_match == "equals":
            return [equals_key]
        return [equals_key, equals_key + (existence_match,)]

    def _exists_without_query(self, client: KGClient, existence_match: str = "equals") -> Optional[bool]:
        """
        Check if this object exists in the KG, where this can be determined without an existence query,
        i.e. if the object has an ID, if there is no existence query, or if the object is found in the save cache.

        Returns True or False if this could be determined, None if an existence query is needed.
        """
        if self.id and self.id.startswith("http"):
            # Since the KG now allows user-specified IDs we can't assume that the presence of
            # an id means the object exists
            data = client.instance_from_full_uri(
                self.id, use_cache=True, release_status=self.release_status or "any", require_full_data=False
            )
            if self._raw_remote_data is None:
                self._raw_remote_data = data
            obj_exists = bool(data)
            if obj_exists:
                self._update_empty_properties(data)  # also updates `remote_data`
            return obj_exists

        try:
            query_filter = self._build_existence_query(existence_match)
        except CannotBuildExistenceQuery:
            return False
        if query_filter is None:
            # if there's no existence query and no ID, we allow
            # duplicate entries
            return False

        existence_cache = client._existence_cache[self.__class__]
        query_cache_key = next(
            (key for key in self._existence_cache_keys(existence_match) if key in existence_cache), None
        )
        if query_cache_key is not None:
            # Because the KnowledgeGraph is only eventually consistent, an instance
            # that has just been written to the KG may not appear in the query.
            # Therefore we cache the query when creating an instance and
            # where exists() returns True
            self.id = existence_cache[query_cache_key]
            data = client.instance_from_full_uri(self.id, release_status="any", require_full_data=False)
            # If the instance is not found, we still treat it as existing, in case retrieving
            # a newly-created instance by its id is also subject to delays.
            # Instances deleted with this client are no longer in the existence cache.
            if data:
                if self._raw_remote_data is None:
                    self._raw_remote_data = data
                # this also updates `self.remote_data`. It must not be replaced by a
                # direct assignment to `self.remote_data`: a property that is empty
                # locally but present remotely would then look like a deliberate
                # deletion, and be set to null by the next call to save().
                self._update_empty_properties(data)
                self._adopt_matched_values(data, existence_match)
            return True
        return None

    def _find_matching_instances(
        self, client: KGClient, in_spaces: Optional[List[str]] = None, existence_match: str = "equals"
    ) -> List[JSONdict]:
        """
        Look for instances in the KG that match this object, and return them, best match first.

        Each instance is returned as a dict containing at least its "@id" and its space
        (under the key "https://schema.hbp.eu/myQuery/space"), as returned by a query generated
        by `generate_minimal_query()`.
        If there is more than one, `exists()` and `save()` raise an exception unless `ignore_duplicates` is True.

        This is called by `exists()` and `save()` when the object has no ID and is not in the save cache.
        By default, it runs the existence query built from `existence_query_properties`
        (see `_build_existence_query()`), and, with `existence_match="normalized"`, checks the instances found.
        Subclasses may override it to look for matches in other ways, calling the superclass method
        to fall back on the existence query (see, for example, `Person`).

        If the connection is lost while querying, an empty list is returned, with a warning.
        """
        instances = self._run_existence_query(client, in_spaces=in_spaces, existence_match=existence_match)
        if existence_match == "normalized":
            instances = self._confirm_normalized_matches(client, instances)
        return instances

    def _find_by_identifiers(
        self, client: KGClient, identifier_types: Tuple[str, ...], in_spaces: Optional[List[str]] = None
    ) -> List[JSONdict]:
        """
        Look for instances in the KG that share one of this object's digital identifiers, considering
        only those identifiers whose class name is in `identifier_types` (e.g. ("ORCID",)).

        An identifier with no ID is first looked for in the KG (by its `identifier` value);
        if it is not there, no instance can share it.
        An identifier with a local ID (one that is not a KG URI, e.g. "_:000012" in a `Collection` that has not
        been uploaded) is skipped, since no instance in the KG can link to it.
        Returns the instances found, as `_find_matching_instances()` does, for the first identifier that has any.
        """
        for item in as_list(getattr(self, "digital_identifiers", None)):
            if isinstance(item, KGProxy):
                if not any(cls.__name__ in identifier_types for cls in item.classes):
                    continue
            elif isinstance(item, KGObject) and item.__class__.__name__ in identifier_types:
                # if the identifier itself is duplicated in the KG, we try only the first copy
                if not item.id and not item.exists(client, ignore_duplicates=True):
                    continue
            else:
                continue
            identifier_id = item.id
            if not (identifier_id and identifier_id.startswith("http")):
                continue
            instances = self._run_minimal_query(client, {"digital_identifiers": identifier_id}, in_spaces=in_spaces)
            if instances:
                return instances
        return []

    def _confirm_normalized_matches(self, client: KGClient, instances: List[JSONdict]) -> List[JSONdict]:
        """
        From the instances found by a "normalized" existence query, which is only a pre-filter, keep those whose
        string values really are equivalent to the local ones (see `names_equivalent()`).

        If exactly one of these also matches exactly (ignoring case, as with `existence_match="equals"`),
        only that one is returned.
        """
        local_values = {
            property_name: getattr(self, property_name, None)
            for property_name in self.existence_query_properties or ()
            if isinstance(getattr(self, property_name, None), str)
        }
        if not local_values:
            return instances
        confirmed = []
        exact = []
        for instance in instances:
            data = client.instance_from_full_uri(instance["@id"], use_cache=True, release_status="any")
            if data is None:
                continue
            stored_values = self.__class__._deserialize_data(data)
            pairs = [(stored_values.get(name, None), local) for name, local in local_values.items()]
            if all(isinstance(stored, str) and names_equivalent(stored, local) for stored, local in pairs):
                confirmed.append(instance)
                if all(stored.lower() == local.lower() for stored, local in pairs):
                    exact.append(instance)
        if len(exact) == 1:
            return exact
        return confirmed

    def _run_existence_query(
        self, client: KGClient, in_spaces: Optional[List[str]] = None, existence_match: str = "equals"
    ) -> List[JSONdict]:
        """
        Run the existence query for this object, and return all matching instances
        (their "@id" and space only).

        If the connection is lost while querying, an empty list is returned, with a warning.
        """
        query_filter = self._build_existence_query(existence_match)
        return self._run_minimal_query(client, query_filter, in_spaces=in_spaces)

    def _run_minimal_query(
        self, client: KGClient, query_filter: Dict[str, Any], in_spaces: Optional[List[str]] = None
    ) -> List[JSONdict]:
        """
        Run a query with the given filters, which returns only the "@id" and space of the instances found,
        and return all of them.

        If the connection is lost while querying, an empty list is returned, with a warning.
        """
        query = self.__class__.generate_minimal_query(client=client, filters=query_filter)
        try:
            response = client.query(
                query=query, size=EXISTENCE_QUERY_SIZE, release_status="any", restrict_to_spaces=in_spaces
            )
            instances = response.data or []
            if response.total > len(instances):
                response = client.query(
                    query=query, size=response.total, release_status="any", restrict_to_spaces=in_spaces
                )
                instances = response.data or []
        except KGConnectionError as err:
            if "RemoteDisconnected" in str(err):
                warn(
                    f"Timeout when checking for existence of object {self}."
                    "Returning False, check for possible creation of duplicate instances."
                )
                return []
            raise
        return instances

    def _check_for_duplicates(
        self, instances: List[JSONdict], ignore_duplicates: bool, existence_match: str = "equals"
    ):
        if len(instances) > 1 and not ignore_duplicates:
            raise Exception(
                f"Existence query is not specific enough. Type: {self.__class__.__name__}; "
                f"filters: {self._build_existence_query(existence_match)}"
            )

    def _use_matching_instance(self, client: KGClient, match: JSONdict, existence_match: str = "equals") -> bool:
        """
        Identify this object with an instance found by the existence query.

        Returns False if the instance could not be retrieved.
        """
        # it seems that sometimes the "query" endpoint returns instances
        # which the "instances" endpoint doesn't know about, so here we double check that
        # the instance can be found
        instance = client.instance_from_full_uri(match["@id"], release_status="any")
        if instance is None:
            return False

        self.id = instance["@id"]
        assert isinstance(self.id, str)
        # the instance's actual location takes precedence over any space set locally
        if "https://schema.hbp.eu/myQuery/space" in match:
            self._space = match["https://schema.hbp.eu/myQuery/space"]
        client._existence_cache[self.__class__][self._existence_cache_keys(existence_match)[-1]] = self.id
        self._update_empty_properties(instance)  # also updates `remote_data`
        self._adopt_matched_values(instance, existence_match)
        return True

    def _adopt_matched_values(self, data: JSONdict, existence_match: str):
        """
        After an existence query has matched this object with the instance in `data`, replace the local value
        of each property in the existence query whose value is a string with the stored one, where the two
        differ only in ways the query ignores: case, and, with `existence_match="contains"`, the rest of the
        stored value, and, with `existence_match="normalized"`, accents and whitespace. Other properties are not changed.

        Otherwise, the difference would count as a local modification, and saving would write the search term
        over the stored value.
        """
        if not self.existence_query_properties:
            return

        stored_values = self.__class__._deserialize_data(data)
        for property_name in self.existence_query_properties:
            local_value = getattr(self, property_name, None)
            stored_value = stored_values.get(property_name, None)
            if not (isinstance(local_value, str) and isinstance(stored_value, str)) or local_value == stored_value:
                continue
            if existence_match == "contains":
                matched = local_value.lower() in stored_value.lower()
            elif existence_match == "normalized":
                matched = names_equivalent(stored_value, local_value)
            else:
                matched = local_value.lower() == stored_value.lower()
            if matched:
                setattr(self, property_name, stored_value)

    def modified_data(self) -> JSONdict:
        """
        Return a dict containing the properties that have been modified locally
        from the values originally obtained from the Knowledge Graph.
        """

        def values_are_equal(local, remote, key=None):
            if key == "@type":
                # The KG returns the type of an embedded object as a list,
                # while to_jsonld() gives a single type as a string.
                return set(as_list(local)) == set(as_list(remote))
            if type(local) != type(remote):
                return False
            if isinstance(local, list):
                if len(local) != len(remote):
                    return False
                return all(values_are_equal(a, b) for a, b in zip(local, remote))
            elif isinstance(local, dict):
                return all(
                    values_are_equal(local[key], remote.get(key, None), key)
                    for key in local.keys()
                    if not (local[key] is None and key not in remote)
                )
            else:
                return local == remote

        current_data = normalize_data(
            self.to_jsonld(include_empty_properties=True, embed_linked_nodes=LinkedNodeEmbedding.IF_NECESSARY),
            self.context,
        )
        modified_data = {}
        for key, current_value in current_data.items():
            if not key.startswith("@"):
                assert key.startswith("http")  # keys should all be expanded by this point
                assert self.remote_data is not None
                remote_value = self.remote_data.get(key, None)
                if not values_are_equal(current_value, remote_value):
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
        ignore_duplicates: bool = False,
        existence_match: str = "equals",
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
            ignore_duplicates (bool, optional): Whether to ignore the existence of multiple objects with the same properties
                (and consider only the first in the list), or to raise an Exception. Defaults to False.
            existence_match (str, optional): How string properties are compared when looking for an existing object
                to update. Either "equals" (the value in the KG must be the same as the local value, ignoring case - the default),
                "contains" (it is enough for the value in the KG to contain the local value,
                so an object with the name "FOO" will overwrite an existing object with the name "FOO-BAR"),
                or "normalized" (the values must be the same, ignoring case, accents and differences in whitespace).
                See `exists()` for details.

        Raises:
            - An `AuthorizationError` if the current user is not authorized to perform the requested operation.

        """
        check_existence_match(existence_match)
        # Done first, so that the existence query, the data that is sent and the comparison with
        # the remote data all use the same values. The object is changed in place on purpose:
        # afterwards it is identical to what is stored in the KG.
        self._normalize_text()
        if recursive:
            for prop in self.properties:
                # We do not save reverse properties, those objects must be saved separately.
                # This could be revisited, but we'll have to be careful about loops
                # if saving recursively
                values = getattr(self, prop.name)
                for value in as_list(values):
                    if isinstance(value, KGNode):
                        target_space: Optional[str]
                        if (
                            isinstance(value, KGObject)
                            and value.__class__.default_space == "controlled"
                            and value.exists(
                                client, ignore_duplicates=ignore_duplicates, existence_match=existence_match
                            )
                            and value.space == "controlled"
                        ):
                            continue
                        elif value.space:
                            target_space = value.space
                        elif space is None and self.space is not None:
                            target_space = self.space
                        else:
                            target_space = space
                        if target_space == "controlled":
                            assert isinstance(value, KGObject)  # for type checking
                            if (
                                value.exists(
                                    client, ignore_duplicates=ignore_duplicates, existence_match=existence_match
                                )
                                and value.space == "controlled"
                            ):
                                continue
                            else:
                                raise AuthorizationError("Cannot write to controlled space")
                        value.save(
                            client,
                            space=target_space,
                            recursive=True,
                            activity_log=activity_log,
                            ignore_duplicates=ignore_duplicates,
                            existence_match=existence_match,
                        )
        if space is None:
            if self.space is None:
                space = self.__class__.default_space
            else:
                space = self.space
        logger.info(f"Saving a {self.__class__.__name__} in space {space}")
        found = self._exists_without_query(client, existence_match)
        if found is None:
            # We look for the object in all spaces, not only the one we are saving to, to avoid creating duplicates,
            # but if it exists both in the target space and elsewhere, we use the instance in the target space.
            instances = self._find_matching_instances(client, existence_match=existence_match)
            candidates = [
                instance for instance in instances if instance.get("https://schema.hbp.eu/myQuery/space") == space
            ] or instances
            if candidates:
                self._check_for_duplicates(candidates, ignore_duplicates, existence_match)
                found = self._use_matching_instance(client, candidates[0], existence_match)
            else:
                found = False
        if found and self.space is not None and self.space != space:
            # An existing instance can only be updated in the space where it lives,
            # so we link to it there rather than creating a duplicate in the requested space.
            warn(
                f"{self.__class__.__name__}(id={self.id}) already exists in space '{self.space}', "
                f"so it will be updated there rather than created in space '{space}'"
            )
            space = self.space
        if found:
            if not self.allow_update:
                logger.info(f"  - not updating {self.__class__.__name__}(id={self.id}), update not allowed by user")
                if activity_log:
                    activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
            else:
                # update
                local_data = normalize_data(
                    self.to_jsonld(include_empty_properties=False, embed_linked_nodes=LinkedNodeEmbedding.NEVER),
                    self.context,
                )
                if replace:
                    logger.info(f"  - replacing - {self.__class__.__name__}(id={self.id})")
                    if activity_log:
                        activity_log.update(item=self, delta=local_data, space=space, entry_type="replacement")
                    try:
                        assert self.uuid is not None
                        client.replace_instance(self.uuid, local_data)
                    except AuthorizationError as err:
                        if ignore_auth_errors:
                            logger.error(str(err))
                        else:
                            raise
                    else:
                        self.remote_data = local_data
                        # Mark the raw server-side document as stale, to match
                        # the cache invalidation done in client.replace_instance.
                        # It will be re-fetched on demand by exists() if needed.
                        self._raw_remote_data = None
                else:
                    modified_data = self.modified_data()
                    if modified_data:
                        logger.info(
                            f"  - updating - {self.__class__.__name__}(id={self.id}) - properties changed: {modified_data.keys()}"
                        )
                        skip_update = False
                        if "storageSize" in modified_data:
                            warn("Removing storage size from update because this prop is currently locked by the KG")
                            modified_data.pop("storageSize")
                            skip_update = len(modified_data) == 0

                        if skip_update:
                            if activity_log:
                                activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
                        else:
                            try:
                                # Note: if modified_data includes embedded objects
                                # then _all_ fields of the embedded objects must be provided,
                                # not only those that have changed.
                                assert self.uuid is not None
                                client.update_instance(self.uuid, modified_data)
                            except AuthorizationError as err:
                                if ignore_auth_errors:
                                    logger.error(str(err))
                                else:
                                    raise
                            else:
                                self.remote_data = local_data
                                # Mark the raw server-side document as stale, to
                                # match the cache invalidation done in
                                # client.update_instance. It will be re-fetched
                                # on demand by exists() if needed.
                                self._raw_remote_data = None
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
            local_data = normalize_data(
                self.to_jsonld(include_empty_properties=False, embed_linked_nodes=LinkedNodeEmbedding.NEVER),
                self.context,
            )
            logger.info("  - creating instance with data {}".format(local_data))
            if self.id and self.id.startswith("http"):
                instance_id = self.uuid
            else:
                instance_id = None
            try:
                instance_data = client.create_new_instance(
                    local_data, space or self.__class__.default_space, instance_id=instance_id
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
                # Because the KnowledgeGraph is only eventually consistent, the new instance
                # may not appear in existence queries straight away, so cache the query here
                # (see exists())
                try:
                    query_filter = self._build_existence_query()
                except CannotBuildExistenceQuery:
                    query_filter = None
                if query_filter is not None:
                    client._existence_cache[self.__class__][generate_cache_key(query_filter)] = self.id
                if activity_log:
                    activity_log.update(item=self, delta=instance_data, space=self.space, entry_type="create")

        # note: if an existing object is in a different space to the one specified here,
        #       it is updated in its own space (with a warning), not moved to the new space.
        if not self.id:
            logger.warning("Object has no id - see log for the underlying error")
        return self.id

    def delete(self, client: KGClient, ignore_not_found: bool = True):
        """Delete the current metadata object from the KG.

        If `ignore_not_found` is False, an exception will be raised if the object does
        not exist. Otherwise, the method will finish silently.
        """
        client.delete_instance(self.uuid, ignore_not_found=ignore_not_found)

    def dump(self, file_path, indent=2):
        """
        Save this object to a file in JSON-LD format.
        """
        LinkedMetadata.save(self, file_path, indent)

    @classmethod
    def by_name(
        cls,
        name: str,
        client: Optional[KGClient] = None,
        match: str = "equals",
        all: bool = False,
        case_sensitive: bool = True,
        ignore_accents: bool = False,
        space: Optional[str] = None,
        release_status: str = "released",
        scope: Optional[str] = None,
        follow_links: Optional[Dict[str, Any]] = None,
    ) -> Union[KGObject, List[KGObject], None]:
        """
        Retrieve metadata objects based on their name, or name-like properties.

        For controlled terms, licences, content types and other classes with an openMINDS instance library,
        call this without `client`: the built-in library is searched, which needs no network access,
        and the objects found can be used directly as links in the Knowledge Graph.
        Only pass `client` to find terms that are newer than the installed openMINDS package.

        "Name-like properties" are "name", "lookup_label", "family_name", "full_name", "short_name", "abbreviation"
        and "synonyms".  If a class has such a property, it will be searched.
        Note that not all metadata classes have a name.

        If no `client` is given, this searches the built-in openMINDS instance library, and the objects found have
        semantic IRIs as their ids, e.g. "https://openminds.om-i.org/instances/species/musMusculus".
        Only classes that have an instance library (controlled terms, licences, content types, ...) can be searched
        this way; for any other class, None is returned.

        If `client` is provided, the Knowledge Graph is searched, and the objects found have UUID-based ids,
        e.g. "https://kg.ebrains.eu/api/instances/d9875ebd-260e-4337-a637-b62fed4aa91d".

        Args:
            name (str): a string to search for.
            client: a KGClient. If not provided, the openMINDS instance library is searched
                instead of the Knowledge Graph.
            match (str, optional): either "equals" (exact match - default), "contains" (the name-like property
                contains the given string), or "within" (the given string contains the name-like property).
            all (bool, optional): Whether to return all objects that match the name, or only the first.
                Defaults to False.
            case_sensitive (bool, optional): Whether the search should be case-sensitive. Defaults to True.
            ignore_accents (bool, optional): Whether to ignore accents (acute, grave, circumflex) and other
                diacritical marks (cedilla, tilde, ring, etc.) when matching. Also treat special letters
                (ß, œ, æ, ø, ł, etc.) as their closest plain-letter equivalents (e.g. "ß" as "ss"). Defaults to False.
            space (str, optional): the KG space to search in. Default is to search in all available spaces.
                Ignored if no client is provided.
            release_status (str, optional): The scope of the search. Valid values are "released", "in progress",
                or "any". Defaults to "released". Ignored if no client is provided.
            follow_links (dict): The links in the graph to follow. Defaults to None. Ignored if no client is provided.

        Raises:
            ValueError: if `match` is not one of "equals", "contains" or "within".
            AttributeError: if a client is provided but the class has no name-like property.

        """
        if match not in MATCH_TYPES:
            raise ValueError("'match' must be either 'equals', 'contains', or 'within'")

        if client is None:
            if not hasattr(cls, "instances"):
                return None  # this class has no instance library to search
            return super().by_name(
                name, match=match, all=all, case_sensitive=case_sensitive, ignore_accents=ignore_accents
            )

        release_status = handle_scope_keyword(scope, release_status)
        # todo: move this to openminds generation, and include only in those subclasses that have a name-like property
        name_properties = [prop_name for prop_name in KG_NAMELIKE_PROPERTIES if prop_name in cls.property_names]
        if not name_properties:
            raise AttributeError(f"{cls.__name__} doesn't have a name-like property")

        # The KG has no way to apply a single filter across several properties, so we query each of them in turn and
        # merge the results.
        # The regular expression is only a pre-filter. It returns a superset of the matches, since the KG's regex
        # matching is always case-insensitive, which is then narrowed down, using the same matching rules as the
        # openMINDS instance-library search.
        pattern = Regex(
            build_name_regex(name, match=match, case_sensitive=case_sensitive, ignore_accents=ignore_accents)
        )
        candidates: Dict[str, KGObject] = {}
        for prop_name in name_properties:
            for obj in cls.list(
                client,
                space=space,
                release_status=release_status,
                api="query",
                follow_links=follow_links,
                **{prop_name: pattern},
            ):
                candidates.setdefault(obj.id, obj)
        objects = narrow_by_name(candidates.values(), name, name_properties, match, case_sensitive, ignore_accents)

        if len(objects) == 0:
            return None
        elif all:
            return objects
        elif len(objects) == 1:
            return objects[0]
        else:
            warn("Multiple objects with the same name, returning the first. " "Use 'all=True' to retrieve them all")
            return objects[0]

    def show(self, max_width: Optional[int] = 120, include_empty_properties=False):
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
        with_reverse_properties: Optional[bool] = False,
        label: Optional[str] = None,
    ) -> Union[Dict[str, Any], None]:
        """
        Generate a KG query definition as a JSON-LD document.

        Args:
            client: KGClient object that handles the communication with the KG.
            space (str, optional): if provided, restrict the query to metadata stored in the given KG space.
            filters (dict): A dictonary defining search parameters for the query.
            follow_links (dict): The links in the graph to follow. Defaults to None.
            with_reverse_properties (bool): Whether to get the values of reverse properties (links to this object
                from other objects) as part of the query, as `KGProxy` objects (or None if there are none).
                Otherwise, each reverse property holds a `KGQuery`, which is only sent when you call its
                `resolve()` method. To get resolved objects, name the reverse property in `follow_links` instead.
                Defaults to False.
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
            properties=cls.generate_query_properties(follow_links, with_reverse_properties),
        )
        # second pass, we add filters
        query.properties.extend(cls.generate_query_filter_properties(normalized_filters))
        # third pass, we add sorting, which the KG allows on only one property, at the top level
        if cls.sort_property:
            sort_path = cls._property_lookup[cls.sort_property].path
            for prop in query.properties:
                if prop.name == sort_path:
                    prop.sorted = True
                    break
        # implementation note: the three-pass approach generates queries that are sometimes more verbose
        #                      than necessary, but it makes the logic easier to understand.
        return query.serialize()

    @classmethod
    def generate_minimal_query(
        cls,
        client: KGClient,
        filters: Optional[Dict[str, Any]] = None,
        label: Optional[str] = None,
    ) -> Union[Dict[str, Any], None]:
        """
        Generate a minimal KG query definition as a JSON-LD document.
        Such a query returns only the @id, @type and space of any instances that are found.

        Args:
            client: KGClient object that handles the communication with the KG.
            filters (dict): A dictonary defining search parameters for the query.
            label (str, optional): a label for the query

        Returns:
            A JSON-LD document containing the KG query definition.

        """
        if filters:
            normalized_filters = cls.normalize_filter(expand_filter(filters))
        else:
            normalized_filters = None
        # first pass, we build the basic structure
        query = Query(
            node_type=cls.type_,
            label=label,
            space=None,
            properties=[
                QueryProperty("https://core.kg.ebrains.eu/vocab/meta/space", name="query:space"),
                QueryProperty("@type"),
            ],
        )
        # second pass, we add filters
        query.properties.extend(cls.generate_query_filter_properties(normalized_filters))
        return query.serialize()

    def children(self, client: KGClient, follow_links: Optional[Dict[str, Any]] = None) -> List[Releasable]:
        """Return a list of child objects."""
        if follow_links:
            self.resolve(client, follow_links=follow_links)
        all_children = []
        for prop in self.properties:
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
