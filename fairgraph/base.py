"""
This module contains base classes that define interfaces
and contain code common to sub-classes, to avoid code duplication.
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

from typing import TYPE_CHECKING, Optional, Dict, List, Union, Any
from typing_extensions import TypeAlias
from copy import copy
from enum import Enum
import logging
from warnings import warn

from .registry import Registry
from .queries import QueryProperty
from .errors import ResolutionFailure, AuthorizationError, CannotBuildExistenceQuery
from .utility import (
    as_list,  # temporary for backwards compatibility (a lot of code imports it from here)
    expand_uri,
    normalize_data,
    invert_dict
)

if TYPE_CHECKING:
    from .client import KGClient
    from .properties import Property
    from .utility import ActivityLog

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
        scope: Optional[str] = None,
        use_cache: bool = True,
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        pass


class ContainsMetadata(Resolvable, metaclass=Registry):  # KGObject and EmbeddedMetadata
    properties: List[Property]
    context: Dict[str, str]
    type_: str
    scope: Optional[str]
    space: Union[str, None]
    default_space: Union[str, None]
    remote_data: Optional[JSONdict]
    aliases: Dict[str, str] = {}

    def __init__(self, data: Optional[Dict] = None, **properties):
        properties_copy = copy(properties)
        for prop in self.properties:
            try:
                val = properties[prop.name]
            except KeyError:
                if prop.required:
                    msg = "Property '{}' is required.".format(prop.name)
                    ErrorHandling.handle_violation(prop.error_handling, msg)
                val = None
            else:
                properties_copy.pop(prop.name)
            if val is None:
                val = prop.default
                if callable(val):
                    val = val()
            elif isinstance(val, (list, tuple)) and len(val) == 0:  # empty list
                val = None
            setattr(self, prop.name, val)
        for name_, alias_ in self.aliases.items():
            # the trailing underscores are because 'name' and 'alias' can be keys in 'properties'
            if name_ in properties_copy:
                val = properties_copy.pop(name_)
                if val is not None:
                    if properties.get(alias_, None):
                        raise ValueError(f"'{name_}' is an alias for '{alias_}', you cannot specify both")
                    setattr(self, alias_, val)
        if len(properties_copy) > 0:
            if len(properties_copy) == 1:
                raise NameError(f'{self.__class__.__name__} does not have a property named "{list(properties_copy)[0]}".')
            else:
                raise NameError(
                    f"""{self.__class__.__name__} does not have properties named "{'", "'.join(properties_copy)}"."""
                )

        # we store the original remote data in `_raw_remote_data`
        # and a normalized version in `remote_data`
        self._raw_remote_data = data  # for debugging
        self.remote_data = {}
        if data:
            self.remote_data = self.to_jsonld(include_empty_properties=True, follow_links=False)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name in self.aliases:
                return object.__getattribute__(self, self.aliases[name])
            else:
                raise

    def __setattr__(self, name, value):
        try:
            prop = self._property_lookup[name]
        except KeyError:
            if name in self.aliases:
                setattr(self, self.aliases[name], value)
            else:
                super().__setattr__(name, value)
        else:
            prop.check_value(value)
            super().__setattr__(name, value)

    def to_jsonld(
        self,
        normalized: bool = True,
        follow_links: bool = False,
        include_empty_properties: bool = False,
        include_reverse_properties: bool = False,
    ):
        """
        Return a JSON-LD representation of this metadata object

        Args:
            normalized (bool): Whether to expand all URIs. Defaults to True.
            follow_links (bool, optional): Whether to represent linked objects just by their "@id"
                or to include their full metadata. Defaults to False.
            include_empty_properties (bool, optional): Whether to include empty properties (with value "null").
                Defaults to False.

        """
        if self.properties:
            data: JSONdict = {"@type": [self.type_]}
            if hasattr(self, "id") and self.id:
                data["@id"] = self.id
            for prop in self.properties:
                if prop.intrinsic or include_reverse_properties:
                    expanded_path = prop.expanded_path
                    value = getattr(self, prop.name)
                    if include_empty_properties or prop.required or value is not None:
                        serialized = prop.serialize(value, follow_links=follow_links)
                        if expanded_path in data:
                            if isinstance(data[expanded_path], list):
                                data[expanded_path].append(serialized)
                            else:
                                data[expanded_path] = [data[expanded_path], serialized]
                        else:
                            data[expanded_path] = serialized
            if normalized:
                return normalize_data(data, self.context)
            else:
                return data
        else:
            raise NotImplementedError("to be implemented by child classes")

    @classmethod
    def from_jsonld(cls, data: JSONdict, client: KGClient, scope: Optional[str] = None):
        """
        Create an instance of the class from a JSON-LD document.
        """
        if scope:
            return cls.from_kg_instance(data, client, scope)
        else:
            return cls.from_kg_instance(data, client)

    @classmethod
    def from_kg_instance(cls, data: JSONdict, client: KGClient, scope: Optional[str] = None) -> ContainsMetadata:
        pass

    def save(
        self,
        client: KGClient,
        space: Optional[str] = None,
        recursive: bool = True,
        activity_log: Optional[ActivityLog] = None,
        replace: bool = False,
        ignore_auth_errors: bool = False,
    ):
        pass

    @classmethod
    def set_error_handling(
        cls, value: Union[ErrorHandling, None], property_names: Optional[Union[str, List[str]]] = None
    ):
        """
        Control validation for this class.

        Args:
            value (str): action to follow when there is a validation failure.
                (e.g. if a required property is not provided).
                Possible values: "error", "warning", "log", None
            property_names (str or list of str, optional): If not provided, the error handling
                mode will be applied to all properties. If a property name or list of names is given,
                the mode will be applied only to those properties.
        """
        if value is None:
            value = ErrorHandling.none
        else:
            value = ErrorHandling(value)
        if property_names:
            for property_name in as_list(property_names):
                try:
                    prop = cls._property_lookup[property_name]
                except KeyError:
                    raise ValueError("No such property: {}".format(property_name))
                else:
                    prop.error_handling = value
        else:
            for prop in cls.properties:
                prop.error_handling = value

    @classmethod
    def normalize_filter(cls, filter_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a dict containing filter key:value pairs so that it can be used
        in a call to the KG query API.

        Example:
            >>> import fairgraph.openminds.core as omcore
            >>> person = omcore.Person.from_uuid("045f846f-f010-4db8-97b9-b95b20970bf2", kg_client)
            >>> filter_dict = {"custodians": person, "name": "Virtual"}
            >>> omcore.Dataset.normalize_filter(filter_dict)
            {'name': 'Virtual',
             'custodians': 'https://kg.ebrains.eu/api/instances/045f846f-f010-4db8-97b9-b95b20970bf2'}
        """
        normalized = {}
        filter_dict_copy = filter_dict.copy()

        # handle aliases
        for name_, alias_ in cls.aliases.items():
            if name_ in filter_dict_copy:
                filter_dict_copy[alias_] = filter_dict_copy.pop(name_)

        for prop in cls.properties:
            if prop.name in filter_dict_copy:
                value = filter_dict_copy[prop.name]
                if isinstance(value, dict):
                    normalized[prop.name] = {}
                    for child_cls in prop.types:
                        normalized[prop.name].update(child_cls.normalize_filter(value))
                else:
                    normalized[prop.name] = prop.get_filter_value(value)
        return normalized

    @classmethod
    def generate_query_properties(cls, follow_links: Optional[Dict[str, Any]] = None):
        """
        Generate a list of QueryProperty instances for this class
        for use in constructing a KG query definition.

        Args:
            follow_links (dict): The links in the graph to follow when constructing the query. Defaults to None.
        """
        properties = [QueryProperty("@type")]
        reverse_aliases = invert_dict(cls.aliases)
        for prop in cls.properties:
            if prop.is_link and follow_links:
                if prop.name in follow_links:
                    properties.extend(prop.get_query_properties(follow_links[prop.name]))
                elif reverse_aliases.get(prop.name, None) in follow_links:
                    properties.extend(prop.get_query_properties(follow_links[reverse_aliases[prop.name]]))
                else:
                    properties.extend(prop.get_query_properties())
            else:
                properties.extend(prop.get_query_properties())
        return properties

    @classmethod
    def generate_query_filter_properties(
        cls,
        filters: Optional[Dict[str, Any]] = None,
    ):
        """

        Args:
            filters (dict, optional): A dict containing search parameters for the query.
        """
        if filters is None:
            filters = {}
        properties = []
        for prop in cls.properties:
            if prop.name in filters:
                properties.append(prop.get_query_filter_property(filters[prop.name]))
        return properties

    @classmethod
    def _deserialize_data(cls, data: JSONdict, client: KGClient, include_id: bool = False):
        # normalize data by expanding keys
        D = {"@type": data["@type"]}
        if include_id:
            D["@id"] = data["@id"]
        for key, value in data.items():
            if "__" in key:
                key, type_filter = key.split("__")
                normalised_key = expand_uri(key, cls.context)
                value = [item for item in as_list(value) if item["@type"][0].endswith(type_filter)]
                if normalised_key in D:
                    D[normalised_key].extend(value)
                else:
                    D[normalised_key] = value
            elif key.startswith("Q"):  # for 'Q' properties in data from queries
                D[key] = value
            elif key[0] != "@":
                normalised_key = expand_uri(key, cls.context)
                D[normalised_key] = value
        if cls.type_ not in D["@type"]:
            raise TypeError("type mismatch {} - {}".format(cls.type_, D["@type"]))

        def _get_type_from_data(data_item):
            type_ = data_item.get("@type", None)
            if type_:
                return type_[0]
            else:
                return None

        deserialized_data = {}
        for prop in cls.properties:
            expanded_path = expand_uri(prop.path, cls.context)
            data_item = D.get(expanded_path)
            if data_item is not None and prop.reverse:
                # for reverse properties, more than one property can have the same path
                # so we extract only those sub-items whose types match
                try:
                    data_item = [
                        part for part in as_list(data_item)
                        if _get_type_from_data(part) in [t.type_ for t in prop.types]
                    ]
                except AttributeError:
                    # problem when a forward and reverse path both given the same expanded path
                    # e.g. for Configuration
                    data_item = None
            # sometimes queries put single items in a list, this removes the enclosing list
            if (not prop.multiple) and isinstance(data_item, (list, tuple)) and len(data_item) == 1:
                data_item = data_item[0]
            deserialized_data[prop.name] = prop.deserialize(data_item, client, belongs_to=data.get("@id", None))
        return deserialized_data

    def resolve(
        self,
        client: KGClient,
        scope: Optional[str] = None,
        use_cache: bool = True,
        follow_links: Optional[Dict[str, Any]] = None,
    ):
        """
        Resolve properties that are represented by KGProxy objects.

        Args:
            client: KGClient object that handles the communication with the KG.
            scope (str): The scope of instances to include in the response.
                   Valid values are 'released', 'in progress', 'any'.
            use_cache (bool): whether to use cached data if they exist. Defaults to True.
            follow_links (dict): The links in the graph to follow. Defaults to None.

        Note: a real (non-proxy) object resolves to itself.
        """
        use_scope = scope or self.scope or "released"
        if follow_links:
            reverse_aliases = invert_dict(self.__class__.aliases)
            for prop in self.properties:
                if prop.is_link:
                    follow_name = None
                    if prop.name in follow_links:
                        follow_name = prop.name
                    elif reverse_aliases.get(prop.name, None) in follow_links:
                        follow_name = reverse_aliases[prop.name]

                    if follow_name:
                        if issubclass(prop.types[0], ContainsMetadata):
                            values = getattr(self, prop.name)
                            resolved_values: List[Any] = []
                            for value in as_list(values):
                                if isinstance(value, Resolvable):
                                    if isinstance(value, ContainsMetadata) and isinstance(value, RepresentsSingleObject):
                                        # i.e. isinstance(value, KGObject) - already resolved
                                        resolved_values.append(value)
                                    else:
                                        try:
                                            resolved_value = value.resolve(
                                                client,
                                                scope=use_scope,
                                                use_cache=use_cache,
                                                follow_links=follow_links[follow_name],
                                            )
                                        except ResolutionFailure as err:
                                            warn(str(err))
                                            resolved_values.append(value)
                                        else:
                                            resolved_values.append(resolved_value)
                            if isinstance(values, RepresentsSingleObject):
                                assert len(resolved_values) == 1
                                setattr(self, prop.name, resolved_values[0])
                            elif values is None:
                                assert len(resolved_values) == 0
                                setattr(self, prop.name, None)
                            else:
                                setattr(self, prop.name, resolved_values)
        return self

    def _build_existence_query(self) -> Union[None, Dict[str, Any]]:
        """
        Generate a KG query definition (as a JSON-LD document) that can be used to
        check whether a locally-defined object (with no ID) already exists in the KG.
        """
        if self.existence_query_properties is None:
            return None

        query_properties = []
        for property_name in self.existence_query_properties:
            for property in self.properties:
                if property.name == property_name:
                    query_properties.append(property)
                    break
        if len(query_properties) < 1:
            raise CannotBuildExistenceQuery("Empty existence query for class {}".format(self.__class__.__name__))
        query = {}
        for property in query_properties:
            query_property_name = property.name
            value = getattr(self, property.name)
            if isinstance(value, ContainsMetadata):
                if hasattr(value, "id") and value.id:
                    query[query_property_name] = value.id
                else:
                    sub_query = value._build_existence_query()
                    query.update({f"{query_property_name}__{key}": val for key, val in sub_query.items()})
            elif isinstance(value, (list, tuple)):
                raise CannotBuildExistenceQuery("not implemented yet")
            else:
                query_val = property.serialize(getattr(self, property.name), follow_links=False)
                if query_val is None:
                    raise CannotBuildExistenceQuery("Required value is missing")
                query[query_property_name] = query_val
        return query

class RepresentsSingleObject(Resolvable):  # KGObject, KGProxy
    id: Optional[str]
    remote_data: Optional[JSONdict]

    def children(
        self, client: KGClient, follow_links: Optional[Dict[str, Any]] = None
    ) -> List[RepresentsSingleObject]:
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


class SupportsQuerying:  # KGObject, KGQuery
    pass


class IRI:
    def __init__(self, value: Union[str, IRI]):
        if isinstance(value, IRI):
            iri = value.value
        else:
            iri = value
        if not iri.startswith("http"):
            raise ValueError("Invalid IRI")
        self.value: str = iri

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value

    def __repr__(self):
        return f"IRI({self.value})"

    def __str__(self):
        return self.value

    def to_jsonld(self):
        return self.value
