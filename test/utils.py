from copy import deepcopy
from uuid import uuid4
from requests.exceptions import SSLError
from fairgraph.client import KGClient
from fairgraph.errors import AuthenticationError

import pytest

kg_host = "core.kg-ppd.ebrains.eu"  # don't use production for testing
have_kg_connection = False
no_kg_err_msg = "No KG connection - have you set the environment variable KG_AUTH_TOKEN?"

try:
    client = KGClient(host=kg_host)
except AuthenticationError:
    pass
except SSLError:
    no_kg_err_msg = "No KG connection - SSL certificate may have expired"
else:
    if client.user_info():
        have_kg_connection = True


def skip_if_no_connection(f):
    return pytest.mark.skipif(not have_kg_connection, reason=no_kg_err_msg)(f)


def skip_if_using_production_server(f):
    return pytest.mark.skipif("kg-ppd" not in kg_host, reason="Using production server for testing")(f)


@pytest.fixture(scope="session")
def kg_client():
    return client


class MockKGResponse:
    def __init__(self, data, error=None):
        self.data = data
        self.error = error
        self.total = len(data) if data else 0


class MockKGClient:
    _private_space = "myspace_1234"

    def __init__(self):
        self.instances = {}

    def retrieve_query(self, query_label):
        return {"@id": f"mock-query-{query_label}"}

    def instance_from_full_uri(
        self,
        uri: str,
        use_cache: bool = True,
        scope: str = "released",
        require_full_data: bool = True,
    ):
        if uri == "0000":
            return {"@id": "0000", "@type": ["https://openminds.ebrains.eu/core/Model"]}
        else:
            raise NotImplementedError

    def query(self, query, filter=None, space=None, size=100, from_index=0, scope="released"):
        for prop in query["structure"]:
            if prop.get("propertyName", "") in ("Qname", "Qfull_name"):
                filter_value = prop["filter"]["value"]
                if "Dummy new model" in filter_value:
                    return MockKGResponse(None)
                elif "protein structure" in filter_value:
                    return MockKGResponse(
                        [
                            {
                                "vocab:name": filter_value,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": ["https://openminds.ebrains.eu/controlledTerms/ModelAbstractionLevel"],
                            }
                        ]
                    )
                elif "subcellular" in filter_value:
                    return MockKGResponse(
                        [
                            {
                                "vocab:name": filter_value,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": ["https://openminds.ebrains.eu/controlledTerms/ModelScope"],
                            }
                        ]
                    )
                elif "Mus musculus" in filter_value:
                    return MockKGResponse(
                        [
                            {
                                "vocab:name": filter_value,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": ["https://openminds.ebrains.eu/controlledTerms/Species"],
                            }
                        ]
                    )
                elif "astrocyte" in filter_value:
                    return MockKGResponse(
                        [
                            {
                                "vocab:name": filter_value,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": ["https://openminds.ebrains.eu/controlledTerms/CellType"],
                            }
                        ]
                    )
                elif "amygdala" in filter_value:
                    return MockKGResponse(
                        [
                            {
                                "vocab:name": filter_value,
                                "@id": "fake_uuid",
                                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                                "@type": ["https://openminds.ebrains.eu/controlledTerms/UBERONParcellation"],
                            }
                        ]
                    )
                elif "The Lonely Mountain" in filter_value:
                    return MockKGResponse([])
            elif prop.get("propertyName", "") == "Qgiven_name":
                filter_value = prop["filter"]["value"]
                if filter_value == "Thorin":
                    return MockKGResponse([])
        raise NotImplementedError("case not yet handled by mock client")

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

    def replace_instance(self, instance_id, data):
        assert instance_id is not None
        assert data is not None


@pytest.fixture
def mock_client():
    return MockKGClient()
