from copy import deepcopy
import os
import re
from uuid import uuid4
from typing import Optional

from requests.exceptions import RequestException, SSLError

from fairgraph.base import OPENMINDS_VERSION
from fairgraph.caching import object_cache, save_cache
from fairgraph.client import KGClient
from fairgraph.errors import AuthenticationError, AuthorizationError
from fairgraph.utility.name_matching import KG_NAMELIKE_PROPERTIES
from fairgraph.utility import as_list

import pytest

kg_host = "core.kg-ppd.ebrains.eu"  # don't use production for testing
# kg_host = "core.kg.ebrains.eu"  # don't use production for testing
have_kg_connection = False
no_kg_err_msg = "No KG connection - have you set the environment variable KG_AUTH_TOKEN?"

try:
    client = KGClient(host=kg_host, allow_interactive=False)
except AuthenticationError:
    pass
except SSLError:
    no_kg_err_msg = "No KG connection - SSL certificate may have expired"
except RequestException:
    # e.g. the KG is down for maintenance.
    no_kg_err_msg = f"No KG connection - could not reach {kg_host}"
else:
    try:
        user_info = client.user_info()
    except (AuthenticationError, AuthorizationError):
        pass
    else:
        if user_info:
            have_kg_connection = True


def skip_if_no_connection(f):
    return pytest.mark.skipif(not have_kg_connection, reason=no_kg_err_msg)(f)


def skip_if_using_production_server(f):
    return pytest.mark.skipif("kg-ppd" not in kg_host, reason="Using production server for testing")(f)


@pytest.fixture(scope="session")
def kg_client():
    return client


@pytest.fixture(scope="session")
def kg_client_curator():
    if "KG_AUTH_TOKEN_CURATOR" in os.environ:
        return KGClient(host=kg_host, allow_interactive=False, token=os.environ["KG_AUTH_TOKEN_CURATOR"])
    else:
        return None


class MockKGResponse:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error
        self.total = len(data) if data else 0


class MockKGClient:
    _private_space = "myspace_1234"
    _max_retries = 2
    _retry_backoff = 5.0

    def __init__(self, openminds_version: str = OPENMINDS_VERSION):
        if openminds_version not in ("v4", "v5"):
            raise ValueError(f"openminds_version must be 'v4' or 'v5', got {openminds_version!r}")
        self.openminds_version = openminds_version
        self.instances = {}
        self.cache = {}
        self.updates = []  # (instance_id, payload) for each update_instance() call
        self.replacements = []  # (instance_id, payload) for each replace_instance() call

    def retrieve_query(self, query_label):
        return {"@id": f"mock-query-{query_label}"}

    def instance_from_full_uri(
        self,
        uri: str,
        use_cache: bool = True,
        release_status: str = "released",
        require_full_data: bool = True,
    ):
        mock_id = "http://example.org/00000000-0000-0000-0000-000000000000"
        if uri in self.instances:
            return deepcopy(self.instances[uri])
        elif uri == mock_id:
            return {"@id": mock_id, "@type": ["https://openminds.om-i.org/types/Model"]}
        else:
            raise NotImplementedError

    # The names a `by_name()` search generates a filter for.
    NAMELIKE_QUERY_PROPERTIES = tuple(f"Q{prop_name}" for prop_name in KG_NAMELIKE_PROPERTIES)

    # Controlled terms this mock knows about, as (name, node type).
    CANNED_TERMS = (
        ("protein structure", "ModelAbstractionLevel"),
        ("subcellular", "ModelScope"),
        ("Mus musculus", "Species"),
        ("astrocyte", "CellType"),
        ("amygdala", "UBERONParcellation"),
    )

    @staticmethod
    def _filter_selects(spec, candidate):
        """
        Whether a query filter would select an instance whose name-like property is `candidate`.

        `by_name()` filters with a regular expression, while existence queries filter with an exact match (which the KG applies case-insensitively),
        so both have to be understood here. The regex is applied case-insensitively, to match the KG.
        """
        value = spec.get("value", None)
        if not isinstance(value, str):
            return False
        if spec.get("op", None) == "REGEX":
            return re.search(value, candidate, re.IGNORECASE) is not None
        if spec.get("op", None) == "EQUALS":
            return candidate.lower() == value.lower()
        return candidate in value

    def query(
        self,
        query,
        filter=None,
        space=None,
        size=100,
        from_index=0,
        release_status="released",
        restrict_to_spaces=None,
    ):
        namelike_filters = [
            prop["filter"]
            for prop in query["structure"]
            if prop.get("propertyName", "") in self.NAMELIKE_QUERY_PROPERTIES and prop.get("filter", None)
        ]
        if namelike_filters:

            def selects(candidate):
                return any(self._filter_selects(spec, candidate) for spec in namelike_filters)

            if selects("Dummy new model"):
                return MockKGResponse(None)
            for term_name, node_type in self.CANNED_TERMS:
                if selects(term_name):
                    return MockKGResponse(
                        [
                            {
                                "https://openminds.om-i.org/props/name": term_name,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": [f"https://openminds.om-i.org/types/{node_type}"],
                            }
                        ]
                    )
        else:
            for prop in query["structure"]:
                if prop.get("propertyName", "") == "Qgiven_name":
                    filter_value = prop["filter"]["value"]
                    if filter_value == "Thorin":
                        return MockKGResponse([])
        matches = self._match_instances(query)
        if matches is None and namelike_filters and not self.instances:
            # nothing has been seeded, so a name-like search legitimately finds nothing.
            # Any other query shape `_match_instances` could not honour still raises below.
            matches = []
        if matches is not None:
            return MockKGResponse(matches)
        raise NotImplementedError("case not yet handled by mock client")

    SUPPORTED_FILTER_OPS = ("EQUALS", "CONTAINS", "REGEX")

    def _match_instances(self, query):
        """
        Match any instances that have been added to the mock KG (either seeded by a
        test or created through `create_new_instance`) against a query definition.

        Returns None for any query shape this mock cannot honour faithfully, so that
        the caller falls back to raising NotImplementedError. That matters more than
        it might seem: silently returning a plausible-but-wrong match set would let a
        test pass for the wrong reason.

        Note that the hard-coded branches in `query` are consulted first, so a test
        that seeds an instance matching one of the names they special-case will get
        the canned response rather than the seeded one.
        """
        if not self.instances:
            return None
        node_type = query.get("meta", {}).get("type", None)
        if node_type is None:
            return None
        filters = []
        for prop in query.get("structure", []):
            if "structure" in prop:
                return None  # a filter on a nested node, which we don't traverse
            spec = prop.get("filter", None)
            if not spec or "value" not in spec:
                continue
            path = prop.get("path", None)
            if not isinstance(path, str) or not path.startswith("http"):
                return None  # e.g. filtering on "@id", which we don't support here
            if spec.get("op") not in self.SUPPORTED_FILTER_OPS:
                return None
            filters.append((path, spec["op"], spec["value"]))
        matches = []
        for instance in self.instances.values():
            if node_type not in as_list(instance.get("@type", [])):
                continue
            if all(self._value_matches(instance.get(path, None), op, value) for path, op, value in filters):
                match = deepcopy(instance)
                if "https://core.kg.ebrains.eu/vocab/meta/space" in match:
                    # the query API returns the space under the name given in the query definition
                    match["https://schema.hbp.eu/myQuery/space"] = match["https://core.kg.ebrains.eu/vocab/meta/space"]
                matches.append(match)
        return matches

    @staticmethod
    def _value_matches(stored, op, value):
        for item in as_list(stored):
            if op == "REGEX":
                # the KG matches regular expressions case-insensitively
                if isinstance(item, str) and isinstance(value, str) and re.search(value, item, re.IGNORECASE):
                    return True
                continue
            if item == value:
                return True
            if op == "EQUALS" and isinstance(item, str) and isinstance(value, str) and item.lower() == value.lower():
                # the KG ignores case, but not whitespace, when matching
                return True
            if op == "CONTAINS" and isinstance(item, str) and isinstance(value, str) and value in item:
                return True
        return False

    def create_new_instance(self, data, space, instance_id=None):
        assert space is not None
        assert data is not None
        instance = deepcopy(data)
        instance["@id"] = instance_id or str(uuid4())
        instance["https://core.kg.ebrains.eu/vocab/meta/space"] = space
        self.instances[instance["@id"]] = instance
        return instance

    def update_instance(self, instance_id, data):
        assert instance_id is not None
        assert data is not None
        self.updates.append((instance_id, deepcopy(data)))

    def replace_instance(self, instance_id, data):
        assert instance_id is not None
        assert data is not None
        self.replacements.append((instance_id, deepcopy(data)))

    def uri_from_uuid(self, uuid):
        return f"https://kg.ebrains.eu/api/instances/{uuid}"


@pytest.fixture
def mock_client():
    return MockKGClient()


@pytest.fixture
def clear_caches():
    """
    Ensure a test starts and finishes with empty global caches.

    `save_cache` and `object_cache` are module-level globals, so tests that
    exercise them would otherwise leak into one another.
    """
    save_cache.clear()
    object_cache.clear()
    yield
    save_cache.clear()
    object_cache.clear()
