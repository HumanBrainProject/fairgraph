import os
import pytest

from kg_core.response import Error as KGError
from fairgraph.kgobject import KGObject
from fairgraph.queries import Query, QueryProperty, Filter
from fairgraph.errors import AuthenticationError, AuthorizationError, ResourceExistsError
from fairgraph.base import OPENMINDS_VERSION
from .utils import kg_client, kg_client_curator, skip_if_no_connection, MockKGResponse


@skip_if_no_connection
def test_spaces(kg_client):
    result = kg_client.spaces()
    assert isinstance(result, list)
    for space in result:
        assert isinstance(space.name, str)
        assert not space.permissions


@skip_if_no_connection
def test_spaces_with_permissions(kg_client):
    result = kg_client.spaces(permissions=["RELEASE"])
    assert isinstance(result, list)
    for space in result:
        assert "RELEASE" in space.permissions


@skip_if_no_connection
def test_spaces_with_permissions_True(kg_client):
    result = kg_client.spaces(permissions=True)
    assert isinstance(result, list)
    for space in result:
        assert space.permissions


@skip_if_no_connection
def test_spaces_names_only(kg_client):
    result = kg_client.spaces(names_only=True)
    assert isinstance(result, list)
    assert all(isinstance(space, str) for space in result)


@skip_if_no_connection
def test_query_filter_by_space(kg_client):

    query = Query(
        node_type="https://openminds.om-i.org/types/Model",
        label="fg-testing-model",
        properties=[
            QueryProperty("@type"),
            QueryProperty(
                "https://core.kg.ebrains.eu/vocab/meta/space",
                name="project_id",
                filter=Filter("EQUALS", value="model"),
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/fullName",
                name="fullName",
                filter=Filter("CONTAINS", parameter="name"),
                sorted=True,
                required=True,
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/custodian",
                name="custodian",
                type_filter="https://openminds.om-i.org/types/Person",
                properties=[
                    QueryProperty(
                        "https://openminds.om-i.org/props/familyName",
                        name="familyName",
                    ),
                ],
            ),
        ],
    )
    results = kg_client.query(
        filter=None,
        query=query.serialize(),
        instance_id=None,
        from_index=0,
        size=1000,
        release_status="in progress",
        id_key="uri",
    )
    spaces = set(result["project_id"] for result in results.data)
    if len(spaces) > 0:
        assert len(spaces) == 1
        assert "model" == list(spaces)[0]


@skip_if_no_connection
def test_get_admin_client(kg_client):
    admin_client = kg_client._kg_admin_client


@skip_if_no_connection
def test_list_scopes(kg_client):

    def _get_models(release_status):
        return kg_client.list(
            target_type="https://openminds.om-i.org/types/Model",
            space="model",
            from_index=0,
            size=10000,
            release_status=release_status,
        )

    released_models = _get_models("released")
    in_progress_models = _get_models("in progress")
    all_models = _get_models("any")
    # following assertion is because some models will appear in both released and in progress
    assert released_models.total + in_progress_models.total >= all_models.total


@skip_if_no_connection
def test_get_token(kg_client):
    assert kg_client.token == os.environ["KG_AUTH_TOKEN"]


@skip_if_no_connection
def test__check_response_with_error(kg_client):
    with pytest.raises(Exception) as err:
        kg_client.update_instance(instance_id="https://kg.ebrains.eu/api/instances/charliechaplin", data={})
        assert "404" in str(err)
    with pytest.raises(AuthorizationError):
        kg_client._check_response(MockKGResponse({}, error=KGError(code=403)))
    with pytest.raises(AuthenticationError):
        kg_client._check_response(MockKGResponse({}, error=KGError(code=401)))
    with pytest.raises(ResourceExistsError):
        kg_client._check_response(MockKGResponse({}, error=KGError(code=409)))
    with pytest.raises(Exception):
        kg_client._check_response(MockKGResponse({}, error=KGError(code=404)), ignore_not_found=False)

    response = MockKGResponse({}, error=KGError(code=404))
    assert kg_client._check_response(response, ignore_not_found=True) is response


@skip_if_no_connection
def test_get_instance_from_cache(kg_client):
    instance_id = "https://kg.ebrains.eu/api/instances/5ed1e9f9-482d-41c7-affd-f1aa887bd618"
    kg_client.cache.pop(instance_id, None)
    instance1 = kg_client.instance_from_full_uri(instance_id)
    assert instance_id in kg_client.cache
    assert kg_client.cache[instance_id] == instance1
    instance2 = kg_client.instance_from_full_uri(instance_id, use_cache=True)
    assert instance2 is instance1


@skip_if_no_connection
def test_get_instance_no_cache(kg_client):
    instance_id = "https://kg.ebrains.eu/api/instances/5ed1e9f9-482d-41c7-affd-f1aa887bd618"
    instance1 = kg_client.instance_from_full_uri(instance_id, use_cache=False, release_status="any")
    instance2 = kg_client.instance_from_full_uri(instance_id, use_cache=False)
    assert instance2 is not instance1


@skip_if_no_connection
def test_get_non_existent_instance(kg_client):
    instance_id = "https://kg.ebrains.eu/api/instances/99999999-9999-9999-9999-999999999999"
    instance1 = kg_client.instance_from_full_uri(instance_id, use_cache=False)
    assert instance1 is None


@skip_if_no_connection
def test_retrieve_query(kg_client):
    queries = kg_client.retrieve_query("dataset")


@skip_if_no_connection
def test_store_and_retrieve_query(kg_client, mocker):
    mocker.patch.object(kg_client._kg_client.queries, "list_per_root_type", lambda search: MockKGResponse({}))
    mocker.patch.object(kg_client._kg_client.queries, "save_query", lambda **kw: MockKGResponse({}))
    kg_client.store_query("not-a-real-query", {"a": 1}, "not-a-real-space")


@skip_if_no_connection
def test_configure_space(kg_client, mocker):
    class MockType(KGObject):
        schema_version = OPENMINDS_VERSION
        type_ = "hello"

    mocker.patch.object(kg_client._kg_admin_client, "create_space_definition", lambda space: None)
    mocker.patch.object(kg_client._kg_admin_client, "assign_type_to_space", lambda space, target_type: None)
    kg_client.configure_space("not-a-real-space-name", [MockType()])
    with pytest.raises(ValueError):
        kg_client.configure_space()


@skip_if_no_connection
def test_is_released(kg_client_curator):
    if kg_client_curator is None:
        pytest.skip("Need to set environment variable KG_AUTH_TOKEN_CURATOR")
    instance_id = "https://kg.ebrains.eu/api/instances/5ed1e9f9-482d-41c7-affd-f1aa887bd618"
    kg_client_curator.is_released(instance_id, with_children=True)
    kg_client_curator.is_released(instance_id, with_children=False)


@skip_if_no_connection
def test_create_new_instance(kg_client, mocker):
    with pytest.raises(ValueError) as err:
        kg_client.create_new_instance({"@id": None}, space="not-a-real-space")
        assert "undefined ids" in str(err)

    mocker.patch.object(kg_client._kg_client.instances, "create_new", lambda **kw: MockKGResponse(kw["payload"]))
    response = kg_client.create_new_instance({"a": 1, "b": 2}, space="not-a-real-space")
    assert response == {"a": 1, "b": 2}

    mocker.patch.object(
        kg_client._kg_client.instances,
        "create_new_with_id",
        lambda **kw: MockKGResponse({**kw["payload"], **{"@id": kw["instance_id"]}}),
    )
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = kg_client.create_new_instance({"a": 1, "b": 2}, instance_id=fake_id, space="not-a-real-space")
    assert response == {"@id": fake_id, "a": 1, "b": 2}


@skip_if_no_connection
def test_replace_instance(kg_client, mocker):
    mocker.patch.object(
        kg_client._kg_client.instances,
        "contribute_to_full_replacement",
        lambda **kw: MockKGResponse({**kw["payload"], **{"@id": kw["instance_id"]}}),
    )
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = kg_client.replace_instance(fake_id, {"a": 1, "b": 2})
    assert response == {"@id": fake_id, "a": 1, "b": 2}


@skip_if_no_connection
def test_delete_instance(kg_client, mocker):
    mocker.patch.object(kg_client._kg_client.instances, "delete")
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = kg_client.delete_instance(fake_id)
    kg_client._kg_client.instances.delete.assert_called_once_with(fake_id)


@pytest.fixture
def offline_kg_client(mocker):
    """A KGClient that can be constructed without network access, for testing
    behaviour that doesn't require a real KG. The underlying kg-core SDK methods
    must be patched per-test."""
    from fairgraph.client import KGClient

    client = KGClient(token="fake-token", allow_interactive=False)
    # `instance_from_full_uri` uses this to build the cache key after writes
    mocker.patch.object(
        client._kg_client.instances._kg_config,
        "id_namespace",
        "https://kg.ebrains.eu/api/instances/",
        create=True,
    )
    return client


class TestCacheInvalidationOnWrite:
    """Regression tests for the bug where writes left stale entries in
    `client.cache`, causing subsequent `from_id(use_cache=True)` calls to
    return out-of-date data and `save()` to no-op on what looked like a
    legitimate modification. See issue #110."""

    uuid = "00000000-0000-0000-0000-000000000000"
    uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000000"

    def test_update_instance_invalidates_cache(self, offline_kg_client, mocker):
        offline_kg_client.cache[self.uri] = {"@id": self.uri, "stale": True}
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "contribute_to_partial_replacement",
            lambda **kw: MockKGResponse({"@id": self.uri}),
        )
        offline_kg_client.update_instance(self.uuid, {"some": "patch"})
        assert self.uri not in offline_kg_client.cache

    def test_replace_instance_invalidates_cache(self, offline_kg_client, mocker):
        offline_kg_client.cache[self.uri] = {"@id": self.uri, "stale": True}
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "contribute_to_full_replacement",
            lambda **kw: MockKGResponse({"@id": self.uri}),
        )
        offline_kg_client.replace_instance(self.uuid, {"some": "data"})
        assert self.uri not in offline_kg_client.cache

    def test_delete_instance_invalidates_cache(self, offline_kg_client, mocker):
        offline_kg_client.cache[self.uri] = {"@id": self.uri}
        mocker.patch.object(offline_kg_client._kg_client.instances, "delete", return_value=None)
        offline_kg_client.delete_instance(self.uuid)
        assert self.uri not in offline_kg_client.cache

    def test_unlink_after_refetch_sends_patch(self, offline_kg_client, mocker):
        """End-to-end: this is the user-visible bug. Load a DatasetVersion,
        link a subject, save; re-load it via `from_id`, set the link back to
        `None`, save again — the second save must PATCH studiedSpecimen=None,
        not be a silent no-op."""
        from fairgraph.openminds.core import DatasetVersion, Subject

        sub_uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000abc"
        studied_specimen_path = "https://openminds.om-i.org/props/studiedSpecimen"
        # Server-side state of the DSV, mutated by each PATCH so subsequent
        # `instance_from_full_uri` calls see fresh data.
        server_state = {
            "@id": self.uri,
            "@type": ["https://openminds.om-i.org/types/DatasetVersion"],
            "http://schema.org/identifier": [self.uri],
            "https://core.kg.ebrains.eu/vocab/meta/space": "myspace",
        }

        def get_by_id(stage, instance_id, extended_response_configuration):
            return MockKGResponse(dict(server_state))

        def contribute_to_partial_replacement(instance_id, payload, extended_response_configuration):
            for key, value in payload.items():
                if value is None:
                    server_state.pop(key, None)
                else:
                    server_state[key] = value
            return MockKGResponse(dict(server_state))

        mocker.patch.object(offline_kg_client._kg_client.instances, "get_by_id", get_by_id)
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "contribute_to_partial_replacement",
            contribute_to_partial_replacement,
        )

        # 1. Load fresh, link a subject, save.
        dsv = DatasetVersion.from_id(self.uuid, offline_kg_client, scope="any")
        dsv.studied_specimens = [Subject(id=sub_uri)]
        dsv.save(offline_kg_client, space="myspace", recursive=False)
        assert studied_specimen_path in server_state, "first save should have linked the subject"

        # 2. Re-fetch via from_id. Before the fix, this would have returned
        # stale cached data with no studiedSpecimen.
        dsv2 = DatasetVersion.from_id(self.uuid, offline_kg_client, scope="any")
        assert dsv2.studied_specimens is not None, (
            "re-fetched object must see the link added by the prior save"
        )

        # 3. Unlink and save. The PATCH must clear studiedSpecimen on the server.
        dsv2.studied_specimens = None
        dsv2.save(offline_kg_client, space="myspace", recursive=False)
        assert studied_specimen_path not in server_state, (
            "second save should have sent a PATCH that cleared studiedSpecimen"
        )

    def test_save_marks_raw_remote_data_stale(self, offline_kg_client, mocker):
        """After a successful update/replace, `_raw_remote_data` must be set
        to None so it can't be silently out of sync with the cache and with
        the actual server state. exists() repopulates it on demand."""
        from fairgraph.openminds.core import DatasetVersion

        server_state = {
            "@id": self.uri,
            "@type": ["https://openminds.om-i.org/types/DatasetVersion"],
            "http://schema.org/identifier": [self.uri],
            "https://core.kg.ebrains.eu/vocab/meta/space": "myspace",
            "https://openminds.om-i.org/props/shortName": "original",
        }

        def get_by_id(stage, instance_id, extended_response_configuration):
            return MockKGResponse(dict(server_state))

        def contribute_to_partial_replacement(instance_id, payload, extended_response_configuration):
            for key, value in payload.items():
                if value is None:
                    server_state.pop(key, None)
                else:
                    server_state[key] = value
            return MockKGResponse(dict(server_state))

        mocker.patch.object(offline_kg_client._kg_client.instances, "get_by_id", get_by_id)
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "contribute_to_partial_replacement",
            contribute_to_partial_replacement,
        )

        dsv = DatasetVersion.from_id(self.uuid, offline_kg_client, scope="any")
        assert dsv._raw_remote_data is not None  # populated by from_id

        dsv.short_name = "updated"
        dsv.save(offline_kg_client, space="myspace", recursive=False)

        assert dsv._raw_remote_data is None, (
            "_raw_remote_data must be invalidated after a successful update"
        )
