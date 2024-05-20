"""
Representations of metadata properties.
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
import logging
from datetime import date, datetime
from collections.abc import Iterable, Mapping
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING, Union
from uuid import UUID
from warnings import warn

if TYPE_CHECKING:
    from .client import KGClient

from dateutil import parser as date_parser

from .registry import lookup, lookup_type
from .utility import as_list
from .base import IRI, JSONdict, ContainsMetadata, ErrorHandling
from .kgproxy import KGProxy
from .kgquery import KGQuery
from .kgobject import KGObject
from .embedded import EmbeddedMetadata
from .utility import expand_uri
from .queries import Filter, QueryProperty


logger = logging.getLogger("fairgraph")


global_context = {
    "vocab": "https://openminds.ebrains.eu/vocab/",
}


def is_resolved(item: JSONdict) -> bool:
    return set(item.keys()) not in (set(["@id", "@type"]), set(["@id"]))


def build_kg_object(
    possible_classes: Iterable[Union[EmbeddedMetadata, KGObject]],
    data: Optional[Union[JSONdict, List[JSONdict]]],
    client: Optional[KGClient] = None,
) -> Union[EmbeddedMetadata, KGObject, KGProxy, None, List[Union[EmbeddedMetadata, KGObject, KGProxy]]]:
    """
    Build a KGObject, an EmbeddedMetadata, a KGProxy, or a list of such, based on the data provided.

    This takes care of the JSON-LD quirk that you get a list if there are multiple
    objects, but you get the object directly if there is only one.

    Returns `None` if data is None.
    """
    if data is None:
        return None
    if not isinstance(data, list):
        if not isinstance(data, dict):
            raise ValueError("data must be a list or dict")
        if "@list" in data:
            assert len(data) == 1
            data = data["@list"]
        else:
            data = [data]
    assert isinstance(data, list)

    objects = []
    for item in data:
        if item is None:
            logger.error(f"Unexpected null. possible_classes={possible_classes} data={data}")
            continue
        logger.debug(f"Building {possible_classes} from {item.get('@id', 'not a node')}")
        if possible_classes is None:
            raise NotImplementedError

        assert isinstance(possible_classes, (list, tuple))
        assert all(issubclass(item, KGObject) for item in possible_classes) or all(
            issubclass(item, EmbeddedMetadata) for item in possible_classes
        )
        if len(possible_classes) > 1:
            if "@type" in item:
                for cls in possible_classes:
                    if item["@type"] == [cls.type_]:
                        kg_cls = cls
                        break
            else:
                kg_cls = possible_classes

        else:
            kg_cls = possible_classes[0]

        if "@id" in item:
            # the following line is only relevant to test data,
            # for real data it is always an expanded uri
            item["@id"] = expand_uri(item["@id"], {"kg": "https://kg.ebrains.eu/api/instances/"})
            if is_resolved(item):
                try:
                    obj = kg_cls.from_kg_instance(item, client)
                except (ValueError, KeyError) as err:
                    # to add: emit a warning
                    logger.warning("Error in building {}: {}".format(kg_cls.__name__, err))
                    obj = KGProxy(kg_cls, item["@id"]).resolve(client)
                    # todo: provide space and scope
            else:
                if "@type" in item and item["@type"] is not None and kg_cls not in as_list(lookup_type(item["@type"][0])):
                    raise Exception(f"mismatched types: {kg_cls} <> {item['@type']} (id: {item['@id']})")
                    obj = None
                else:
                    obj = KGProxy(kg_cls, item["@id"])
        elif "@type" in item:  # Embedded metadata
            obj = kg_cls.from_kg_instance(item, client)
        else:
            # todo: add a logger.warning that we have dud data
            obj = None

        if obj is not None:
            objects.append(obj)
    if len(objects) == 1:
        return objects[0]
    else:
        return objects


class Property(object):
    """
    Representation of a metadata property.

    Args:
        name (str): The name of the property.
        types (str, date, datetime, int, KGObject, EmbeddedMetadata): The types of values that the property can take.
        path (URI): The globally unique identifier of this property.
        required (bool, optional): Whether the property is required or not. Defaults to False.
        default (Any, optional): The default value of the property if it is not provided.
        multiple (bool, optional): Whether the property can have multiple values or not. Defaults to False.
        error_handling (str, optional): How to handle errors, such as the wrong type of value being provided.
            One of "error", "warning", "log", "none". Defaults to "warning".
        reverse (str, optional): The name of the reverse property, if any.
        doc (str, optional): The documentation of the property.

    The class also contains machinery for serialization into JSON-LD of values stored in properties in
    KGObjects and EmbeddedMetadata instances, and for de-serialization from JSON-LD into Python objects.
    """

    def __init__(
        self,
        name: str,
        types: Union[
            str,
            type,
            KGObject,
            EmbeddedMetadata,
            Iterable[Union[str, type, KGObject, EmbeddedMetadata]],
        ],
        path: str,
        required: bool = False,
        default: Any = None,
        multiple: bool = False,
        error_handling: ErrorHandling = ErrorHandling.log,
        reverse: Optional[str] = None,
        doc: str = "",
    ):
        self.name = name
        self._types: Tuple[Union[str, type, KGObject, EmbeddedMetadata], ...]
        if isinstance(types, (type, str)):
            self._types = (types,)
        else:
            assert isinstance(types, Iterable)
            self._types = tuple(types)
        self._resolved_types = False
        # later, may need to use lookup() to turn strings into classes
        self.path = path
        self.required = required
        self.default = default
        self.multiple = multiple
        self.error_handling = error_handling
        self.reverse = reverse
        self.doc = doc

    def __repr__(self):
        return "Property(name='{}', types={}, path='{}', required={}, multiple={})".format(
            self.name, self._types, self.path, self.required, self.multiple
        )

    @property
    def types(self):
        if not self._resolved_types:
            self._types = tuple([lookup(obj) if isinstance(obj, str) else obj for obj in self._types])
            self._resolved_types = True
        return self._types

    def check_value(self, value):
        def check_single(item):
            if not isinstance(item, self.types):
                if not (
                    isinstance(item, (KGProxy, KGQuery, EmbeddedMetadata))
                    and any(issubclass(cls, _type) for _type in self.types for cls in item.classes)
                ):
                    if item is None and self.required:
                        errmsg = "Property '{}' is required but was not provided.".format(self.name)
                    else:
                        errmsg = "Property '{}' should be of type {}, not {}".format(self.name, self.types, type(item))
                    ErrorHandling.handle_violation(self.error_handling, errmsg)

        if self.required or value is not None:
            if self.multiple and isinstance(value, Iterable) and not isinstance(value, Mapping):
                for item in value:
                    check_single(item)
            else:
                check_single(value)

    @property
    def intrinsic(self):
        """
        Return True If the prop contains data that is directly stored in the instance,
        False if the prop contains data that is obtained through a query
        """
        return not self.reverse

    @property
    def is_link(self) -> bool:
        return issubclass(self.types[0], (KGObject, EmbeddedMetadata))

    @property
    def expanded_path(self) -> str:
        return expand_uri(self.path, global_context)

    def serialize(self, value: Any, follow_links: bool = False):
        """
        Serialize a value to JSON-LD.

        Args:
            value (any): The value to be serialized.
            follow_links (bool): If the value contains graph links, these links
                will be represented using "@id" (follow_links=False) or fully
                serialized recursively (follow_links=True).
        """

        def serialize_single(value):
            if isinstance(value, (str, int, float, dict)):
                return value
            elif isinstance(value, EmbeddedMetadata):
                return value.to_jsonld(follow_links=follow_links)
            elif isinstance(value, IRI):
                return value.to_jsonld()
            elif isinstance(value, KGObject):
                if follow_links or value.id is None:
                    return value.to_jsonld(follow_links=follow_links)
                else:
                    return {"@id": value.id}
            elif isinstance(value, KGProxy):
                return {"@id": value.id}
            elif isinstance(value, (datetime, date)):
                return value.isoformat()
            elif value is None:
                return None
            else:
                raise ValueError("don't know how to serialize this value")

        if isinstance(value, (list, tuple)):
            if self.multiple or self.error_handling != ErrorHandling.error:
                value = [serialize_single(item) for item in value]
                if len(value) == 1:
                    return value[0]
                else:
                    return value
            elif len(value) == 1:
                return serialize_single(value[0])
            elif self.error_handling != ErrorHandling.none:
                errmsg = f"Single item expected for prop {self.name} but received multiple"
                ErrorHandling.handle_violation(self.error_handling, errmsg)
            else:
                return value
        else:
            return serialize_single(value)

    def deserialize(self, data: Union[JSONdict, List[JSONdict]], client: KGClient, belongs_to: Optional[str] = None):
        """
        Deserialize a JSON-LD data structure into Python objects.

        Args:
            data: the JSON-LD data
            client: a KG client
            belongs_to: the ID of the object this property belongs to
        """
        if data == []:
            return None
        elif data is None:
            if self.reverse:
                if isinstance(self.reverse, list):
                    # todo: handle all possible reverses
                    #       for now, we just take the first
                    return KGQuery(self.types, {self.reverse[0]: belongs_to})
                else:
                    return KGQuery(self.types, {self.reverse: belongs_to})
            else:
                return None
        try:
            if issubclass(self.types[0], (KGObject, EmbeddedMetadata)):
                return build_kg_object(self.types, data, client=client)
            elif self.types[0] in (datetime, date):
                if isinstance(data, str):
                    if data == "":  # seems like the KG Editor puts empty strings here rather than None?
                        return None
                    return date_parser.parse(data)
                elif isinstance(data, Iterable):
                    return [date_parser.parse(item) for item in data]
                else:
                    raise ValueError("expecting a string or list")
            elif self.types[0] == int:
                if isinstance(data, str):
                    return int(data)
                elif isinstance(data, Iterable):
                    return [int(item) for item in data]
                else:
                    return int(data)
            elif self.types[0] == IRI:
                return IRI(data)
            else:
                return data
        except Exception as err:
            ErrorHandling.handle_violation(self.error_handling, str(err))
            return None

    def _get_query_property_name(self, possible_classes):
        if isinstance(self.path, str):
            property_name = self.path
        else:
            assert isinstance(self.path, list)
            found_match = False
            for cls in possible_classes:
                for path in self.path:
                    assert path.startswith("^")
                    for prop in cls.properties:
                        if path[1:] == prop.path:
                            property_name = path
                            found_match = True
                            break
                    if found_match:
                        break
                if found_match:
                    break
            assert found_match
        if property_name.startswith("^"):
            assert self.reverse
            property_name = property_name[1:]
        return property_name

    def get_query_properties(self, follow_links: Optional[Dict[str, Any]] = None) -> List[QueryProperty]:
        """
        Generate one or more QueryProperty instances for this property,
        for use in constructing a KG query definition.
        """

        properties = []
        if any(issubclass(_type, EmbeddedMetadata) for _type in self.types):
            if not all(issubclass(_type, EmbeddedMetadata) for _type in self.types):
                warn(f"Mixed types in {self}")
                return properties
            for cls in self.types:
                if len(self.types) > 1:
                    property_name = f"{self.path}__{cls.__name__}"
                    type_filter = cls.type_
                else:
                    property_name = self.path
                    type_filter = None
                if property_name.startswith("^"):
                    # used to mark reverse properties. Maybe not necessary?
                    assert self.reverse
                    property_name = property_name[1:]
                properties.append(
                    QueryProperty(
                        self.expanded_path,
                        name=property_name,
                        reverse=self.reverse,
                        type_filter=type_filter,
                        ensure_order=self.multiple,
                        properties=cls.generate_query_properties(follow_links),
                    )
                )
        elif any(issubclass(_type, KGObject) for _type in self.types):
            assert all(issubclass(_type, KGObject) for _type in self.types)
            if follow_links is not None:
                for cls in self.types:
                    property_name = self._get_query_property_name(possible_classes=[cls])
                    if len(self.types) > 1:
                        property_name = f"{property_name}__{cls.__name__}"
                        type_filter = cls.type_
                    else:
                        type_filter = None
                    properties.append(
                        QueryProperty(
                            self.expanded_path,
                            name=property_name,
                            reverse=self.reverse,
                            type_filter=type_filter,
                            ensure_order=self.multiple,
                            properties=[QueryProperty("@id"), *cls.generate_query_properties(follow_links)],
                        )
                    )
            else:
                if isinstance(self.path, str):
                    property_name = self.path
                    if property_name.startswith("^"):
                        assert self.reverse
                        property_name = property_name[1:]
                    properties.append(
                        QueryProperty(
                            self.expanded_path,
                            name=property_name,
                            reverse=self.reverse,
                            type_filter=None,
                            ensure_order=self.multiple,
                            properties=[
                                QueryProperty("@id"),
                                QueryProperty("@type"),
                            ],
                        )
                    )
                else:
                    assert isinstance(self.path, list)
                    logger.warning(f"Cannot yet handle case where self.path is a list: {self}")
        else:
            assert not self.reverse
            properties.append(
                QueryProperty(
                    self.expanded_path,
                    name=self.path,
                    reverse=self.reverse,
                    ensure_order=self.multiple,
                )
            )
        return properties

    def get_query_filter_property(self, filter: Any) -> QueryProperty:
        """
        Generate a QueryProperty instance containing a filter,
        for use in constructing a KG query definition.
        """
        assert filter is not None
        if isinstance(filter, dict):
            # we pass the filter through to the next level
            filter_obj = None
        else:
            # we have a filter value for this property
            if self.types[0] in (int, float, bool, datetime, date):
                op = "EQUALS"
            else:
                op = "CONTAINS"
            filter_obj = Filter(op, value=filter)

        if any(issubclass(_type, ContainsMetadata) for _type in self.types):
            assert all(issubclass(_type, ContainsMetadata) for _type in self.types)
            prop = QueryProperty(self.expanded_path, name=f"Q{self.name}", required=True, reverse=self.reverse)
            if filter_obj:
                prop.properties.append(QueryProperty("@id", filter=filter_obj))
            else:
                for cls in self.types:
                    child_properties = cls.generate_query_filter_properties(filter)
                    if child_properties:
                        # if the class has properties with the appropriate name
                        # we add them, then break to avoid adding the same
                        # prop twice
                        prop.properties.extend(child_properties)
                        break
        else:
            prop = QueryProperty(self.expanded_path, name=f"Q{self.name}", filter=filter_obj, required=True)
        return prop

    def get_filter_value(self, value: Any) -> Union[str, List[str]]:
        """
        Normalize a value for use in a KG query

        Example:
            >>> import fairgraph.openminds.core as omcore
            >>> person = omcore.Person.from_uuid("045f846f-f010-4db8-97b9-b95b20970bf2", kg_client)
            >>> prop = Property(name='custodians', types=(omcore.Organization, omcore.Person),
            ...                  path="vocab:custodian", multiple=True)
            >>> prop.get_filter_value(person)
            https://kg.ebrains.eu/api/instances/045f846f-f010-4db8-97b9-b95b20970bf2
        """

        def is_valid(val):
            if isinstance(val, str):
                try:
                    val = UUID(val)
                except ValueError:
                    pass
            return isinstance(val, (IRI, UUID, *self.types)) or (isinstance(val, KGProxy) and val.cls in self.types)

        if isinstance(value, list) and len(value) > 0:
            valid_type = all(is_valid(item) for item in value)
            have_multiple = True
        else:
            valid_type = is_valid(value)
            have_multiple = False
        if not valid_type:
            if self.name == "hash":  # bit of a hack
                filter_value = value
            elif isinstance(value, str) and value.startswith("http"):  # for @id
                filter_value = value
            else:
                raise TypeError("{} must be of type {}, not {}".format(self.name, self.types, type(value)))

        filter_items = []
        for item in as_list(value):
            if isinstance(item, IRI):
                filter_item = item.value
            elif isinstance(item, (date, datetime)):
                filter_item = item.isoformat()
            elif hasattr(item, "id"):
                filter_item = item.id
            elif isinstance(item, UUID):
                # todo: consider using client.uri_from_uuid()
                # would require passing client as arg
                filter_item = f"https://kg.ebrains.eu/api/instances/{item}"
            elif isinstance(item, str) and "+" in item:  # workaround for KG bug
                invalid_char_index = item.index("+")
                if invalid_char_index < 3:
                    raise ValueError(f"Cannot use {item} as filter, contains invalid characters")
                filter_item = item[:invalid_char_index]
                warn(f"Truncating filter value {item} --> {filter_item}")
            else:
                filter_item = item
            filter_items.append(filter_item)

        if have_multiple:
            return filter_items
        else:
            return filter_items[0]
