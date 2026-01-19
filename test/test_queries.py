import os
import json
import pytest
from kg_core.request import Stage, Pagination
from fairgraph.queries import Query, QueryProperty, Filter
from fairgraph.utility import adapt_namespaces_for_query
import fairgraph.openminds.core as omcore
from .utils import kg_client, mock_client, skip_if_no_connection


@pytest.fixture()
def example_query_model_version():
    return Query(
        node_type="https://openminds.om-i.org/types/ModelVersion",
        label="fg-testing-modelversion",
        space="model",
        properties=[
            QueryProperty("https://core.kg.ebrains.eu/vocab/meta/space", name="query:space"),
            QueryProperty("@type"),
            QueryProperty(
                "https://openminds.om-i.org/props/fullName",
                name="fullName",
                filter=Filter("CONTAINS", parameter="name"),
                sorted=True,
                required=True,
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/versionIdentifier",
                name="versionIdentifier",
                filter=Filter("EQUALS", parameter="version"),
                required=True,
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/format",
                name="format",
                ensure_order=True,
                properties=[
                    QueryProperty("@id", filter=Filter("EQUALS", parameter="format")),
                    QueryProperty("@type"),
                ],
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/custodian",
                name="custodian",
                ensure_order=True,
                type_filter="https://openminds.om-i.org/types/Person",
                properties=[
                    QueryProperty("@id", filter=Filter("EQUALS", parameter="custodian")),
                    QueryProperty(
                        "https://openminds.om-i.org/props/affiliation",
                        name="affiliation",
                        properties=[
                            QueryProperty("@type"),
                            QueryProperty(
                                "https://openminds.om-i.org/props/memberOf",
                                name="memberOf",
                                properties=[QueryProperty("@id")],
                            ),
                            QueryProperty(
                                "https://openminds.om-i.org/props/startDate",
                                name="startDate",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


@pytest.fixture()
def example_query_model():
    return Query(
        node_type="https://openminds.om-i.org/types/Model",
        label="fg-testing-model",
        space="model",
        properties=[
            QueryProperty("https://core.kg.ebrains.eu/vocab/meta/space", name="query:space"),
            QueryProperty("@type"),
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
                    # QueryProperty("@type"),
                    QueryProperty(
                        "https://openminds.om-i.org/props/familyName",
                        name="familyName",
                    ),
                ],
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/custodian",
                name="organization",
                type_filter="https://openminds.om-i.org/types/Organization",
                properties=[
                    # QueryProperty("@type"),
                    QueryProperty(
                        "https://openminds.om-i.org/props/shortName",
                        name="shortName",
                    ),
                ],
            ),
        ],
    )


@pytest.fixture()
def example_query_repository_with_reverse():
    return Query(
        node_type="https://openminds.om-i.org/types/FileRepository",
        properties=[
            QueryProperty("https://core.kg.ebrains.eu/vocab/meta/space", name="query:space"),
            QueryProperty("https://openminds.om-i.org/props/IRI", name="location"),
            QueryProperty(
                "https://openminds.om-i.org/props/fileRepository",
                reverse=True,
                name="files",
                properties=[
                    QueryProperty("https://openminds.om-i.org/props/name", name="filename"),
                    QueryProperty(
                        [
                            "https://openminds.om-i.org/props/format",
                            "https://openminds.om-i.org/props/name",
                        ],
                        name="format",
                    ),
                    QueryProperty(
                        "https://openminds.om-i.org/props/hash",
                        name="hash",
                        properties=[
                            QueryProperty(
                                "https://openminds.om-i.org/props/digest",
                                name="digest",
                            ),
                            QueryProperty(
                                "https://openminds.om-i.org/props/algorithm",
                                name="algorithm",
                            ),
                        ],
                    ),
                    QueryProperty(
                        "https://openminds.om-i.org/props/storageSize",
                        name="size",
                        expect_single=True,
                        properties=[
                            QueryProperty("https://openminds.om-i.org/props/value", name="value"),
                            QueryProperty(
                                [
                                    "https://openminds.om-i.org/props/unit",
                                    "https://openminds.om-i.org/props/name",
                                ],
                                name="units",
                                expect_single=True,
                            ),
                        ],
                    ),
                ],
            ),
            QueryProperty(
                "https://openminds.om-i.org/props/repository",
                reverse=True,
                required=True,
                name="contains_dataset_version",
                properties=[
                    QueryProperty("@id"),
                    QueryProperty(
                        "https://openminds.om-i.org/props/shortName",
                        name="alias",
                        filter=Filter("EQUALS", parameter="dataset_alias"),
                    ),
                ],
            ),
        ],
    )


def test_query_builder(example_query_model_version):
    generated = example_query_model_version.serialize()
    expected = {
        "@context": {
            "@vocab": "https://core.kg.ebrains.eu/vocab/query/",
            "path": {"@id": "path", "@type": "@id"},
            "merge": {"@id": "merge", "@type": "@id"},
            "propertyName": {"@id": "propertyName", "@type": "@id"},
            "query": "https://schema.hbp.eu/myQuery/",
        },
        "meta": {
            "description": "Automatically generated by fairgraph",
            "name": "fg-testing-modelversion",
            "type": "https://openminds.om-i.org/types/ModelVersion",
        },
        "structure": [
            {
                "filter": {"op": "EQUALS", "parameter": "id"},
                "path": "@id",
            },
            {
                "filter": {"op": "EQUALS", "value": "model"},
                "path": "https://core.kg.ebrains.eu/vocab/meta/space",
                "propertyName": "query:space",
            },
            {"path": "@type"},
            {
                "filter": {"op": "CONTAINS", "parameter": "name"},
                "path": "https://openminds.om-i.org/props/fullName",
                "propertyName": "fullName",
                "required": True,
                "sort": True,
            },
            {
                "filter": {"op": "EQUALS", "parameter": "version"},
                "path": "https://openminds.om-i.org/props/versionIdentifier",
                "propertyName": "versionIdentifier",
                "required": True,
            },
            {
                "ensureOrder": True,
                "path": "https://openminds.om-i.org/props/format",
                "propertyName": "format",
                "structure": [
                    {"filter": {"op": "EQUALS", "parameter": "format"}, "path": "@id"},
                    {"path": "@type"},
                ],
            },
            {
                "ensureOrder": True,
                "path": {
                    "@id": "https://openminds.om-i.org/props/custodian",
                    "typeFilter": {"@id": "https://openminds.om-i.org/types/Person"},
                },
                "propertyName": "custodian",
                "structure": [
                    {
                        "filter": {"op": "EQUALS", "parameter": "custodian"},
                        "path": "@id",
                    },
                    {
                        "path": "https://openminds.om-i.org/props/affiliation",
                        "propertyName": "affiliation",
                        "structure": [
                            {"path": "@type"},
                            {
                                "path": "https://openminds.om-i.org/props/memberOf",
                                "propertyName": "memberOf",
                                "structure": [{"path": "@id"}],
                            },
                            {
                                "path": "https://openminds.om-i.org/props/startDate",
                                "propertyName": "startDate",
                            },
                        ],
                    },
                ],
            },
        ],
    }
    assert generated == expected


def test_query_with_reverse_properties(example_query_repository_with_reverse):
    generated = example_query_repository_with_reverse.serialize()
    expected = {
        "@context": {
            "@vocab": "https://core.kg.ebrains.eu/vocab/query/",
            "query": "https://schema.hbp.eu/myQuery/",
            "merge": {"@id": "merge", "@type": "@id"},
            "propertyName": {"@id": "propertyName", "@type": "@id"},
            "path": {"@id": "path", "@type": "@id"},
        },
        "meta": {
            "type": "https://openminds.om-i.org/types/FileRepository",
            "description": "Automatically generated by fairgraph",
        },
        "structure": [
            {"filter": {"op": "EQUALS", "parameter": "id"}, "path": "@id"},
            {
                "path": "https://core.kg.ebrains.eu/vocab/meta/space",
                "propertyName": "query:space",
            },
            {
                "propertyName": "location",
                "path": "https://openminds.om-i.org/props/IRI",
            },
            {
                "propertyName": "files",
                "path": {
                    "@id": "https://openminds.om-i.org/props/fileRepository",
                    "reverse": True,
                },
                "structure": [
                    {
                        "propertyName": "filename",
                        "path": "https://openminds.om-i.org/props/name",
                    },
                    {
                        "propertyName": "format",
                        "path": [
                            "https://openminds.om-i.org/props/format",
                            "https://openminds.om-i.org/props/name",
                        ],
                    },
                    {
                        "propertyName": "hash",
                        "path": "https://openminds.om-i.org/props/hash",
                        "structure": [
                            {
                                "propertyName": "digest",
                                "path": "https://openminds.om-i.org/props/digest",
                            },
                            {
                                "propertyName": "algorithm",
                                "path": "https://openminds.om-i.org/props/algorithm",
                            },
                        ],
                    },
                    {
                        "propertyName": "size",
                        "path": "https://openminds.om-i.org/props/storageSize",
                        "singleValue": "FIRST",
                        "structure": [
                            {
                                "propertyName": "value",
                                "path": "https://openminds.om-i.org/props/value",
                            },
                            {
                                "propertyName": "units",
                                "singleValue": "FIRST",
                                "path": [
                                    "https://openminds.om-i.org/props/unit",
                                    "https://openminds.om-i.org/props/name",
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "path": {"@id": "https://openminds.om-i.org/props/repository", "reverse": True},
                "propertyName": "contains_dataset_version",
                "required": True,
                "structure": [
                    {"path": "@id"},
                    {
                        "filter": {"op": "EQUALS", "parameter": "dataset_alias"},
                        "path": "https://openminds.om-i.org/props/shortName",
                        "propertyName": "alias",
                    },
                ],
            },
        ],
    }
    assert generated == expected


@skip_if_no_connection
def test_execute_query(kg_client, example_query_model_version):
    query = example_query_model_version.serialize()
    if kg_client.migrated is False:
        query = adapt_namespaces_for_query(query)
    response = kg_client._kg_client.queries.test_query(
        payload=query,
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=3),
    )
    data = response.data
    assert len(data) == 3
    expected_keys = set(
        [
            "@id",
            "@type",
            "https://schema.hbp.eu/myQuery/space",
            "custodian",
            "format",
            "versionIdentifier",
            "fullName",
        ]
    )
    data0 = data[0]
    assert set(data0.keys()) == expected_keys

    if data0["custodian"]:
        custodian0 = data0["custodian"][0]
        assert set(custodian0.keys()) == set(["@id", "affiliation"])
        if custodian0["affiliation"]:
            affil0 = custodian0["affiliation"][0]
            assert set(affil0.keys()) == set(["@type", "memberOf", "startDate"])


@skip_if_no_connection
def test_execute_query_with_id_filter(kg_client, example_query_model):
    target_id = "https://kg.ebrains.eu/api/instances/3ca9ae35-c9df-451f-ac76-4925bd2c7dc6"
    query = example_query_model.serialize()
    if kg_client.migrated is False:
        query = adapt_namespaces_for_query(query)
    response = kg_client._kg_client.queries.test_query(
        payload=query,
        instance_id=kg_client.uuid_from_uri(target_id),
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=10),
    )
    data = response.data
    assert len(data) == 1
    assert data[0]["fullName"] == "AdEx Neuron Models with PyNN"
    assert data[0]["custodian"][0]["familyName"] == "Destexhe"
    # assert data[0]["organization"][0]["shortName"] == "Destexhe Lab"


@skip_if_no_connection
def test_execute_query_with_reverse_properties_and_instance_id(kg_client, example_query_repository_with_reverse):
    target_id = "https://kg.ebrains.eu/api/instances/1c846a5f-eac2-477a-9dc3-d2e51b00fda9"
    query = example_query_repository_with_reverse.serialize()
    if kg_client.migrated is False:
        query = adapt_namespaces_for_query(query)
    response = kg_client._kg_client.queries.test_query(
        payload=query,
        instance_id=kg_client.uuid_from_uri(target_id),
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=10),
    )
    data = response.data
    assert len(data) == 1
    assert (
        data[0]["location"]
        == "https://data-proxy.ebrains.eu/api/v1/buckets/p63ea6-Angelo_SGA1_1.2.4?prefix=hbp-00810/EPSC/"
    )
    assert "hbp-00810_E" in data[0]["files"][0]["filename"]
    assert data[0]["files"][4]["hash"][0]["algorithm"] == "MD5"


@skip_if_no_connection
def test_execute_query_with_reverse_properties_and_filter(kg_client, example_query_repository_with_reverse):
    query = example_query_repository_with_reverse.serialize()
    if kg_client.migrated is False:
        query = adapt_namespaces_for_query(query)
    response = kg_client._kg_client.queries.test_query(
        payload=query,
        additional_request_params={
            "dataset_alias": "Recordings of excitatory postsynaptic currents from cerebellar neurons"
        },
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=10),
    )
    data = response.data
    assert len(data) == 1
    assert (
        data[0]["location"]
        == "https://data-proxy.ebrains.eu/api/v1/buckets/p63ea6-Angelo_SGA1_1.2.4?prefix=hbp-00810/EPSC/"
    )
    assert "hbp-00810_E" in data[0]["files"][0]["filename"]
    assert data[0]["files"][4]["hash"][0]["algorithm"] == "MD5"
    assert (
        data[0]["contains_dataset_version"][0]["alias"]
        == "Recordings of excitatory postsynaptic currents from cerebellar neurons"
    )


def test_openminds_core_queries(mock_client):
    for cls in omcore.list_kg_classes():
        path_expected = os.path.join(
            os.path.dirname(__file__),
            "test_data",
            "queries",
            "openminds",
            "core",
            f"{cls.__name__.lower()}_simple_query.json",
        )
        generated = cls.generate_query(
            space="collab-foobar", client=mock_client, follow_links=None, with_reverse_properties=True
        )
        with open(path_expected) as fp:
            expected = json.load(fp)
            assert generated == expected


def test_generate_query_with_follow_one_link(mock_client):
    for cls in (omcore.Person,):
        path_expected = os.path.join(
            os.path.dirname(__file__),
            "test_data",
            "queries",
            "openminds",
            "core",
            f"{cls.__name__.lower()}_resolved-1_query.json",
        )
        generated = cls.generate_query(
            space=None,
            client=mock_client,
            filters=None,
            follow_links={
                "affiliations": {"member_of": {}},
                "associated_accounts": {},
                "contact_information": {},
                "digital_identifiers": {},
            },
            with_reverse_properties=True,
        )
        with open(path_expected) as fp:
            expected = json.load(fp)
        assert generated == expected


def test_generate_query_with_follow_named_links(mock_client):
    cls = omcore.Person
    path_expected = os.path.join(
        os.path.dirname(__file__),
        "test_data",
        "queries",
        "openminds",
        "core",
        f"{cls.__name__.lower()}_newstyle_query.json",
    )
    generated = cls.generate_query(
        space=None,
        client=mock_client,
        filters={"affiliations__member_of__has_parents__alias": "FZJ"},
        follow_links={"affiliations": {"member_of": {"has_parents": {}}}, "contact_information": {}},
        with_reverse_properties=True,
    )
    with open(path_expected) as fp:
        expected = json.load(fp)
    assert generated == expected


def test_generate_query_type_filter_flattened():
    query = Query(
        node_type="https://openminds.om-i.org/types/LivePaperVersion",
        label="fg-testing-livepaperversion",
        space="livepapers",
        properties=[
            QueryProperty("https://openminds.om-i.org/props/shortName", name="short_name"),
            QueryProperty(
                [
                    "https://openminds.om-i.org/props/relatedPublication",
                    "https://openminds.om-i.org/props/identifier",
                ],
                type_filter="https://openminds.om-i.org/types/DOI",
                name="related_publications",
            ),
        ],
    )
    expected = {
        "@context": {
            "@vocab": "https://core.kg.ebrains.eu/vocab/query/",
            "merge": {"@id": "merge", "@type": "@id"},
            "query": "https://schema.hbp.eu/myQuery/",
            "propertyName": {"@id": "propertyName", "@type": "@id"},
            "path": {"@id": "path", "@type": "@id"},
        },
        "meta": {
            "type": "https://openminds.om-i.org/types/LivePaperVersion",
            "description": "Automatically generated by fairgraph",
            "name": "fg-testing-livepaperversion",
        },
        "structure": [
            {"path": "@id", "filter": {"op": "EQUALS", "parameter": "id"}},
            {"propertyName": "short_name", "path": "https://openminds.om-i.org/props/shortName"},
            {
                "propertyName": "related_publications",
                "path": [
                    {
                        "@id": "https://openminds.om-i.org/props/relatedPublication",
                        "typeFilter": {"@id": "https://openminds.om-i.org/types/DOI"},
                    },
                    "https://openminds.om-i.org/props/identifier",
                ],
            },
            {
                "propertyName": "query:space",
                "path": "https://core.kg.ebrains.eu/vocab/meta/space",
                "filter": {"op": "EQUALS", "value": "livepapers"},
            },
        ],
    }
    assert query.serialize() == expected
