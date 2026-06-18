"""


"""

# Copyright 2019-2020 CNRS

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
import hashlib
import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, TYPE_CHECKING
import warnings

if TYPE_CHECKING:
    from .client import KGClient
    from .kgobject import KGObject

logger = logging.getLogger("fairgraph")

JSONdict = Dict[str, Any]  # see https://github.com/python/typing/issues/182 for some possible improvements
ATTACHMENT_SIZE_LIMIT = 1024 * 1024  # 1 MB


def as_list(obj: Union[None, KGObject, dict, str, list, tuple]) -> list:
    """
    Converts the input obj into a list.

    Args:
        obj: The input object to be converted to a list.

    Returns:
        list: A list - see Notes below.

    Raises:
        TypeError: If the input obj cannot be converted to a list.

    Notes:
        - If obj is None, it returns an empty list.
        - If obj is a dict or a str, it returns a list containing obj.
        - If obj is a list or a tuple, it returns a list with the same elements as obj.
        - If obj is not any of the above, it tries to convert obj into a list. If it fails due to a TypeError, it raises a TypeError with an appropriate error message.
    """
    if obj is None:
        return []
    elif isinstance(obj, (dict, str)):
        return [obj]
    try:
        L = list(obj)
    except TypeError:
        L = [obj]
    return L


def invert_dict(D):
    newD = {}
    for key, value in D.items():
        newD[value] = key
    return newD


def expand_uri(uri_list: Union[str, List[str]], context: Dict[str, Any]) -> Union[str, Tuple[str, ...]]:
    """
    Expands a URI or a list of URIs using a given context.

    Args:
        uri_list (Union[str, List[str]]): A URI or a list of URIs to be expanded.
        context (Dict[str, Any]): A dictionary containing a mapping of prefixes to base URLs.

    Returns:
        Union[str, Tuple[str, ...]]: An expanded URI or a tuple of expanded URIs.

    Raises:
        ValueError: If a prefix in the URI is not found in the context.

    Examples:
        >>> context = {'foaf': 'http://xmlns.com/foaf/0.1/'}
        >>> uri_list = 'foaf:Person'
        >>> expand_uri(uri_list, context)
        'http://xmlns.com/foaf/0.1/Person'

    """
    expanded_uris = []
    for uri in as_list(uri_list):
        if uri.startswith("http") or uri.startswith("@"):
            expanded_uris.append(uri)
        else:
            parts = uri.split(":")
            if len(parts) == 1:
                prefix = "@vocab"
                identifier = uri
            else:
                prefix, identifier = parts
            if prefix not in context:
                raise ValueError(f"prefix {prefix} not found in context")
            base_url = context[prefix]
            if not base_url.endswith("/"):
                base_url += "/"
            expanded_uris.append(f"{base_url}{identifier}")
    if isinstance(uri_list, str):
        return expanded_uris[0]
    else:
        return tuple(expanded_uris)


def compact_uri(
    uri_list: Union[str, List[str]], context: Dict[str, Any], strict: bool = False
) -> Union[str, Tuple[str, ...]]:
    """
    Compacts a URI or a list of URIs using a given context.

    Args:
        uri_list (Union[str, List[str]]): A URI or a list of URIs to be compacted.
        context (Dict[str, Any]): A dictionary containing a mapping of prefixes to base URLs.
        strict (bool, optional): Whether to raise an error if a URI cannot be compacted. Defaults to False.

    Returns:
        Union[str, Tuple[str, ...]]: A compacted URI or a tuple of compacted URIs.

    Raises:
        ValueError: If strict is True and a URI cannot be compacted.

    Examples:
        >>> context = {'foaf': 'http://xmlns.com/foaf/0.1/'}
        >>> uri_list = 'http://xmlns.com/foaf/0.1/Person'
        >>> compact_uri(uri_list, context)
        'foaf:Person'
    """
    compacted_uris = []
    for uri in as_list(uri_list):
        if uri.startswith("http"):
            found = False
            for prefix, base_url in context.items():
                if uri.startswith(base_url):
                    start = len(base_url)
                    identifier = uri[start:].strip("/")
                    if prefix == "@vocab":
                        compacted_uris.append(identifier)
                    else:
                        compacted_uris.append(f"{prefix}:{identifier}")
                    found = True
                    break
            if not found:
                if strict:
                    raise ValueError(f"Unable to compact {uri} with the provided context")
                else:
                    compacted_uris.append(uri)
        else:
            compacted_uris.append(uri)
    if isinstance(uri_list, str):
        return compacted_uris[0]
    else:
        return tuple(compacted_uris)


def normalize_data(data: Union[None, JSONdict], context: Dict[str, Any]) -> Union[None, JSONdict]:
    """
    Normalizes JSON-LD data using a given context.

    Args:
        data (Union[None, JSONdict]): A JSON-LD data dict to be normalized.
        context (Dict[str, Any]): A dictionary containing a mapping of prefixes to base URLs.

    Returns:
        Union[None, JSONdict]: A normalized JSON-LD data dict.

    Examples:
        >>> context = {'foaf': 'http://xmlns.com/foaf/0.1/'}
        >>> data = {
        ...     "foaf:name": "John Smith",
        ...     "foaf:age": 35,
        ...     "foaf:knows": {
        ...         "foaf:name": "Jane Doe",
        ...         "foaf:age": 25
        ...     }
        ... }
        >>> normalize_data(data, context)
        {
            "http://xmlns.com/foaf/0.1/name": "John Smith",
            "http://xmlns.com/foaf/0.1/age": 35,
            "http://xmlns.com/foaf/0.1/knows": {
                "http://xmlns.com/foaf/0.1/name": "Jane Doe",
                "http://xmlns.com/foaf/0.1/age": 25
            }
        }

    """
    if data is None:
        return data
    normalized: JSONdict = {}
    for key, value in data.items():
        assert isinstance(key, str)
        if key == "@context":
            continue
        elif key.startswith("Q"):
            expanded_key = key
        else:
            result = expand_uri(key, context)
            assert isinstance(result, str)  # for type checking
            expanded_key = result
        assert expanded_key.startswith("http") or expanded_key.startswith("@") or expanded_key.startswith("Q")

        if hasattr(value, "__len__") and len(value) == 0:
            pass
        elif expanded_key == "@id":
            if value.startswith("http"):
                # do not take local ids, e.g., those starting with "_"
                normalized[expanded_key] = value
        elif expanded_key == "@type":
            normalized[expanded_key] = value
        elif isinstance(value, (list, tuple)):
            normalized[expanded_key] = []
            for item in value:
                if isinstance(item, dict):
                    normalized[expanded_key].append(normalize_data(item, context))
                else:
                    normalized[expanded_key].append(item)
        elif isinstance(value, dict):
            normalized[expanded_key] = normalize_data(value, context)
        else:
            normalized[expanded_key] = value
    return normalized


def in_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == "ZMQInteractiveShell":
            return True
        elif shell == "TerminalInteractiveShell":
            return False
        else:
            return False
    except NameError:
        return False


def expand_filter(filter_dict: Dict[str, Any]):
    """
    Expand single-level filter specification (provided by user) into
    a multi-level dict as required by the query-generation machinery.

    Example:
    >>> filter = {
    ...    "developers__affiliations__member_of__alias": "CNRS",
    ...    "digital_identifier__identifier": "https://doi.org/some-doi"
    ... }
    >>> expand_filter(filter)
    {
        "developers": {
            "affiliations": {
                "member_of": {
                    "alias": "CNRS
                }
            }
        },
        "digital_identifier": {
            "identifier": "https://doi.org/some-doi"
        }
    }
    """
    expanded = {}
    for key, value in filter_dict.items():
        if hasattr(value, "items"):
            raise TypeError("Filter specifications should be a single-level dict, without nesting")
        local_path = expanded
        parts = key.split("__")
        for part in parts[:-1]:
            local_path[part] = {}
            local_path = local_path[part]
        local_path[parts[-1]] = value
    return expanded


def sha1sum(filename):
    BUFFER_SIZE = 128 * 1024
    h = hashlib.sha1()
    with open(filename, "rb") as fp:
        while True:
            data = fp.read(BUFFER_SIZE)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


class LogEntry:
    """
    Represents an entry in an activity log.

    Attributes:
        cls (str): The name of the class of the Knowledge Grapg object.
        id (Optional[str]): The identifer of the object being logged.
        delta (Optional[JSONdict]): A dictionary containing the changes made to the object.
        space (Optional[str]): The Knowledge Graph space containing the object.
        type_ (str): The type of the log entry.
    """

    def __init__(
        self,
        cls: str,
        id: Optional[str],
        delta: Optional[JSONdict],
        space: Optional[str],
        type_: str,
    ):
        self.cls = cls
        self.id = id
        self.delta = delta
        self.space = space
        self.type = type_

    def __repr__(self):
        return f"{self.type}: {self.cls}({self.id}) in '{self.space}'"

    def as_dict(self):
        return {
            "cls": self.cls,
            "id": self.id,
            "delta": self.delta,
            "space": self.space,
            "type_": self.type
        }


class ActivityLog:
    """
    Represents a log of activities performed on Knowledge Graph objects.

    Attributes:
        entries (List[LogEntry]): A list of LogEntry objects representing the activities performed.
    """

    def __init__(self):
        self.entries = []

    def update(self, item: KGObject, delta: Optional[JSONdict], space: Optional[str], entry_type: str):
        """
        Adds a new log entry to the activity log.

        Args:
            item (KGObject): The object being logged.
            delta (Optional[JSONdict]): A dictionary containing the changes made to the object.
            space (Optional[str]): The Knowledge Graph space containing the object.
            entry_type (str): The type of the log entry.
        """
        self.entries.append(LogEntry(item.__class__.__name__, item.uuid, delta, space, entry_type))

    def __repr__(self):
        return "\n".join((str(entry) for entry in self.entries))


TERMS_OF_USE = """
# EBRAINS Knowledge Graph Data Platform Citation Requirements

This text is provided to describe the requirements for citing datasets,
models and software found via EBRAINS Knowledge Graph Data Platform (KG):
 https://kg.ebrains.eu/search.
It is meant to provide a more human-readable form of key parts of the
KG Terms of Service, but in the event of disagreement between the KG Terms of
Service and these Citation Requirements, the former is to be taken as authoritative.

## Dataset, model and software licensing

Datasets, models and software in the KG have explicit licensing conditions attached.
The license is typically one of the Creative Commons licenses.
You must follow the licensing conditions attached to the dataset, model or software,
including all restrictions on commercial use, requirements for attribution or
requirements to share-alike.

## EBRAINS Knowledge Graph citation policy

If you use content or services from the EBRAINS Knowledge Graph (Search or API)
to advance a scientific publication you must follow the following citation policy:

1. For a dataset or model which is released under a Creative Commons license
   which includes "Attribution":

    1. Cite the dataset / model as defined in the provided citation instructions
       ("Cite dataset / model") and - if available - also cite the primary publication listed

    or

    2. in cases where neither citation instructions nor a primary publication are provided,
       and only in such cases, the names of the contributors should be cited
       (Data / model provided by Contributor 1, Contributor 2, …, and Contributor N) .

2. For software, please cite as defined in the software's respective citation policy.
   If you can't identify a clear citation policy for the software in question,
   use the open source repository as the citation link.

3. For EBRAINS services which were key in attaining your results, please consider
   citing the corresponding software which the service relies on,
   including but not limited to:

    EBRAINS Knowledge Graph, "https://kg.ebrains.eu"

Failure to cite datasets, models, or software used in another publication or
presentation would constitute scientific misconduct.
Failure to cite datasets, models, or software used in a scientific publication
must be corrected by an Erratum and correction of the given article if it was
discovered post-publication.

## Final thoughts

Citations are essential for encouraging researchers to release their datasets,
models and software through the KG or other scientific sharing platforms.
Your citation may help them to get their next job or next grant and will
ultimately encourage researchers to produce and release more useful open data
and open source. Make science more reproducible and more efficient.
"""


def accepted_terms_of_use(client: KGClient, accept_terms_of_use: bool = False) -> bool:
    if accept_terms_of_use or client.accepted_terms_of_use:
        return True
    else:
        if in_notebook():
            from IPython.display import display, Markdown  # type: ignore

            display(Markdown(TERMS_OF_USE))
        else:
            print(TERMS_OF_USE)
        user_response = input("Do you accept the EBRAINS KG Terms of Service? ")
        if user_response in ("y", "Y", "yes", "YES"):
            client.accepted_terms_of_use = True
            return True
        else:
            warnings.warn("Please accept the terms of use before downloading the dataset")
            return False


def initialise_instances(class_list):
    """Cast openMINDS instances to their fairgraph subclass"""
    for cls in class_list:
        cls.set_error_handling(None)
        # find parent openMINDS class
        for parent_cls in cls.__mro__[1:]:
            if parent_cls.__name__ == cls.__name__:
                # could also do this by looking for issubclass(parent_cls, openminds.Node)
                break
        for key, value in parent_cls.__dict__.items():
            if isinstance(value, parent_cls):
                fg_instance = cls.from_jsonld(value.to_jsonld())
                fg_instance._space = cls.default_space
                setattr(cls, key, fg_instance)
        cls.set_error_handling("log")


def handle_scope_keyword(scope, release_status):
    """
    The keyword 'scope' has been renamed 'release_status',
    use of 'scope' is deprecated but still accepted.
    """
    if scope in ("released", "in progress", "any"):
        warnings.warn(
            "The keyword 'scope' is deprecated, and will be removed in version 1.0; it has been renamed to 'release_status'",
            DeprecationWarning,
            stacklevel=2,
        )
        return scope
    else:
        return release_status
