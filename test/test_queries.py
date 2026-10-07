import os
import json
import pytest
from kg_core.request import Stage, Pagination
from fairgraph.queries import Query, QueryProperty, Filter, PathElement, Regex, Equals
import fairgraph.openminds.core as omcore
import fairgraph.openminds.controlled_terms as omterms
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


def test_generate_query_single_root_level_sort_key(mock_client):
    """Generated queries carry at most one 'sort': true, on a root-level property only.

    The KG query API allows sorting on exactly one property, at the root level. This pins
    that constraint and the deliberate priority order in which the sort property is chosen.
    Most classes use the default priority (SORT_PRIORITY in fairgraph/queries.py), but a few
    classes override it via a per-class SORT_PRIORITY attribute (see the builder's
    SORT_PRIORITY_EXCEPTIONS); ParcellationEntity sorts by lookup_label so that terms from the
    same atlas stay together.
    """
    import fairgraph.openminds.v4.core as v4core
    import fairgraph.openminds.v4.sands as v4sands
    import fairgraph.openminds.v4.ephys as v4ephys
    import fairgraph.openminds.v4.specimen_prep as v4sp
    import fairgraph.openminds.v5.sands as v5sands

    # (class, expected sort propertyName, or None for "no sort")
    cases = [
        # per-class override: lookup_label preferred so atlas terms stay together
        (v4sands.ParcellationEntity, "lookupLabel"),
        (v4sands.ParcellationEntityVersion, "lookupLabel"),
        (v5sands.ParcellationEntity, "lookupLabel"),
        (v5sands.ParcellationEntityVersion, "lookupLabel"),
        # default priority: name wins over lookup_label
        (v4ephys.Electrode, "name"),
        (v4ephys.ElectrodeArray, "name"),
        (v4ephys.Pipette, "name"),
        (v4sp.SlicingDevice, "name"),
        # no 'name', but family_name -> familyName (newly sortable)
        (v4core.Person, "familyName"),
        # no 'name', full_name present -> fullName
        (v4core.Organization, "fullName"),
        (v4core.Dataset, "fullName"),
    ]
    for cls, expected_sort in cases:
        query = cls.generate_query(space="collab-foobar", client=mock_client, with_reverse_properties=True)
        sorts = [prop.get("propertyName") for prop in query["structure"] if prop.get("sort")]
        assert len(sorts) <= 1, f"{cls.__name__}: expected at most one sort key, got {sorts}"
        assert sorts == [expected_sort], f"{cls.__name__}: expected sort key {expected_sort!r}, got {sorts}"
        # sort must not appear on any nested (non-root) property
        for prop in query["structure"]:
            if "structure" in prop:
                assert "sort" not in prop, f"{cls.__name__}: nested sort present"


def test_generate_query_no_sort_when_no_name_like_property(mock_client):
    """Classes with no name-like property should not emit a sort key."""
    # DOI has no name-like top-level property to sort by
    query = omcore.DOI.generate_query(space="collab-foobar", client=mock_client, with_reverse_properties=True)
    for prop in query["structure"]:
        assert "sort" not in prop, f"unexpected sort on {prop.get('propertyName')}"


def test_per_class_sort_priority_override():
    """The generated SORT_PRIORITY class attribute pins the deliberate per-class overrides.

    ParcellationEntity(-Version) prefer lookup_label so that terms from the same atlas stay
    together, unlike every other class which uses the default priority. This guards against
    the builder regeneration silently reverting the override (see SORT_PRIORITY_EXCEPTIONS in
    builder/update_openminds.py).
    """
    import fairgraph.openminds.v4.sands as v4sands
    import fairgraph.openminds.v5.sands as v5sands
    import fairgraph.openminds.v4.ephys as v4ephys
    from fairgraph.queries import SORT_PRIORITY

    default = ("name", "fullName", "shortName", "familyName", "abbreviation", "lookupLabel")
    override = ("lookupLabel", "name", "fullName", "shortName", "familyName", "abbreviation")

    assert v4sands.ParcellationEntity.SORT_PRIORITY == override
    assert v4sands.ParcellationEntityVersion.SORT_PRIORITY == override
    assert v5sands.ParcellationEntity.SORT_PRIORITY == override
    assert v5sands.ParcellationEntityVersion.SORT_PRIORITY == override
    # a class without an override still uses the default
    assert v4ephys.Electrode.SORT_PRIORITY == default
    # and the module default matches
    assert SORT_PRIORITY == default
    assert SORT_PRIORITY


@skip_if_no_connection
def test_list_results_sorted_by_chosen_property(kg_client):
    """Live: results come back sorted case-insensitively by the chosen sort property.

    The KG sorts case-insensitively (e.g. 'AAL1_brain' sits between 'AAL1_AMYG' and
    'AAL1_CAU'), so the assertion compares lower-cased values rather than using plain
    ``sorted()``, which would disagree. Sorting only applies to the query API, so the
    query API is forced explicitly. ParcellationEntity sorts by lookup_label (its per-class
    override).
    """
    import fairgraph.openminds.v4.sands as v4sands

    instances = v4sands.ParcellationEntity.list(kg_client, size=30, api="query")
    values = [inst.lookup_label for inst in instances if getattr(inst, "lookup_label", None)]
    assert len(values) > 1
    lowered = [value.lower() for value in values]
    assert lowered == sorted(lowered), "results not ordered case-insensitively by lookup_label"


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


def test_multi_element_path_with_path_elements():
    query = Query(
        node_type="https://openminds.om-i.org/types/File",
        properties=[
            QueryProperty(
                [
                    "https://openminds.om-i.org/props/fileRepository",
                    PathElement(
                        "https://openminds.om-i.org/props/repository",
                        reverse=True,
                        type_filter="https://openminds.om-i.org/types/DatasetVersion",
                    ),
                ],
                name="dataset",
            )
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
            "type": "https://openminds.om-i.org/types/File",
            "description": "Automatically generated by fairgraph",
        },
        "structure": [
            {"path": "@id", "filter": {"op": "EQUALS", "parameter": "id"}},
            {
                "propertyName": "dataset",
                "path": [
                    "https://openminds.om-i.org/props/fileRepository",
                    {
                        "@id": "https://openminds.om-i.org/props/repository",
                        "reverse": True,
                        "typeFilter": {"@id": "https://openminds.om-i.org/types/DatasetVersion"},
                    },
                ],
            },
        ],
    }
    assert query.serialize() == expected


def test_path_element_conflicts_with_top_level_reverse():
    with pytest.raises(ValueError, match="Cannot use top-level"):
        QueryProperty(
            [
                "https://openminds.om-i.org/props/fileRepository",
                PathElement("https://openminds.om-i.org/props/repository", reverse=True),
            ],
            reverse=True,
        )


@skip_if_no_connection
def test_execute_query_with_multi_element_path_with_path_elements(kg_client):
    # This query should return only Files belonging to the specified dataset.
    # This is possibly a bad choice for a test, since queries involving
    # Files are often very slow, as there are so many Files in the KG.
    DATASET_ID = "bd5f91ff-e829-4b85-92eb-fc56991541f1"
    query = Query(
        node_type="https://openminds.om-i.org/types/File",
        properties=[
            QueryProperty(
                [
                    "https://openminds.om-i.org/props/fileRepository",
                    PathElement(
                        "https://openminds.om-i.org/props/repository",
                        reverse=True,
                        type_filter="https://openminds.om-i.org/types/DatasetVersion",
                    ),
                    "@id",
                ],
                name="dataset",
                expect_single=True,
                filter=Filter("CONTAINS", value=DATASET_ID)
            ),
            QueryProperty("https://openminds.om-i.org/props/name", name="name"),
        ]
    )
    expected = {
        "@context": {
            "@vocab": "https://core.kg.ebrains.eu/vocab/query/",
            "merge": {
                "@id": "merge",
                "@type": "@id",
            },
            "query": "https://schema.hbp.eu/myQuery/",
            "propertyName": {"@id": "propertyName", "@type": "@id"},
            "path": {"@id": "path", "@type": "@id"},
        },
        "meta": {
            "type": "https://openminds.om-i.org/types/File",
            "description": "Automatically generated by fairgraph",
        },
        "structure": [
            {
                "filter": {
                    "op": "EQUALS",
                    "parameter": "id",
                },
                "path": "@id",
            },
            {
                "propertyName": "dataset",
                "singleValue": "FIRST",
                "filter": {"op": "CONTAINS", "value": "bd5f91ff-e829-4b85-92eb-fc56991541f1"},
                "path": [
                    "https://openminds.om-i.org/props/fileRepository",
                    {
                        "@id": "https://openminds.om-i.org/props/repository",
                        "reverse": True,
                        "typeFilter": {"@id": "https://openminds.om-i.org/types/DatasetVersion"},
                    },
                    "@id",
                ],
            },
            {
                "propertyName": "name",
                "path": "https://openminds.om-i.org/props/name"
            },
        ],
    }
    assert query.serialize() == expected
    response = kg_client._kg_client.queries.test_query(
        payload=query.serialize(),
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=5),
    )
    assert len(response.data) == 5
    assert all(item["dataset"] == f"https://kg.ebrains.eu/api/instances/{DATASET_ID}"
               for item in response.data)


def test_generate_query_with_regex_filter(mock_client):
    query = omcore.Person.generate_query(client=mock_client, space=None, filters={"family_name": Regex("^M[uü]ller$")})
    filters = [prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == "Qfamily_name"]
    assert filters == [{"op": "REGEX", "value": "^M[uü]ller$"}]


def test_generate_query_with_plain_string_filter_still_uses_contains(mock_client):
    query = omcore.Person.generate_query(client=mock_client, space=None, filters={"family_name": "Müller"})
    filters = [prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == "Qfamily_name"]
    assert filters == [{"op": "CONTAINS", "value": "Müller"}]


def test_filter_values_containing_a_plus_sign_are_not_modified(mock_client):
    # filter values containing "+" used to be truncated, to work around a KG bug that no longer occurs
    for cls, property_name, value, expected in (
        (omterms.ProgrammingLanguage, "name", "C++", {"op": "CONTAINS", "value": "C++"}),
        (
            omcore.ContactInformation,
            "email",
            "jane.doe+kg@example.org",
            {"op": "CONTAINS", "value": "jane.doe+kg@example.org"},
        ),
        (omterms.Technique, "name", Regex("^CLARITY[-+/]TDE$"), {"op": "REGEX", "value": "^CLARITY[-+/]TDE$"}),
        (
            omcore.Comment,
            "timestamp",
            "2025-01-17T16:22:53.824903+00:00",
            {"op": "EQUALS", "value": "2025-01-17T16:22:53.824903+00:00"},
        ),
        (
            omcore.Comment,
            "timestamp",
            "2026-09-13T14:00:00+02:00",
            {"op": "EQUALS", "value": "2026-09-13T14:00:00+02:00"},
        ),
    ):
        query = cls.generate_query(client=mock_client, space=None, filters={property_name: value})
        filters = [
            prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == f"Q{property_name}"
        ]
        assert filters == [expected]


def test_regex_rejects_a_malformed_pattern():
    # the KG returns no results for a malformed pattern without reporting an error, so a
    # typo would otherwise be indistinguishable from a genuine absence of matches
    for pattern in ("Mus [musculus", "(unbalanced", "a**", "?x"):
        with pytest.raises(ValueError):
            Regex(pattern)


def test_regex_accepts_a_valid_pattern():
    pattern = Regex("^M[uü]ller$")
    assert isinstance(pattern, str)
    assert pattern == "^M[uü]ller$"


def test_equals_marker_filters_with_equals_operator(mock_client):
    query = omcore.Dataset.generate_query(client=mock_client, space=None, filters={"short_name": Equals("FOO")})
    filters = [prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == "Qshort_name"]
    assert filters == [{"op": "EQUALS", "value": "FOO"}]


def test_equals_is_exported_from_the_package():
    import fairgraph

    assert fairgraph.Equals is Equals


@pytest.mark.parametrize(
    "cls, filters, path_expected",
    [
        (omcore.Dataset, {"short_name": Equals("FOO")}, "Qshort_name"),
        (omcore.Dataset, {"digital_identifier__identifier": Equals("https://doi.org/10.1/x")}, "Qidentifier"),
        (omcore.WebResource, {"iri": Equals("https://example.org/a")}, "Qiri"),
    ],
)
def _find_filters(structure, property_name=None):
    """All the filters in a query structure, at any depth, optionally only on the named property"""
    for prop in structure:
        if "filter" in prop and property_name in (None, prop.get("propertyName")):
            yield prop["filter"]
        yield from _find_filters(prop.get("structure", []), property_name)


@pytest.mark.parametrize(
    "cls, filters, property_name",
    [
        (omcore.Dataset, {"short_name": Equals("FOO")}, "Qshort_name"),
        (omcore.Dataset, {"digital_identifier__identifier": Equals("https://doi.org/10.1/x")}, "Qidentifier"),
        (omcore.WebResource, {"iri": Equals("https://example.org/a")}, "Qiri"),
    ],
)
def test_equals_filters_string_and_iri_properties_with_equals(mock_client, cls, filters, property_name):
    query = cls.generate_query(client=mock_client, space=None, filters=filters)
    assert [f["op"] for f in _find_filters(query["structure"], property_name)] == ["EQUALS"]


def test_equals_filters_a_link_by_id_with_equals(mock_client):
    instance_id = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000001"
    query = omcore.DatasetVersion.generate_query(
        client=mock_client, space=None, filters={"is_new_version_of": Equals(instance_id)}
    )
    filters = [f for f in _find_filters(query["structure"]) if f.get("value") == instance_id]
    assert filters == [{"op": "EQUALS", "value": instance_id}]


def test_equals_rejects_a_non_id_string_for_a_link(mock_client):
    # as for a plain string or a Regex
    with pytest.raises(TypeError):
        omcore.DatasetVersion.generate_query(client=mock_client, space=None, filters={"is_new_version_of": Equals("FOO")})


def test_existence_query_filters_strings_with_equals(mock_client):
    dataset = omcore.Dataset(short_name="FOO")
    query = omcore.Dataset.generate_minimal_query(client=mock_client, filters=dataset._build_existence_query())
    filters = [prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == "Qshort_name"]
    assert filters == [{"op": "EQUALS", "value": "FOO"}]


def test_existence_query_filters_strings_with_contains_if_requested(mock_client):
    dataset = omcore.Dataset(short_name="FOO")
    filters = dataset._build_existence_query("contains")
    assert filters == {"short_name": "FOO"}
    assert not isinstance(filters["short_name"], Equals)
    query = omcore.Dataset.generate_minimal_query(client=mock_client, filters=filters)
    query_filters = [prop["filter"] for prop in query["structure"] if prop.get("propertyName", None) == "Qshort_name"]
    assert query_filters == [{"op": "CONTAINS", "value": "FOO"}]


def test_existence_query_rejects_an_invalid_match():
    with pytest.raises(ValueError, match="existence_match"):
        omcore.Dataset(short_name="FOO")._build_existence_query("fuzzy")
