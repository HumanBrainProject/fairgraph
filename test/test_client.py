import copy
import os
import pytest
import requests

from kg_core.request import Stage, Pagination
from kg_core.response import Error as KGError
from fairgraph.kgobject import KGObject
from fairgraph.queries import Query, QueryProperty, Filter
from fairgraph.errors import AuthenticationError, AuthorizationError, KGConnectionError, ResourceExistsError
from fairgraph.base import OPENMINDS_VERSION
from fairgraph.client import KGClient
from .utils import (
    kg_client,
    kg_client_curator,
    mock_client,
    skip_if_no_connection,
    MockKGResponse,
)


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
def test_space_info_tolerates_unknown_types(kg_client):
    # Regression test for #113. A KG space may contain types that have no fairgraph
    # class -- the KG's own internal types, for example
    # "https://core.kg.ebrains.eu/doi/AdditionalDoiInformation". space_info() used to
    # raise ValueError for those, so a single unrecognised type made the whole space
    # listing fail. They are now returned keyed by their type IRI instead.
    #
    # "controlled" with release_status="in progress" is the case from the bug report.
    info = kg_client.space_info("controlled", release_status="in progress")

    assert isinstance(info, dict)
    for key, count in info.items():
        assert isinstance(count, int)
        if isinstance(key, str):
            # an unmapped type, keyed by its IRI
            assert key.startswith("http"), f"unmapped type key is not an IRI: {key!r}"
        else:
            # a fairgraph/openMINDS class
            assert isinstance(key, type), f"unexpected key type: {key!r}"
            assert hasattr(key, "type_"), f"class key has no type_: {key!r}"


@skip_if_no_connection
def test_space_info_reports_unmapped_types_by_iri(kg_client):
    # Companion to the test above: check that unmapped types really do occur and are
    # handled, rather than the tolerance never being exercised. Scans the spaces the
    # user can read until it finds one, since which spaces contain internal types
    # depends on the deployment.
    #
    # Skips rather than fails if none is found: that means the KG served nothing
    # unmapped, which is not a fairgraph bug.
    unmapped = {}
    for space_name in kg_client.spaces(names_only=True):
        try:
            info = kg_client.space_info(space_name, release_status="in progress")
        except Exception as err:  # pragma: no cover - the bug this guards against
            pytest.fail(f"space_info({space_name!r}) raised {type(err).__name__}: {err}")
        found = [key for key in info if isinstance(key, str)]
        if found:
            unmapped[space_name] = found

    if not unmapped:
        pytest.skip("no unmapped types found in any accessible space")

    for space_name, keys in unmapped.items():
        for key in keys:
            assert key.startswith("http"), f"in {space_name}: {key!r} is not an IRI"


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


@pytest.mark.parametrize("use_stored_query", [False, True])
@pytest.mark.parametrize("value", ["application/ld+json", "100%"])
def test_query_rejects_plus_and_percent_in_filter_parameters(offline_kg_client, mocker, use_stored_query, value):
    # the KG misreads "+" and "%" in request parameters (see test_kg_misreads_plus_and_percent_in_query_parameters),
    # so the query must not be sent
    for method in ("test_query", "execute_query_by_id"):
        mocker.patch.object(offline_kg_client._kg_client.queries, method, side_effect=AssertionError("query was sent"))
    query = {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000000"}
    with pytest.raises(ValueError, match="Cannot filter on name="):
        offline_kg_client.query(query, filter={"name": value}, use_stored_query=use_stored_query)


@skip_if_no_connection
def test_kg_misreads_plus_and_percent_in_query_parameters(kg_client):
    """
    The KG decodes request parameter values twice (once by Spring, and again in
    DataQueryBuilder.createAqlForFilter() in marmotgraph-core), so a "+" in a filter parameter
    is received as a space, and a "%" that isn't part of a valid escape sequence causes an error.
    KGClient.query() therefore refuses filter parameters containing "+" or "%".

    The second decoding is absent from the v4 branch of marmotgraph-core. If this test starts failing,
    the KG has been fixed, and that check can be removed.
    """
    query = Query(
        node_type="https://openminds.om-i.org/types/ContentType",
        properties=[
            QueryProperty("@type"),
            QueryProperty(
                "https://openminds.om-i.org/props/name",
                name="name",
                filter=Filter("CONTAINS", parameter="name"),
                required=True,
            ),
        ],
    ).serialize()

    def run_query(value):
        # calls kg-core directly, since KGClient.query() rejects these filters
        return kg_client._kg_client.queries.test_query(
            query, additional_request_params={"name": value}, stage=Stage.RELEASED, pagination=Pagination(size=20)
        )

    def names_found(value):
        return [item["name"] for item in run_query(value).data]

    assert "application/ld+json" in names_found("application/ld")
    assert "application/ld+json" not in names_found("application/ld+json")
    assert run_query("100%").error is not None


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
    assert response == {"@id": kg_client.uri_from_uuid(fake_id), "a": 1, "b": 2}


@skip_if_no_connection
def test_replace_instance(kg_client, mocker):
    mocker.patch.object(
        kg_client._kg_client.instances,
        "contribute_to_full_replacement",
        lambda **kw: MockKGResponse({**kw["payload"], **{"@id": kw["instance_id"]}}),
    )
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = kg_client.replace_instance(fake_id, {"a": 1, "b": 2})
    assert response == {"@id": kg_client.uri_from_uuid(fake_id), "a": 1, "b": 2}


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

    # Building the kg-core client fetches the IAM token endpoint from the KG, which
    # fails if the KG is unreachable (e.g. during maintenance).
    mocker.patch("kg_core.__communication.TokenHandler.define_endpoint")

    client = KGClient(token="fake-token", allow_interactive=False)
    # `instance_from_full_uri` uses this to build the cache key after writes
    mocker.patch.object(
        client._kg_client.instances._kg_config,
        "id_namespace",
        "https://kg.ebrains.eu/api/instances/",
        create=True,
    )
    return client


class TestRetryOnConnectionError:
    """Read-only/query-only KGClient methods retry on KGConnectionError; methods that
    modify the KG never do, since retrying a write risks duplicating or corrupting
    data if the original request actually succeeded but its response was lost."""

    def test_retryable_method_recovers_after_connection_error(self, offline_kg_client, mocker):
        mocker.patch("fairgraph.client.sleep")
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "list",
            side_effect=[requests.exceptions.ConnectionError("boom"), MockKGResponse([])],
        )
        response = offline_kg_client.list("https://openminds.om-i.org/types/File")
        assert response.data == []
        assert offline_kg_client._kg_client.instances.list.call_count == 2

    def test_retryable_method_exhausts_retries(self, offline_kg_client, mocker):
        mocker.patch("fairgraph.client.sleep")
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "list",
            side_effect=requests.exceptions.ConnectionError("boom"),
        )
        with pytest.raises(KGConnectionError):
            offline_kg_client.list("https://openminds.om-i.org/types/File")
        assert offline_kg_client._kg_client.instances.list.call_count == offline_kg_client._max_retries + 1

    def test_mutating_method_does_not_retry(self, offline_kg_client, mocker):
        mocker.patch("fairgraph.client.sleep")
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "delete",
            side_effect=requests.exceptions.ConnectionError("boom"),
        )
        fake_id = "00000000-0000-0000-0000-000000000000"
        with pytest.raises(KGConnectionError):
            offline_kg_client.delete_instance(fake_id)
        offline_kg_client._kg_client.instances.delete.assert_called_once()


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


class TestSpaceInfoOffline:
    """space_info() and its callers, exercised without a KG connection.

    Additional regression tests for #113, but no KG connection required.
    """

    known_type = "https://openminds.om-i.org/types/Person"
    unknown_type = "https://core.kg.ebrains.eu/doi/AdditionalDoiInformation"

    def _client_listing(self, mocker, mock_client, items):
        """Equip the mock client with a types.list() returning `items`."""
        data = [mocker.Mock(identifier=iri, occurrences=count) for iri, count in items]
        mock_client._kg_client = mocker.Mock()
        mock_client._kg_client.types.list.return_value = MockKGResponse(data)
        return mock_client

    def test_maps_known_types_to_classes_and_unknown_types_to_iris(self, mock_client, mocker):
        client = self._client_listing(
            mocker, mock_client, [(self.known_type, 3), (self.unknown_type, 7)]
        )

        info = KGClient.space_info(client, "myspace", release_status="in progress")

        by_label = {(k if isinstance(k, str) else k.__name__): v for k, v in info.items()}
        assert by_label == {"Person": 3, self.unknown_type: 7}

        # the known type resolved to a class, the unknown one stayed a string
        assert self.unknown_type in info
        assert all(isinstance(k, type) for k in info if not isinstance(k, str))

    def test_unknown_type_alone_does_not_raise(self, mock_client, mocker):
        # The reported failure: a space whose only unrecognised type made the whole
        # listing raise ValueError.
        client = self._client_listing(mocker, mock_client, [(self.unknown_type, 1)])

        assert KGClient.space_info(client, "myspace", release_status="in progress") == {
            self.unknown_type: 1
        }

    def test_clean_space_lists_both_kinds_then_aborts(self, mock_client, mocker, capsys):
        # clean_space() renders a label for every entry, so it has to cope with string
        # keys as well as classes. Answering "n" exercises the listing without deleting.
        from openminds.registry import lookup_type

        person = lookup_type(self.known_type, mock_client.openminds_version)
        mock_client.space_info = mocker.Mock(return_value={person: 3, self.unknown_type: 7})
        mocker.patch("builtins.input", return_value="n")

        KGClient.clean_space(mock_client, "myspace")

        out = capsys.readouterr().out
        assert "Person 3" in out
        assert f"{self.unknown_type} 7" in out


class TestBareUuidLinks:
    """Marmotgraph v4 gives links to other KG instances as bare UUIDs rather than full URIs.
    The client expands them, so that links can be resolved and compared with instance ids."""

    namespace = "https://kg.ebrains.eu/api/instances/"
    dsv_uuid = "00000000-0000-0000-0000-000000000001"
    target_uuid = "00000000-0000-0000-0000-00000000000a"

    def dataset_version(self, id_):
        return {
            "@id": id_,
            "@type": ["https://openminds.om-i.org/types/DatasetVersion"],
            "http://schema.org/identifier": [self.dsv_uuid, self.namespace + self.dsv_uuid],
            "https://core.kg.ebrains.eu/vocab/meta/space": "dataset",
            "https://openminds.om-i.org/props/accessibility": {"@id": self.target_uuid},
            "https://openminds.om-i.org/props/digitalIdentifier": {"@id": "https://doi.org/10.25493/6640-3XH"},
            "https://openminds.om-i.org/props/technique": [
                {"@id": "https://openminds.om-i.org/instances/technique/spatialRegistration"},
                {"@id": self.target_uuid.upper()},
            ],
        }

    def test_expand_bare_uuids(self):
        from fairgraph.client import expand_bare_uuids

        data = [
            {
                "@id": self.dsv_uuid,
                "http://schema.org/identifier": [self.dsv_uuid],
                "https://openminds.om-i.org/props/link": {"@id": self.target_uuid},
                "https://openminds.om-i.org/props/links": [
                    {"@id": self.target_uuid},
                    {"@id": "https://example.com/x"},
                ],
                "https://openminds.om-i.org/props/embedded": {
                    "@id": f"{self.dsv_uuid}_emb_1",
                    "https://openminds.om-i.org/props/nested": {"@id": self.target_uuid},
                },
                "https://openminds.om-i.org/props/name": self.target_uuid,
            }
        ]
        result = expand_bare_uuids(data, self.namespace)
        assert result is data
        assert data == [
            {
                "@id": self.namespace + self.dsv_uuid,
                "http://schema.org/identifier": [self.dsv_uuid],  # not an "@id", so unchanged
                "https://openminds.om-i.org/props/link": {"@id": self.namespace + self.target_uuid},
                "https://openminds.om-i.org/props/links": [
                    {"@id": self.namespace + self.target_uuid},
                    {"@id": "https://example.com/x"},
                ],
                "https://openminds.om-i.org/props/embedded": {
                    "@id": f"{self.dsv_uuid}_emb_1",
                    "https://openminds.om-i.org/props/nested": {"@id": self.namespace + self.target_uuid},
                },
                "https://openminds.om-i.org/props/name": self.target_uuid,
            }
        ]

    def test_full_uris_unchanged(self):
        from fairgraph.client import expand_bare_uuids

        data = self.dataset_version(self.namespace + self.dsv_uuid)
        for item in data["https://openminds.om-i.org/props/technique"]:
            item["@id"] = "https://openminds.om-i.org/instances/technique/spatialRegistration"
        data["https://openminds.om-i.org/props/accessibility"]["@id"] = self.namespace + self.target_uuid
        expected = copy.deepcopy(data)
        assert expand_bare_uuids(data, self.namespace) == expected

    def test_list(self, offline_kg_client, mocker):
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "list",
            lambda **kw: MockKGResponse([self.dataset_version(self.namespace + self.dsv_uuid)]),
        )
        data = offline_kg_client.list("https://openminds.om-i.org/types/DatasetVersion").data[0]
        assert data["https://openminds.om-i.org/props/accessibility"] == {"@id": self.namespace + self.target_uuid}
        assert data["https://openminds.om-i.org/props/technique"] == [
            {"@id": "https://openminds.om-i.org/instances/technique/spatialRegistration"},
            {"@id": self.namespace + self.target_uuid.upper()},
        ]
        assert data["https://openminds.om-i.org/props/digitalIdentifier"] == {
            "@id": "https://doi.org/10.25493/6640-3XH"
        }

    def test_query(self, offline_kg_client, mocker):
        mocker.patch.object(
            offline_kg_client._kg_client.queries,
            "test_query",
            lambda *args, **kw: MockKGResponse([{"@id": self.dsv_uuid, "accessibility": {"@id": self.target_uuid}}]),
        )
        data = offline_kg_client.query({"@context": {}, "structure": []}).data
        assert data == [
            {"@id": self.namespace + self.dsv_uuid, "accessibility": {"@id": self.namespace + self.target_uuid}}
        ]

    def test_resolve_link(self, offline_kg_client, mocker):
        from fairgraph.openminds.core import DatasetVersion
        from fairgraph.openminds.controlled_terms import ProductAccessibility

        server = {
            self.dsv_uuid: self.dataset_version(self.namespace + self.dsv_uuid),
            self.target_uuid: {
                "@id": self.namespace + self.target_uuid,
                "@type": ["https://openminds.om-i.org/types/ProductAccessibility"],
                "http://schema.org/identifier": [self.namespace + self.target_uuid],
                "https://core.kg.ebrains.eu/vocab/meta/space": "controlled",
                "https://openminds.om-i.org/props/name": "controlled access",
            },
        }
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "get_by_id",
            lambda stage, instance_id, extended_response_configuration: MockKGResponse(
                copy.deepcopy(server[str(instance_id)])
            ),
        )
        dsv = DatasetVersion.from_id(self.dsv_uuid, offline_kg_client)
        assert dsv.accessibility.id == self.namespace + self.target_uuid
        accessibility = dsv.accessibility.resolve(offline_kg_client)
        assert isinstance(accessibility, ProductAccessibility)
        assert accessibility.name == "controlled access"
        assert accessibility.id == dsv.accessibility.id

    def test_openminds_instance(self, offline_kg_client, mocker):
        uri = "https://openminds.om-i.org/instances/technique/spatialRegistration"
        result = mocker.Mock(
            data={"@id": self.target_uuid, "https://openminds.om-i.org/props/link": {"@id": self.dsv_uuid}}
        )
        mocker.patch.object(
            offline_kg_client._kg_client.instances,
            "get_by_identifiers",
            lambda **kw: mocker.Mock(data={uri: result}),
        )
        data = offline_kg_client.instance_from_full_uri(uri, use_cache=False, require_full_data=False)
        assert data == {
            "@id": self.namespace + self.target_uuid,
            "https://openminds.om-i.org/props/link": {"@id": self.namespace + self.dsv_uuid},
        }
