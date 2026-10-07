"""
This module provides Python classes to assist in writing Knowledge Graph queries.
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
from typing import Optional, List, Any, Dict, Union
from uuid import UUID
from datetime import date, datetime
import logging
import re
from warnings import warn

from openminds.base import IRI, EmbeddedMetadata, LinkedMetadata, Node
from .utility import as_list, expand_uri


logger = logging.getLogger("fairgraph")


class Regex(str):
    """
    A regular expression, for use as a filter value in place of a plain string.

    Where a plain string filters with the KG's "CONTAINS" operator, a `Regex` filters with "REGEX". 
    The KG applies the pattern as a search rather than a full match, 
    so a pattern with no anchors matches anywhere in the property value; use "^" and "$" to anchor it.
    Matching is always case-insensitive, whatever the pattern says.

    The pattern is checked when the `Regex` is created, and a malformed one raises ValueError
    (since the KG silently returns no results for a malformed pattern).

    Args:
        pattern (str): the regular expression.

    Raises:
        ValueError: if `pattern` is not a valid regular expression.

    Example:
        >>> import fairgraph.openminds.core as omcore
        >>> from fairgraph.queries import Regex
        >>> omcore.Person.list(client, family_name=Regex("^M[uü]ller$"))
    """

    def __new__(cls, pattern: str):
        try:
            # The KG's regular expression engine is not Python's, so this does not guarantee the KG will accept 
            # the pattern, but it catches common errors such as an unbalanced bracket or parenthesis.
            re.compile(pattern)
        except re.error as err:
            raise ValueError(f"Invalid regular expression {pattern!r}: {err}") from err
        return super().__new__(cls, pattern)


class Equals(str):
    """
    A string, for use as a filter value in place of a plain string, that must match the
    property value exactly rather than as a substring.

    Where a plain string filters with the KG's "CONTAINS" operator, an `Equals` filters with "EQUALS".
    The whole property value must match, so `Equals("FOO")` does not match "FOO-BAR".
    The KG ignores case when matching, but not whitespace, so `Equals("FOO")` does match "foo",
    but not "FOO ".

    Only a single value is supported: a list of `Equals` values is filtered with "CONTAINS".

    Args:
        value (str): the value the property must be equal to.

    Example:
        >>> import fairgraph.openminds.core as omcore
        >>> from fairgraph import Equals
        >>> omcore.Dataset.list(client, short_name=Equals("FOO"))
    """


class PathElement:
    """
    A single element in a multi-element query path, carrying optional
    ``reverse`` and ``type_filter`` settings for that step.

    Args:
        uri (str): The URI for this path step.
        reverse (bool): Whether to follow this link in reverse. Defaults to False.
        type_filter (str or list of str, optional): Type URI(s) to filter on at this step.
    """

    def __init__(self, uri: str, reverse: bool = False, type_filter: Optional[Union[str, List[str]]] = None):
        self.uri = uri
        self.reverse = reverse
        self.type_filter = type_filter

    def __repr__(self):
        return f"PathElement('{self.uri}', reverse={self.reverse}, type_filter={self.type_filter!r})"

    def serialize(self) -> Union[str, Dict[str, Any]]:
        if not self.reverse and not self.type_filter:
            return self.uri
        d: Dict[str, Any] = {"@id": self.uri}
        if self.type_filter:
            if isinstance(self.type_filter, (list, tuple)):
                d["typeFilter"] = [{"@id": t} for t in self.type_filter]
            else:
                d["typeFilter"] = {"@id": self.type_filter}
        if self.reverse:
            d["reverse"] = True
        return d


class Filter:
    """
    A filter for querying Knowledge Graph nodes.

    Args:
        operation (str): The operation for the filter. Options are:
            ("CONTAINS", "EQUALS", "IS_EMPTY", "STARTS_WITH", "ENDS_WITH", "REGEX")
        parameter (str, optional): A parameter name for the filter.
        value (str, optional): The value to filter on.

    Methods:
        serialize: Returns a dictionary containing the serialized filter.

    """

    def __init__(self, operation: str, parameter: Optional[str] = None, value: Optional[str] = None):
        self.operation = operation
        self.parameter = parameter
        self.value = value

    def __repr__(self):
        repr = f"Filter(operation='{self.operation}'"
        if self.parameter:
            repr += f", parameter='{self.parameter}'"
        if self.value:
            repr += f", value='{self.value}'"
        return repr + ")"

    def serialize(self):
        data = {"op": self.operation}
        if self.parameter:
            data["parameter"] = self.parameter
        if self.value:
            data["value"] = self.value
        return data


class QueryProperty:
    """
    A property for a Knowledge Graph query.

    Args:
        path (URI): The path of the property as a URI.
        name (str, optional): The name of the property to be used in the returned results.
        filter (Filter, optional): A filter based on the property.
        sorted (bool, optional): Whether to sort the results based on the property. Defaults to False.
        required (bool, optional): Whether the property is required. Defaults to False.
        ensure_order (bool, optional): Whether to ensure the ordering of results is maintained. Defaults to False.
        properties (List[QueryProperty], optional): A list of sub-properties.
        type_filter (URI, optional): Ensure that only objects that match the given type URI are returned.
        reverse (bool, optional): Whether the link defined by the path should be followed in the reverse direction. Defaults to False.
        expect_single (bool, optional): Whether to expect a single element in the result. Defaults to False.

    Methods:
        add_property: Adds a sub-property to the QueryProperty object.
        serialize: Returns a dictionary containing the serialized QueryProperty.

    Example:
        >>> p = QueryProperty(
        ...    "https://openminds.om-i.org/props/fullName",
        ...    name="full_name",
        ...    filter=Filter("CONTAINS", parameter="name"),
        ...    sorted=True,
        ...    required=True
        ... )
    """

    def __init__(
        self,
        path: Union[str, List[Union[str, PathElement]]],
        name: Optional[str] = None,
        filter: Optional[Filter] = None,
        sorted: bool = False,
        required: bool = False,
        ensure_order: bool = False,
        properties: Optional[List[QueryProperty]] = None,
        type_filter: Optional[Union[str, List[str]]] = None,
        reverse: bool = False,
        expect_single: bool = False,
    ):
        self.path = path
        self.name = name
        self.filter = filter
        self.sorted = sorted
        self.required = required
        self.ensure_order = ensure_order
        self.properties = properties or []
        self.type_filter = type_filter
        self.reverse = reverse
        self.expect_single = expect_single

        # Normalize path to a list of PathElement for clean serialization
        if isinstance(path, str):
            self._path_elements = [PathElement(path, reverse=reverse, type_filter=type_filter)]
        else:
            has_path_elements = any(isinstance(p, PathElement) for p in path)
            if has_path_elements and (reverse or type_filter is not None):
                raise ValueError(
                    "Cannot use top-level 'reverse' or 'type_filter' when path contains PathElement objects; "
                    "set those on the PathElement directly."
                )
            normalized = []
            for i, p in enumerate(path):
                if isinstance(p, PathElement):
                    normalized.append(p)
                elif i == 0 and not has_path_elements:
                    # backwards compat: top-level reverse/type_filter apply to first element
                    normalized.append(PathElement(p, reverse=reverse, type_filter=type_filter))
                else:
                    normalized.append(PathElement(p))
            self._path_elements = normalized

        for prop in self.properties:
            if prop.sorted:
                raise ValueError("Sorting is only allowed on the root level of a query.")

    def __repr__(self):
        return f"QueryProperty({self.path}, name={self.name}, reverse={self.reverse})"

    def add_property(self, prop: QueryProperty):
        assert isinstance(prop, QueryProperty)
        if prop.sorted:
            raise ValueError("Sorting is only allowed on the root level of a query.")
        self.properties.append(prop)

    def serialize(self) -> Dict[str, Any]:
        serialized_elements = [pe.serialize() for pe in self._path_elements]
        if isinstance(self.path, str):
            data: Dict[str, Any] = {"path": serialized_elements[0]}
        else:
            data: Dict[str, Any] = {"path": serialized_elements}
        if self.name:
            data["propertyName"] = self.name
        if self.filter:
            data["filter"] = self.filter.serialize()
        if self.sorted:
            data["sort"] = True
        if self.required:
            data["required"] = True
        if self.ensure_order:
            data["ensureOrder"] = True
        if self.properties:
            data["structure"] = [prop.serialize() for prop in self.properties]
        if self.expect_single:
            data["singleValue"] = "FIRST"
        return data


class Query:
    """
    A Python representation of an EBRAINS Knowledge Graph query,
    which can be serialized to the JSON-LD used by the kg-core query API.

    Args:
        node_type (URI): The URI of the node type to query.
        label (str, optional): A label for this query.
        space (Optional[str], optional): The KG space to query.
        properties (Optional[List[QueryProperty]], optional): A list of QueryProperty
            objects representing the properties to include in the results.

    Methods:
        add_property: Adds a QueryProperty object to the list of properties to include.
        serialize: Returns a JSON-LD representation of the query, suitable for sending to the KG.

    Example:
        >>> q = Query(
        ...    node_type="https://openminds.om-i.org/types/ModelVersion",
        ...    label="fg-testing-modelversion",
        ...    space="model",
        ...    properties=[
        ...        QueryProperty("@type"),
        ...        QueryProperty(
        ...            "https://openminds.om-i.org/props/fullName",
        ...            name="vocab:fullName",
        ...            filter=Filter("CONTAINS", parameter="name"),
        ...            sorted=True,
        ...            required=True,
        ...        ),
        ...        QueryProperty(
        ...            "https://openminds.om-i.org/props/versionIdentifier",
        ...            name="vocab:versionIdentifier",
        ...            filter=Filter("EQUALS", parameter="version"),
        ...            required=True,
        ...        ),
        ...        QueryProperty(
        ...            "https://openminds.om-i.org/props/format",
        ...            name="vocab:format",
        ...            ensure_order=True,
        ...            properties=[
        ...                QueryProperty("@id", filter=Filter("EQUALS", parameter="format")),
        ...                QueryProperty("@type"),
        ...            ],
        ...        )
        ...     )
    """

    def __init__(
        self,
        node_type: str,
        label: Optional[str] = None,
        space: Optional[str] = None,
        properties: Optional[List[QueryProperty]] = None,
    ):
        self.node_type = node_type
        self.label = label
        self.space = space
        self.properties = [QueryProperty("@id", filter=Filter("EQUALS", parameter="id"))]
        if properties:
            self.properties.extend(properties)
        if space:
            found = False
            for property in self.properties:
                if property.path == "https://core.kg.ebrains.eu/vocab/meta/space":
                    property.filter = Filter("EQUALS", value=self.space)
                    found = True
            if not found:
                self.properties.append(
                    QueryProperty(
                        "https://core.kg.ebrains.eu/vocab/meta/space",
                        name="query:space",
                        filter=Filter("EQUALS", value=self.space),
                    )
                )

    def add_property(self, prop: QueryProperty):
        assert isinstance(prop, QueryProperty)
        self.properties.append(prop)

    def serialize(self) -> Dict[str, Any]:
        query = {
            "@context": {
                "@vocab": "https://core.kg.ebrains.eu/vocab/query/",
                "query": "https://schema.hbp.eu/myQuery/",
                "propertyName": {"@id": "propertyName", "@type": "@id"},
                "merge": {"@type": "@id", "@id": "merge"},
                "path": {"@id": "path", "@type": "@id"},
            },
            "meta": {
                "type": self.node_type,
                "description": "Automatically generated by fairgraph",
            },
            "structure": [prop.serialize() for prop in self.properties],
        }
        if self.label:
            query["meta"]["name"] = self.label
        return query


#: Order, most preferred first, in which a generated query picks its single sort key.
#: The names are the camelCase schema names used as ``QueryProperty.name`` (e.g. the Python
#: attribute ``lookup_label`` is the schema name ``lookupLabel``). ``name`` is preferred because
#: its values are human-readable and sort meaningfully; ``lookupLabel`` is deliberately last
#: because it embeds atlas/project prefixes, camel-case and sometimes DOIs, so sorting by it
#: groups by origin scheme first and looks cluttered. ``synonyms`` is excluded: it is
#: list-valued and not a sensible sort key.
#:
#: This is the default priority. Generated openMINDS classes carry their own ``SORT_PRIORITY``
#: class attribute (see the builder's ``DEFAULT_SORT_PRIORITY`` / ``SORT_PRIORITY_EXCEPTIONS``),
#: and a few classes override it — e.g. ``ParcellationEntity`` and ``ParcellationEntityVersion``
#: put ``lookupLabel`` first so that terms from the same atlas stay together.
#:
#: The KG API allows ``"sort": true`` on only one property, and only at the root level, so
#: exactly one property is chosen and it is always a top-level property.
SORT_PRIORITY = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")


def choose_sort_property(query_properties, priority=SORT_PRIORITY):
    """
    Return the single top-level ``QueryProperty`` to sort a generated query by, or ``None``.

    The first top-level property whose ``name`` appears in ``priority`` (in priority order) is
    chosen; this satisfies the KG's constraint of exactly one ``"sort": true`` at the root level.
    ``priority`` defaults to the module-level :data:`SORT_PRIORITY`. If no sortable property is
    present, returns ``None`` so no sort is requested.
    """
    for sort_name in priority:
        for prop in query_properties:
            if prop.name == sort_name:
                return prop
    return None


def _get_query_property_name(property, possible_classes):
    if isinstance(property.path, str):
        property_name = property.path
    else:
        assert isinstance(property.path, list)
        found_match = False
        for cls in possible_classes:
            for path in property.path:
                for prop in cls.properties:
                    if path == prop.path:
                        property_name = path
                        found_match = True
                        break
                if found_match:
                    break
            if found_match:
                break
        assert found_match
    return property_name


def get_query_properties(
    property, context, follow_links: Optional[Dict[str, Any]] = None, with_reverse_properties: Optional[bool] = False
) -> List[QueryProperty]:
    """
    Generate one or more QueryProperty instances for this property,
    for use in constructing a KG query definition.
    """
    expanded_path = expand_uri(property.path, context)
    properties = []

    if any(issubclass(_type, EmbeddedMetadata) for _type in property.types):
        if not all(issubclass(_type, EmbeddedMetadata) for _type in property.types):
            warn(f"Mixed types in {property}")
            return properties
        for cls in property.types:
            if len(property.types) > 1:
                property_name = f"{property.path}__{cls.__name__}"
                assert isinstance(cls.type_, str)
                type_filter = cls.type_
            else:
                property_name = property.path
                type_filter = None
            properties.append(
                QueryProperty(
                    expanded_path,
                    name=property_name,
                    reverse=bool(property.reverse),
                    type_filter=type_filter,
                    ensure_order=property.multiple,
                    expect_single=property.is_link and not property.multiple,
                    properties=cls.generate_query_properties(follow_links, with_reverse_properties),
                )
            )
    elif any(issubclass(_type, LinkedMetadata) for _type in property.types):
        assert all(issubclass(_type, LinkedMetadata) for _type in property.types)
        if follow_links is not None:
            for cls in property.types:
                property_name = _get_query_property_name(property, possible_classes=[cls])
                if len(property.types) > 1:
                    property_name = f"{property_name}__{cls.__name__}"
                    assert isinstance(cls.type_, str)
                    type_filter = cls.type_
                else:
                    type_filter = None
                properties.append(
                    QueryProperty(
                        expanded_path,
                        name=property_name,
                        reverse=bool(property.reverse),
                        type_filter=type_filter,
                        ensure_order=property.multiple,
                        expect_single=property.is_link and not property.multiple,
                        properties=[
                            QueryProperty("@id"),
                            *cls.generate_query_properties(follow_links, with_reverse_properties),
                        ],
                    )
                )
        else:
            if isinstance(property.path, str):
                property_name = property.path
                properties.append(
                    QueryProperty(
                        expanded_path,
                        name=property_name,
                        reverse=bool(property.reverse),
                        type_filter=None,
                        ensure_order=property.multiple,
                        expect_single=property.is_link and not property.multiple,
                        properties=[
                            QueryProperty("@id"),
                            QueryProperty("@type"),
                        ],
                    )
                )
            else:
                assert isinstance(property.path, list)
                logger.warning(f"Cannot yet handle case where property.path is a list: {property}")
    else:
        assert not property.reverse
        properties.append(
            QueryProperty(
                expanded_path,
                name=property.path,
                reverse=bool(property.reverse),
                ensure_order=property.multiple,
                expect_single=property.is_link and not property.multiple,
            )
        )
    return properties


def get_query_filter_property(property, context, filter: Any) -> QueryProperty:
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
        if isinstance(filter, Regex):
            op = "REGEX"
        elif isinstance(filter, Equals):
            op = "EQUALS"
        elif property.types[0] in (int, float, bool, datetime, date):
            op = "EQUALS"
        else:
            op = "CONTAINS"
        filter_obj = Filter(op, value=filter)

    expanded_path = expand_uri(property.path, context)

    if any(issubclass(_type, Node) for _type in property.types):
        assert all(issubclass(_type, Node) for _type in property.types)
        prop = QueryProperty(expanded_path, name=f"Q{property.name}", required=True, reverse=property.reverse)
        if filter_obj:
            if filter_obj.value.startswith("https://kg.ebrains.eu/api/instances"):
                filter_path = "@id"
            else:
                filter_path = "http://schema.org/identifier"
            prop.properties.append(QueryProperty(filter_path, filter=filter_obj))
        else:
            for cls in property.types:
                child_properties = cls.generate_query_filter_properties(filter)
                if child_properties:
                    # if the class has properties with the appropriate name
                    # we add them, then break to avoid adding the same
                    # prop twice
                    prop.properties.extend(child_properties)
                    break
    else:
        prop = QueryProperty(expanded_path, name=f"Q{property.name}", filter=filter_obj, required=True)
    return prop


def get_filter_value(property, value: Any) -> Union[str, List[str]]:
    """
    Normalize a value for use in a KG query

    Example:
        >>> import fairgraph.openminds.core as omcore
        >>> person = omcore.Person.from_uuid("045f846f-f010-4db8-97b9-b95b20970bf2", kg_client)
        >>> prop = Property(name='custodians', types=(omcore.Organization, omcore.Person),
        ...                  path="vocab:custodian", multiple=True)
        >>> get_filter_value(prop, person)
        https://kg.ebrains.eu/api/instances/045f846f-f010-4db8-97b9-b95b20970bf2
    """
    from .kgproxy import KGProxy

    def is_valid(val):
        if isinstance(val, str):
            try:
                val = UUID(val)
            except ValueError:
                pass
        if isinstance(val, str):
            if IRI in property.types:
                return True
            for temporal_type in (datetime, date):
                if temporal_type in property.types:
                    try:
                        temporal_type.fromisoformat(val)
                    except ValueError:
                        continue
                    else:
                        return True
        return isinstance(val, (IRI, UUID, *property.types)) or (
            isinstance(val, KGProxy) and not set(val.classes).isdisjoint(property.types)
        )

    if isinstance(value, list) and len(value) > 0:
        valid_type = all(is_valid(item) for item in value)
        have_multiple = True
    else:
        valid_type = is_valid(value)
        have_multiple = False
    if not valid_type:
        if property.name == "hash":  # bit of a hack
            filter_value = value
        elif isinstance(value, str) and value.startswith("http"):  # for @id
            filter_value = value
        else:
            raise TypeError("{} must be of type {}, not {}".format(property.name, property.types, type(value)))

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
        else:
            filter_item = item
        filter_items.append(filter_item)

    if have_multiple:
        return filter_items
    else:
        return filter_items[0]
