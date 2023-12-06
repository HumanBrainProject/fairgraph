import os
import json
from random import randint
from uuid import UUID
from copy import deepcopy
from datetime import datetime
import shutil
import tempfile
import urllib.request

import pytest

from fairgraph.utility import as_list
from fairgraph.base import IRI
from fairgraph.kgproxy import KGProxy
from fairgraph.kgquery import KGQuery
from fairgraph.kgobject import KGObject
import fairgraph.openminds.core as omcore
import fairgraph.openminds.controlledterms as omterms
from fairgraph.utility import ActivityLog, sha1sum

from test.utils import mock_client, kg_client, skip_if_no_connection


def test_query_generation(mock_client):
    for cls in omcore.list_kg_classes():
        generated = cls.generate_query(space="collab-foobar", client=mock_client)
        filename = f"test/test_data/queries/openminds/core/{cls.__name__.lower()}_simple_query.json"
        with open(filename, "r") as fp:
            expected = json.load(fp)
        assert generated == expected


@skip_if_no_connection
def test_retrieve_released_models_no_filter_api_core(kg_client):
    models = omcore.Model.list(
        kg_client, scope="released", space="model", api="core", size=20, from_index=randint(0, 80)
    )
    assert len(models) == 20
    for m in models:
        assert m.space == "model"


@skip_if_no_connection
def test_retrieve_released_models_no_filter_api_query(kg_client):
    models = omcore.Model.list(
        kg_client, scope="released", space="model", api="query", size=20, from_index=randint(0, 80)
    )
    assert len(models) == 20


@skip_if_no_connection
def test_retrieve_released_models_with_filter_api_core(kg_client):
    with pytest.raises(ValueError):
        models = omcore.Model.list(kg_client, scope="released", api="core", name="foo")


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_obj(kg_client):
    rat = omterms.Species.by_name("Rattus norvegicus", kg_client)
    assert rat.name == "Rattus norvegicus"
    models = omcore.Model.list(kg_client, scope="released", space="model", api="query", study_targets=rat)
    assert len(models) > 0
    for model in models:
        study_targets = [st.resolve(kg_client, scope="released") for st in as_list(model.study_targets)]
        if study_targets:
            assert rat in study_targets


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_uuid(kg_client):
    human = omterms.Species.by_name("Homo sapiens", kg_client)
    models = omcore.Model.list(kg_client, scope="released", space="model", api="query", study_targets=UUID(human.uuid))
    assert len(models) > 0
    for model in models:
        if model.study_targets:
            assert human.id in [st.id for st in as_list(model.study_targets)]


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_id(kg_client):
    mouse = omterms.Species.by_name("Mus musculus", kg_client)
    models = omcore.Model.list(kg_client, scope="released", space="model", api="query", study_targets=IRI(mouse.id))
    # todo: fix so that don't need to wrap the id in an IRI
    assert len(models) > 0
    for model in models:
        if model.study_targets:
            assert mouse.id in [st.id for st in as_list(model.study_targets)]


@skip_if_no_connection
def test_retrieve_released_models_filter_custodian(kg_client):
    alain = omcore.Person.list(kg_client, family_name="Destexhe", given_name="Alain")[0]
    assert alain.given_name == "Alain"
    models = omcore.Model.list(kg_client, scope="released", space="model", api="query", custodians=alain)
    assert len(models) > 0
    for model in models:
        assert alain.id in [c.id for c in as_list(model.custodians)]


@skip_if_no_connection
def test_retrieve_models_filter_by_space(kg_client):
    all_models = omcore.Model.list(kg_client, scope="in progress", space=None, size=10000)
    n_models_in_model_space_core = omcore.Model.count(kg_client, scope="in progress", space="model", api="core")
    n_models_in_model_space_query = omcore.Model.count(kg_client, scope="in progress", space="model", api="query")
    assert n_models_in_model_space_core == n_models_in_model_space_query
    assert len(all_models) > n_models_in_model_space_core
    assert len([m for m in all_models if m.space == "model"]) == n_models_in_model_space_query


@skip_if_no_connection
def test_retrieve_single_model_with_followed_links(kg_client):
    model = omcore.Model.from_uri(
        "https://kg.ebrains.eu/api/instances/708024f7-9dd7-4c92-ae95-936db23c6d99",
        kg_client,
        follow_links={"abstraction_level": {}},
    )
    assert isinstance(model.abstraction_level, omterms.ModelAbstractionLevel)  # followed
    assert isinstance(model.model_scope, KGProxy)  # not followed


@skip_if_no_connection
def test_retrieve_single_model_from_alias(kg_client):
    model = omcore.Model.from_alias("AdEx Models", kg_client)
    assert model.uuid == "3ca9ae35-c9df-451f-ac76-4925bd2c7dc6"


@skip_if_no_connection
def test_retrieve_single_model_from_ambiguous_alias(kg_client):
    model = omcore.Model.from_alias("hippo", kg_client)
    # check that warning is emitted


@skip_if_no_connection
def test_retrieve_unknown_type(kg_client):
    obj = KGObject.from_id("708024f7-9dd7-4c92-ae95-936db23c6d99", kg_client)
    assert isinstance(obj, omcore.Model)


@skip_if_no_connection
def test_resolve_model(kg_client):
    model = omcore.Model.from_id("708024f7-9dd7-4c92-ae95-936db23c6d99", kg_client)
    assert model.name == "Scaffold Model of Cerebellum microcircuit version 2.0"
    assert isinstance(model.versions, KGProxy)
    resolved_model2 = deepcopy(model).resolve(
        kg_client, scope="in progress", follow_links={"versions": {}, "custodians": {"affiliations": {}}}
    )
    assert isinstance(resolved_model2.versions, omcore.ModelVersion)
    assert isinstance(resolved_model2.custodians[0].affiliations[0].member_of, KGProxy)

    resolved_model4 = deepcopy(model).resolve(
        kg_client, scope="in progress", follow_links={"custodians": {"affiliations": {"member_of": {}}}}
    )
    assert isinstance(resolved_model4.custodians[0].affiliations[0].member_of, omcore.Organization)


@skip_if_no_connection
def test_retrieve_released_models_follow_links(kg_client):
    models = omcore.Model.list(
        kg_client,
        scope="released",
        space="model",
        api="query",
        size=5,
        from_index=randint(0, 80),
        follow_links={"versions": {}, "developers": {"affiliation": {"member_of": {}}}, "abstraction_level": {}},
    )
    assert len(models) == 5
    for model in models:
        # check first level links have been resolved
        for version in as_list(model.versions):
            assert isinstance(version, omcore.ModelVersion)
        if model.abstraction_level:
            assert isinstance(model.abstraction_level, omterms.ModelAbstractionLevel)
        for developer in as_list(model.developers):
            assert isinstance(developer, (omcore.Person, omcore.Organization, omcore.Consortium))
        # check second level links have _not_ been resolved
        for version in as_list(model.versions):
            if version.accessibility:
                assert isinstance(version.accessibility, KGProxy)
            if version.repository:
                assert isinstance(version.repository, KGProxy)


@skip_if_no_connection
def test_retrieve_released_model_versions_no_follow(kg_client):
    for api in ("query", "core"):
        versions = omcore.ModelVersion.list(
            kg_client,
            scope="released",
            space="model",
            api=api,
            size=5,
            from_index=randint(0, 80),
        )
        for ver in versions:
            if ver.formats:
                for ct_proxy in as_list(ver.formats):
                    assert isinstance(ct_proxy, KGProxy)
                    assert ct_proxy.classes == [omcore.ContentType]
            if api == "query":
                assert isinstance(ver.is_version_of, KGProxy)
            else:
                assert isinstance(ver.is_version_of, KGQuery)
            assert ver.is_version_of.classes == [omcore.Model]


@skip_if_no_connection
def test_retrieve_released_model_versions_follow_reverse_links(kg_client):
    versions = omcore.ModelVersion.list(
        kg_client,
        scope="released",
        space="model",
        api="query",
        size=5,
        from_index=randint(0, 80),
        follow_links={
            "accessibility": {},
            "formats": {},
            "is_version_of": {
                "abstraction_level": {},
                "versions": {},
                "developers": {"affiliation": {"member_of": {}}},
            },
        },
    )
    for ver in versions:
        # check first level forward links have been resolved
        if ver.accessibility:
            assert isinstance(ver.accessibility, omterms.ProductAccessibility)
        if ver.formats:
            for fmt in as_list(ver.formats):
                assert isinstance(fmt, omcore.ContentType)
        # check first level reverse links have been resolved
        model = ver.is_version_of
        assert isinstance(model, omcore.Model)
        # check forward links from first level reverse links
        assert ver.id in [ver2.id for ver2 in as_list(model.versions)]
        if model.abstraction_level:
            assert isinstance(model.abstraction_level, omterms.ModelAbstractionLevel)
        if model.model_scope:
            assert isinstance(model.model_scope, KGProxy)
        for developer in as_list(model.developers):
            assert isinstance(developer, (omcore.Person, omcore.Organization, omcore.Consortium))


# @skip_if_no_connection
# def test_retrieve_released_people_resolve_two_steps(kg_client):
#     people = omcore.Person.list(
#         kg_client,
#         scope="released",
#         space="common",
#         api="query",
#         size=5,
#         from_index=randint(0, 100),
#         follow_links=2,
#     )
#     assert len(people) == 5


# @skip_if_no_connection
# def test_retrieve_released_models_resolve_two_steps(kg_client):
#     models = omcore.Model.list(kg_client, scope="released", space="model",
#                                api="query", size=10, from_index=randint(0, 80),
#                                follow_links=2)
#     assert len(models) == 10
#     for model in models:
#         # check first level links have been resolved
#         for version in as_list(model.versions):
#             assert isinstance(version, omcore.ModelVersion)
#         if model.abstraction_level:
#             assert isinstance(model.abstraction_level, omterms.ModelAbstractionLevel)
#         for developer in as_list(model.developers):
#             assert isinstance(developer, (omcore.Person, omcore.Organization, omcore.Consortium))
#         # check second level links have been resolved
#         for version in as_list(model.versions):
#             if version.accessibility:
#                 assert isinstance(version.accessibility, omterms.ProductAccessibility)
#             if version.repository:
#                 assert isinstance(version.repository, omcore.FileRepository)
#         # check third level links have _not_ been resolved
#         for version in as_list(model.versions):
#             if version.repository:
#                 assert isinstance(version.repository.type, KGProxy)
#             if version.hosted_by:
#                 assert isinstance(version.repository.hosted_by, KGProxy)


@skip_if_no_connection
def test_query_across_links(kg_client):
    models = omcore.Model.list(
        kg_client,
        scope="in progress",
        space="model",
        api="query",
        follow_links={"developers": {"affiliations": {"member_of": {}}}},
        developers__affiliations__member_of="7bdf4340-c718-45ea-9912-41079799dfd3",
    )
    assert len(models) > 0
    assert len(models) < 100
    for model in models:
        orgs = []
        for dev in as_list(model.developers):
            for affil in as_list(dev.affiliations):
                if affil.member_of:
                    orgs.append(affil.member_of.uuid)
        assert "7bdf4340-c718-45ea-9912-41079799dfd3" in orgs

    # check that "follow_links" is not needed for the cross-link filter to work
    models2 = omcore.Model.list(
        kg_client,
        scope="in progress",
        space="model",
        api="query",
        follow_links=None,
        developers__affiliations__member_of="7bdf4340-c718-45ea-9912-41079799dfd3",
    )
    assert set(model.id for model in models) == set(model.id for model in models2)
    assert isinstance(models[0].developers[0], omcore.Person)
    assert isinstance(models2[0].developers[0], KGProxy)


@skip_if_no_connection
def test_query_across_reverse_links(kg_client):
    versions = omcore.ModelVersion.list(
        kg_client,
        scope="in progress",
        space="model",
        api="query",
        follow_links={"is_version_of": {"developers": {"affiliations": {"member_of": {}}}}},
        is_version_of__developers__affiliations__member_of="7bdf4340-c718-45ea-9912-41079799dfd3",
    )
    assert len(versions) > 0
    assert len(versions) < 100
    for version in versions:
        orgs = []
        model = version.is_version_of
        for dev in as_list(model.developers):
            for affil in as_list(dev.affiliations):
                if affil.member_of:
                    orgs.append(affil.member_of.uuid)
        assert "7bdf4340-c718-45ea-9912-41079799dfd3" in orgs


@skip_if_no_connection
def test_count_released_models(kg_client):
    models = omcore.Model.list(kg_client, scope="released", space="model", api="core", size=1000)
    n_models = omcore.Model.count(kg_client, scope="released", space="model", api="core")
    assert len(models) == n_models
    assert n_models > 100


@skip_if_no_connection
def test_count_models_with_filters(kg_client):
    # rat = omterms.Species.by_name("Rattus norvegicus", kg_client)
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)

    models = omcore.Model.list(
        kg_client,
        scope="released",
        space="model",
        api="auto",
        study_targets=ca1,
        model_scope=single_cell,
    )
    n_models = omcore.Model.count(
        kg_client,
        scope="released",
        space="model",
        api="auto",
        study_targets=ca1,
        model_scope=single_cell,
    )
    assert len(models) == n_models
    assert n_models > 1


@skip_if_no_connection
def test_exists_method_with_known_id(kg_client):
    model = omcore.Model.from_id("708024f7-9dd7-4c92-ae95-936db23c6d99", kg_client)
    assert model.existence_query_fields == ("name",)

    new_model = omcore.Model(id=model.id)
    assert new_model != model
    assert new_model.exists(kg_client)
    assert new_model == model


@skip_if_no_connection
def test_exists_method_without_id(kg_client):
    model = omcore.Model.from_id("708024f7-9dd7-4c92-ae95-936db23c6d99", kg_client)
    assert model.existence_query_fields == ("name",)

    new_model = omcore.Model(name=model.name)
    assert new_model != model
    assert new_model.exists(kg_client)
    assert new_model == model


def test__update():
    example_data = {
        "@id": "https://kg.ebrains.eu/api/instances/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
        "@type": ["https://openminds.ebrains.eu/core/Person"],
        "http://schema.org/identifier": [
            "ba78ffe138e3a79a7514f26441fba6ff",
            "https://nexus.humanbrainproject.org/v0/data/uniminds/core/person/v1.0.0/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
            "https://kg.ebrains.eu/api/instances/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
        ],
        "https://core.kg.ebrains.eu/vocab/meta/revision": "_fCLxIMC---",
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.ebrains.eu/vocab/affiliation": {
            "@type": ["https://openminds.ebrains.eu/core/Affiliation"],
            "https://openminds.ebrains.eu/vocab/memberOf": {
                "@id": "https://kg.ebrains.eu/api/instances/05c23d56-b27e-4cf2-8c47-ed12c1a441e7"
            },
        },
        "https://openminds.ebrains.eu/vocab/contactInformation": [
            {"@id": "https://kg.ebrains.eu/api/instances/4b88cd1e-e222-47e9-9b4a-32b648bddbca"},
            {"@id": "https://kg.ebrains.eu/api/instances/bc036c71-084b-4ffa-8430-4543095660f2"},
        ],
        "https://openminds.ebrains.eu/vocab/familyName": "Bianchi",
        "https://openminds.ebrains.eu/vocab/givenName": "Daniela",
    }
    client = None
    person = omcore.Person.from_kg_instance(example_data, client=client, scope="in progress")
    for key in (
        "http://schema.org/identifier",
        "https://core.kg.ebrains.eu/vocab/meta/revision",
        "https://core.kg.ebrains.eu/vocab/meta/space",
    ):
        example_data.pop(key)
    assert person.remote_data == example_data
    # this follows the sequence in person.save()
    updated_data = person.modified_data()
    assert len(updated_data) == 0


@skip_if_no_connection
def test_KGQuery_resolve(kg_client):
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)
    filters = {"study_targets": ca1, "model_scope": single_cell}
    q = KGQuery(omcore.Model, filters)
    models_q = q.resolve(kg_client, scope="released")
    models_direct = omcore.Model.list(kg_client, scope="released", space="model", api="query", **filters)
    assert models_q == models_direct


@skip_if_no_connection
def test_KGQuery_count(kg_client):
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)
    filters = {"study_targets": ca1, "model_scope": single_cell}
    q = KGQuery(omcore.Model, filters)
    n_models_q = q.count(kg_client, space="model", scope="released")
    n_models_direct = omcore.Model.count(kg_client, scope="released", space="model", api="query", **filters)
    assert n_models_q == n_models_direct
    assert n_models_q > 1


def test_to_jsonld():
    person1 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
    )
    expected1 = {
        "@id": "0000",
        "@type": ["https://openminds.ebrains.eu/core/Person"],
        "https://openminds.ebrains.eu/vocab/affiliation": {
            "@type": ["https://openminds.ebrains.eu/core/Affiliation"],
            "https://openminds.ebrains.eu/vocab/memberOf": {
                "@type": ["https://openminds.ebrains.eu/core/Organization"],
                "https://openminds.ebrains.eu/vocab/fullName": "The Lonely Mountain",
            },
        },
        "https://openminds.ebrains.eu/vocab/familyName": "Oakenshield",
        "https://openminds.ebrains.eu/vocab/givenName": "Thorin",
    }
    assert person1.to_jsonld(follow_links=True) == expected1
    assert person1.to_jsonld(follow_links=False) == expected1

    person2 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(id="1111", name="The Lonely Mountain")),
    )
    expected2a = {
        "@id": "0000",
        "@type": ["https://openminds.ebrains.eu/core/Person"],
        "https://openminds.ebrains.eu/vocab/affiliation": {
            "@type": ["https://openminds.ebrains.eu/core/Affiliation"],
            "https://openminds.ebrains.eu/vocab/memberOf": {
                "@id": "1111",
                "@type": ["https://openminds.ebrains.eu/core/Organization"],
                "https://openminds.ebrains.eu/vocab/fullName": "The Lonely Mountain",
            },
        },
        "https://openminds.ebrains.eu/vocab/familyName": "Oakenshield",
        "https://openminds.ebrains.eu/vocab/givenName": "Thorin",
    }
    expected2b = {
        "@id": "0000",
        "@type": ["https://openminds.ebrains.eu/core/Person"],
        "https://openminds.ebrains.eu/vocab/affiliation": {
            "@type": ["https://openminds.ebrains.eu/core/Affiliation"],
            "https://openminds.ebrains.eu/vocab/memberOf": {"@id": "1111"},
        },
        "https://openminds.ebrains.eu/vocab/familyName": "Oakenshield",
        "https://openminds.ebrains.eu/vocab/givenName": "Thorin",
    }
    assert person2.to_jsonld(follow_links=True) == expected2a
    assert person2.to_jsonld(follow_links=False) == expected2b


def test_save_new_mock(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        name=f"Dummy new model created for testing at {timestamp}",
        alias=f"DummyModel-{timestamp.isoformat()}",
        abstraction_level=omterms.ModelAbstractionLevel.by_name("protein structure", mock_client),
        custodians=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        description="This model should never actually appear in the KG. If it does, please remove it.",
        developers=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        digital_identifier=None,
        versions=None,
        homepage=IRI("http://example.com"),
        how_to_cite=None,
        model_scope=omterms.ModelScope.by_name("subcellular", mock_client),
        study_targets=[
            omterms.Species.by_name("Mus musculus", mock_client),
            omterms.CellType.by_name("astrocyte", mock_client),
            omterms.UBERONParcellation.by_name("amygdala", mock_client),
        ],
    )
    log = ActivityLog()
    new_model.save(mock_client, space="myspace", recursive=False, activity_log=log)
    assert len(log.entries) == 1
    assert log.entries[0].cls == "Model"
    assert log.entries[0].space == "myspace"
    assert log.entries[0].type == "create"


def test_save_existing_mock(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="0000",
        name=f"Dummy new model created for testing at {timestamp}",
        alias=f"DummyModel-{timestamp.isoformat()}",
        abstraction_level=omterms.ModelAbstractionLevel.by_name("protein structure", mock_client),
        custodians=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        description="This model should never actually appear in the KG. If it does, please remove it.",
        developers=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        digital_identifier=None,
        versions=None,
        homepage=IRI("http://example.com"),
        how_to_cite=None,
        model_scope=omterms.ModelScope.by_name("subcellular", mock_client),
        study_targets=[
            omterms.Species.by_name("Mus musculus", mock_client),
            omterms.CellType.by_name("astrocyte", mock_client),
            omterms.UBERONParcellation.by_name("amygdala", mock_client),
        ],
    )
    new_model._space = "model"
    log = ActivityLog()
    new_model.save(mock_client, recursive=False, activity_log=log)
    assert len(log.entries) == 1
    assert log.entries[0].cls == "Model"
    assert log.entries[0].space == "model"
    assert log.entries[0].type == "update"


def test_save_existing_mock_no_updates_allowed(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="0000",
        name=f"Dummy new model created for testing at {timestamp}",
        alias=f"DummyModel-{timestamp.isoformat()}",
        abstraction_level=omterms.ModelAbstractionLevel.by_name("protein structure", mock_client),
        custodians=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        description="This model should never actually appear in the KG. If it does, please remove it.",
        developers=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        digital_identifier=None,
        versions=None,
        homepage=IRI("http://example.com"),
        how_to_cite=None,
        model_scope=omterms.ModelScope.by_name("subcellular", mock_client),
        study_targets=[
            omterms.Species.by_name("Mus musculus", mock_client),
            omterms.CellType.by_name("astrocyte", mock_client),
            omterms.UBERONParcellation.by_name("amygdala", mock_client),
        ],
    )
    new_model._space = "model"

    new_model.allow_update = False

    log = ActivityLog()
    new_model.save(mock_client, recursive=False, activity_log=log)
    assert len(log.entries) == 1
    assert log.entries[0].type == "no-op"


def test_save_replace_existing_mock(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="0000",
        name=f"Dummy new model created for testing at {timestamp}",
        alias=f"DummyModel-{timestamp.isoformat()}",
        abstraction_level=omterms.ModelAbstractionLevel.by_name("protein structure", mock_client),
        custodians=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        description="This model should never actually appear in the KG. If it does, please remove it.",
        developers=omcore.Person(given_name="Bilbo", family_name="Baggins", id="fake_uuid", space="common"),
        digital_identifier=None,
        versions=None,
        homepage=IRI("http://example.com"),
        how_to_cite=None,
        model_scope=omterms.ModelScope.by_name("subcellular", mock_client),
        study_targets=[
            omterms.Species.by_name("Mus musculus", mock_client),
            omterms.CellType.by_name("astrocyte", mock_client),
            omterms.UBERONParcellation.by_name("amygdala", mock_client),
        ],
    )
    new_model._space = "model"
    log = ActivityLog()
    new_model.save(mock_client, recursive=False, replace=True, activity_log=log)
    assert len(log.entries) == 1
    assert log.entries[0].cls == "Model"
    assert log.entries[0].space == "model"
    assert log.entries[0].type == "replacement"


def test_save_new_recursive_mock(mock_client):
    new_person = omcore.Person(
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
    )
    log = ActivityLog()
    new_person.save(mock_client, space="myspace", recursive=True, activity_log=log)
    assert len(log.entries) == 2
    assert log.entries[0].cls == "Organization"
    assert log.entries[0].space == "myspace"
    assert log.entries[0].type == "create"
    assert log.entries[1].cls == "Person"
    assert log.entries[1].space == "myspace"
    assert log.entries[1].type == "create"
    assert UUID(new_person.uuid)
    assert UUID(new_person.affiliations.member_of.uuid)


# def test_save_existing_with_id_mock(mock_client):
#    existing_model = mock_client.instances[]


def test_normalize_filter():
    result = omcore.Model.normalize_filter(
        {
            "developers": {"affiliations": {"member_of": omcore.Organization(id="some_id")}},
            "digital_identifier": {"identifier": "https://doi.org/some-doi"},
        }
    )
    expected = {
        "developers": {"affiliations": {"member_of": "some_id"}},
        "digital_identifier": {"identifier": "https://doi.org/some-doi"},
    }
    assert result == expected


def test_class_docstring():
    assert "email address" in omcore.Person.__doc__


def test_field_names():
    assert omcore.Person.field_names == [
        "affiliations",
        "alternate_names",
        "associated_accounts",
        "contact_information",
        "digital_identifiers",
        "family_name",
        "given_name",
        "activities",
        "comments",
        "coordinated_projects",
        "developed",
        "funded",
        "is_custodian_of",
        "is_owner_of",
        "is_provider_of",
        "manufactured",
        "published",
        "started",
    ]
    assert omcore.Person.required_field_names == ["given_name"]


def test_diff():
    person1 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
    )
    person2 = omcore.Person(
        given_name="Thorin son of Thráin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="Erebor")),
    )
    expected = {
        "id": ("0000", None),
        "fields": {
            "given_name": ("Thorin", "Thorin son of Thráin"),
            "affiliations": (
                omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
                omcore.Affiliation(member_of=omcore.Organization(name="Erebor")),
            ),
        },
    }
    assert person1.diff(person2) == expected

    assert person1.affiliations.member_of.diff(person2) == {"type": (omcore.Organization, omcore.Person)}


def test_show():
    # todo: capture stdout
    person1 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
    )
    person1.show()
    person1.show(max_width=120)


def test_file_download():
    file_obj = omcore.File(
        name="installation.rst",
        iri=IRI("https://raw.githubusercontent.com/HumanBrainProject/fairgraph/master/doc/installation.rst"),
        hashes=omcore.Hash(algorithm="SHA1", digest="7c97abf3c007bfa58d58e09c0e497ceffd93bd11"),
    )
    local_dir = tempfile.mkdtemp()

    # test download to a directory
    local_filename = file_obj.download(local_dir, client=None, accept_terms_of_use=True)
    assert str(local_filename) == os.path.join(local_dir, file_obj.name)
    assert sha1sum(local_filename) == file_obj.hashes.digest

    # test download to a specific filename
    local_filename_expected = os.path.join(local_dir, "installation1.rst")
    local_filename = file_obj.download(local_filename_expected, client=None, accept_terms_of_use=True)
    assert str(local_filename) == local_filename_expected
    assert sha1sum(local_filename) == file_obj.hashes.digest

    shutil.rmtree(local_dir)


def test_file_from_local_file():
    file_obj = omcore.File.from_local_file("test/utils.py")
    assert file_obj.name == "test/utils.py"
    assert file_obj.storage_size.value == float(os.stat("test/utils.py").st_size)
    assert file_obj.format.name == "text/x-python"
    assert file_obj.hashes.digest == sha1sum("test/utils.py")


@skip_if_no_connection
def test_dataset_version_download(mocker):
    mock_urlretrieve = mocker.patch(
        "fairgraph.openminds.core.products.dataset_version.urlretrieve",
        lambda url, local_filename: (local_filename, None),
    )
    fake_dsv = omcore.DatasetVersion(
        repository=omcore.FileRepository(iri=IRI("https://data-proxy.ebrains.eu/api/v1/public/foo/bar"))
    )
    local_dir = tempfile.mkdtemp()
    local_filename, repository_url = fake_dsv.download(local_dir, client=None, accept_terms_of_use=True)
    os.rmdir(local_dir)
    assert repository_url == "https://data-proxy.ebrains.eu/api/v1/public/foo/bar"
    assert str(local_filename) == os.path.join(local_dir, "bar.zip")


@skip_if_no_connection
def test_person_me(kg_client):
    person = omcore.Person.me(kg_client, allow_multiple=False)
    # the following assumes that anyone running these tests is represented in the KG
    assert isinstance(person, omcore.Person)


# def test_children():
