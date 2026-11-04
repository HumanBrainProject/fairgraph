import os
import json
from random import randint
from uuid import UUID
from copy import deepcopy
from datetime import datetime
import shutil
import tempfile
import urllib.request
import warnings

from http.client import RemoteDisconnected

import pytest
from requests.exceptions import ConnectionError

from openminds import IRI
from openminds.base import LinkedNodeEmbedding

from fairgraph.utility import as_list
from fairgraph.collection import Collection
from fairgraph.kgproxy import KGProxy
from fairgraph.kgquery import KGQuery
from fairgraph.kgobject import KGObject, EXISTENCE_QUERY_SIZE
import fairgraph.openminds.core as omcore
import fairgraph.openminds.controlled_terms as omterms
from fairgraph.utility import ActivityLog, sha1sum, normalize_data

from test.utils import (
    MockKGResponse,
    mock_client,
    kg_client,
    skip_if_no_connection,
    skip_if_using_production_server,
)


def test_query_generation(mock_client):
    for cls in omcore.list_kg_classes():
        generated = cls.generate_query(space="collab-foobar", client=mock_client, with_reverse_properties=True)
        filename = f"test/test_data/queries/openminds/core/{cls.__name__.lower()}_simple_query.json"
        with open(filename, "r") as fp:
            expected = json.load(fp)
        assert generated == expected


@skip_if_no_connection
def test_retrieve_released_models_no_filter_api_core(kg_client):
    models = omcore.Model.list(
        kg_client, release_status="released", space="model", api="core", size=20, from_index=randint(0, 80)
    )
    assert len(models) == 20
    for m in models:
        assert m.space == "model"


@skip_if_no_connection
def test_retrieve_released_models_no_filter_api_query(kg_client):
    models = omcore.Model.list(
        kg_client, release_status="released", space="model", api="query", size=20, from_index=randint(0, 80)
    )
    assert len(models) == 20


@skip_if_no_connection
def test_retrieve_released_models_with_filter_api_core(kg_client):
    with pytest.raises(ValueError):
        models = omcore.Model.list(kg_client, release_status="released", api="core", name="foo")


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_obj(kg_client):
    rat = omterms.Species.by_name("Rattus norvegicus", kg_client)
    assert rat.name == "Rattus norvegicus"
    models = omcore.Model.list(kg_client, release_status="released", space="model", api="query", study_targets=rat)
    assert len(models) > 0
    for model in models:
        study_targets = [st.resolve(kg_client, release_status="released") for st in as_list(model.study_targets)]
        if study_targets:
            assert rat in study_targets


@skip_if_no_connection
def test_retrieve_released_datasets_filter_species_by_openminds_obj(kg_client):
    rat = omterms.Species.by_name("Rattus norvegicus", kg_client)
    rat_om = omterms.Species.rattus_norvegicus
    assert rat.name == rat_om.name == "Rattus norvegicus"
    follow_links = {"study_targets": {}}
    datasets = omcore.DatasetVersion.list(kg_client, space="dataset", study_targets=rat, follow_links=follow_links)
    datasets_om = omcore.DatasetVersion.list(
        kg_client, space="dataset", study_targets=rat_om, follow_links=follow_links
    )
    assert len(datasets) > 0
    assert len(datasets) == len(datasets_om)
    assert [ds.id for ds in datasets] == [ds.id for ds in datasets_om]
    for dataset in datasets_om:
        assert rat in dataset.study_targets


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_uuid(kg_client):
    human = omterms.Species.by_name("Homo sapiens", kg_client)
    models = omcore.Model.list(
        kg_client, release_status="released", space="model", api="query", study_targets=UUID(human.uuid)
    )
    assert len(models) > 0
    for model in models:
        if model.study_targets:
            assert human.id in [st.id for st in as_list(model.study_targets)]


@skip_if_no_connection
def test_retrieve_released_models_filter_species_by_id(kg_client):
    mouse = omterms.Species.by_name("Mus musculus", kg_client)
    models = omcore.Model.list(
        kg_client, release_status="released", space="model", api="query", study_targets=mouse.id
    )
    assert len(models) > 0
    for model in models:
        if model.study_targets:
            assert mouse.id in [st.id for st in as_list(model.study_targets)]


@skip_if_no_connection
def test_retrieve_released_models_filter_custodian(kg_client):
    alain = omcore.Person.list(kg_client, family_name="Destexhe", given_name="Alain")[0]
    assert alain.given_name == "Alain"
    models = omcore.Model.list(kg_client, release_status="released", space="model", api="query", custodians=alain)
    assert len(models) > 0
    for model in models:
        assert alain.id in [c.id for c in as_list(model.custodians)]


@skip_if_no_connection
def test_retrieve_models_filter_by_space(kg_client):
    all_models = omcore.Model.list(kg_client, release_status="in progress", space=None, size=10000)
    n_models_in_model_space_core = omcore.Model.count(
        kg_client, release_status="in progress", space="model", api="core"
    )
    n_models_in_model_space_query = omcore.Model.count(
        kg_client, release_status="in progress", space="model", api="query"
    )
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
    assert isinstance(model.scope, KGProxy)  # not followed


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
        kg_client, release_status="released", follow_links={"versions": {}, "custodians": {"affiliations": {}}}
    )
    assert isinstance(resolved_model2.versions, omcore.ModelVersion)
    assert isinstance(resolved_model2.custodians[0].affiliations[0].member_of, KGProxy)

    resolved_model4 = deepcopy(model).resolve(
        kg_client, release_status="released", follow_links={"custodians": {"affiliations": {"member_of": {}}}}
    )
    assert isinstance(resolved_model4.custodians[0].affiliations[0].member_of, omcore.Organization)


@skip_if_no_connection
def test_retrieve_released_models_follow_links(kg_client):
    models = omcore.Model.list(
        kg_client,
        release_status="released",
        space="model",
        api="query",
        size=5,
        from_index=randint(0, 80),
        follow_links={"versions": {}, "developers": {"affiliations": {"member_of": {}}}, "abstraction_level": {}},
        with_reverse_properties=True,
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
            release_status="released",
            space="model",
            api=api,
            size=5,
            from_index=randint(0, 80),
            with_reverse_properties=True,
        )
        for ver in versions:
            if ver.formats:
                for ct_proxy in as_list(ver.formats):
                    assert isinstance(ct_proxy, KGProxy)
                    assert ct_proxy.classes == [omcore.ContentType]
            if api == "query":
                assert isinstance(ver.is_version_of[0], KGProxy)
                assert ver.is_version_of[0].classes == [omcore.Model]
            else:
                assert isinstance(ver.is_version_of, KGQuery)
                assert ver.is_version_of.classes == [omcore.Model]


@skip_if_no_connection
def test_retrieve_released_model_versions_follow_reverse_links(kg_client):
    versions = omcore.ModelVersion.list(
        kg_client,
        release_status="released",
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
        with_reverse_properties=True,
    )
    for ver in versions:
        # check first level forward links have been resolved
        if ver.accessibility:
            assert isinstance(ver.accessibility, omterms.ProductAccessibility)
        if ver.formats:
            for fmt in as_list(ver.formats):
                assert isinstance(fmt, omcore.ContentType)
        # check first level reverse links have been resolved
        model = ver.is_version_of[0]
        assert isinstance(model, omcore.Model)
        # check forward links from first level reverse links
        assert ver.id in [ver2.id for ver2 in as_list(model.versions)]
        if model.abstraction_level:
            assert isinstance(model.abstraction_level, omterms.ModelAbstractionLevel)
        if model.scope:
            assert isinstance(model.scope, KGProxy)
        for developer in as_list(model.developers):
            assert isinstance(developer, (omcore.Person, omcore.Organization, omcore.Consortium))


# @skip_if_no_connection
# def test_retrieve_released_people_resolve_two_steps(kg_client):
#     people = omcore.Person.list(
#         kg_client,
#         release_status="released",
#         space="common",
#         api="query",
#         size=5,
#         from_index=randint(0, 100),
#         follow_links=2,
#     )
#     assert len(people) == 5


# @skip_if_no_connection
# def test_retrieve_released_models_resolve_two_steps(kg_client):
#     models = omcore.Model.list(kg_client, release_status="released", space="model",
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
        release_status="released",
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
        release_status="released",
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
        release_status="released",
        space="model",
        api="query",
        follow_links={"is_version_of": {"developers": {"affiliations": {"member_of": {}}}}},
        is_version_of__developers__affiliations__member_of="7bdf4340-c718-45ea-9912-41079799dfd3",
    )
    assert len(versions) > 0
    assert len(versions) < 100
    for version in versions:
        orgs = []
        model = version.is_version_of[0]
        for dev in as_list(model.developers):
            for affil in as_list(dev.affiliations):
                if affil.member_of:
                    orgs.append(affil.member_of.uuid)
        assert "7bdf4340-c718-45ea-9912-41079799dfd3" in orgs


@skip_if_no_connection
def test_resolve_reverse_link(kg_client):
    repo = omcore.FileRepository.from_id("c569b826-9d2e-4ba0-9363-561906c67cd6", kg_client)
    files = repo.files.resolve(kg_client)
    assert len(files) == 37


@skip_if_no_connection
def test_count_released_models(kg_client):
    models = omcore.Model.list(kg_client, release_status="released", space="model", api="core", size=1000)
    n_models = omcore.Model.count(kg_client, release_status="released", space="model", api="core")
    assert len(models) == n_models
    assert n_models > 100


@skip_if_no_connection
def test_count_models_with_filters(kg_client):
    # rat = omterms.Species.by_name("Rattus norvegicus", kg_client)
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)

    models = omcore.Model.list(
        kg_client,
        release_status="released",
        space="model",
        api="auto",
        study_targets=ca1,
        model_scope=single_cell,  # note that 'model_scope' is an alias for 'scope'
    )
    n_models = omcore.Model.count(
        kg_client,
        release_status="released",
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
    assert model.existence_query_properties == ("full_name",)

    new_model = omcore.Model(id=model.id)
    assert new_model != model
    assert new_model.exists(kg_client)
    assert new_model == model


@skip_if_no_connection
def test_exists_method_without_id(kg_client):
    model = omcore.Model.from_id("708024f7-9dd7-4c92-ae95-936db23c6d99", kg_client)
    assert model.existence_query_properties == ("full_name",)

    new_model = omcore.Model(name=model.name)
    assert new_model != model
    assert new_model.exists(kg_client)
    assert new_model == model


def test_modified_data_method_with_local_changes():
    dsv = omcore.DatasetVersion(
        id="https://kg.ebrains.eu/api/instances/12345678-90ab-cdef-0123-4567890abcde", full_name="test1234"
    )
    dsv.remote_data = normalize_data(
        dsv.to_jsonld(include_empty_properties=True, embed_linked_nodes=LinkedNodeEmbedding.NEVER), dsv.context
    )
    assert dsv.modified_data() == {}
    dsv.repository = omcore.FileRepository(iri="http://example.org")
    assert dsv.modified_data() == {
        "https://openminds.om-i.org/props/repository": {
            "@type": "https://openminds.om-i.org/types/FileRepository",
            "https://openminds.om-i.org/props/IRI": "http://example.org",
            "https://openminds.om-i.org/props/contentTypePattern": None,
            "https://openminds.om-i.org/props/format": None,
            "https://openminds.om-i.org/props/hash": None,
            "https://openminds.om-i.org/props/hostedBy": None,
            "https://openminds.om-i.org/props/name": None,
            "https://openminds.om-i.org/props/storageSize": None,
            "https://openminds.om-i.org/props/structurePattern": None,
            "https://openminds.om-i.org/props/type": None,
        }
    }
    dsv.repository = omcore.FileRepository(
        id="https://kg.ebrains.eu/api/instances/23456789-0abc-def0-1234-567890abcdef", iri="http://example.org"
    )
    assert dsv.modified_data() == {"https://openminds.om-i.org/props/repository": {"@id": dsv.repository.id}}


def test__update():
    example_data = {
        "@id": "https://kg.ebrains.eu/api/instances/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
        "@type": "https://openminds.om-i.org/types/Person",
        "http://schema.org/identifier": [
            "ba78ffe138e3a79a7514f26441fba6ff",
            "https://nexus.humanbrainproject.org/v0/data/uniminds/core/person/v1.0.0/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
            "https://kg.ebrains.eu/api/instances/e90fc25a-fc35-4066-9ff2-ca3583a2d008",
        ],
        "https://core.kg.ebrains.eu/vocab/meta/revision": "_fCLxIMC---",
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/affiliation": [
            {
                "@type": "https://openminds.om-i.org/types/Affiliation",
                "https://openminds.om-i.org/props/memberOf": {
                    "@id": "https://kg.ebrains.eu/api/instances/05c23d56-b27e-4cf2-8c47-ed12c1a441e7"
                },
            }
        ],
        "https://openminds.om-i.org/props/contactInformation": [
            {"@id": "https://kg.ebrains.eu/api/instances/4b88cd1e-e222-47e9-9b4a-32b648bddbca"},
            {"@id": "https://kg.ebrains.eu/api/instances/bc036c71-084b-4ffa-8430-4543095660f2"},
        ],
        "https://openminds.om-i.org/props/familyName": "Bianchi",
        "https://openminds.om-i.org/props/givenName": "Daniela",
    }
    person = omcore.Person.from_jsonld(example_data, ignore_unexpected_keys=True, release_status="in progress")
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


LONELY_MOUNTAIN_ID = "https://kg.ebrains.eu/api/instances/45678901-bcde-f012-3456-7890abcdef01"


def _seed_lonely_mountain(mock_client):
    mock_client.instances[LONELY_MOUNTAIN_ID] = {
        "@id": LONELY_MOUNTAIN_ID,
        "@type": ["https://openminds.om-i.org/types/Organization"],
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/fullName": "Kingdom under the Lonely Mountain",
    }


@pytest.mark.parametrize(
    "full_name,existence_match",
    [
        ("kingdom under the lonely mountain", "equals"),  # differs only in case
        ("Lonely Mountain", "contains"),
        ("lonely mountain", "contains"),
    ],
)
def test_inexact_existence_match_adopts_the_stored_value(mock_client, full_name, existence_match):
    # see issue #170
    _seed_lonely_mountain(mock_client)
    org = omcore.Organization(full_name=full_name)
    log = ActivityLog()
    org.save(mock_client, space="common", existence_match=existence_match, activity_log=log)
    assert org.id == LONELY_MOUNTAIN_ID
    assert org.full_name == "Kingdom under the Lonely Mountain"
    assert org.modified_data() == {}
    assert [entry.type for entry in log.entries] == ["no-op"]
    assert mock_client.updates == []

    # a second object with the same search term is found in the existence cache, with the same result
    org2 = omcore.Organization(full_name=full_name)
    assert org2.exists(mock_client, existence_match=existence_match)
    assert org2.id == LONELY_MOUNTAIN_ID
    assert org2.full_name == "Kingdom under the Lonely Mountain"
    assert org2.modified_data() == {}


def _person_document(extra_key=None, extra_key_in_link=None):
    """A JSON-LD document for a Person, linking to an ORCID that is included in full."""
    orcid = {
        "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002",
        "@type": "https://openminds.om-i.org/types/ORCID",
        "https://openminds.om-i.org/props/identifier": "https://orcid.org/0000-0002-1825-0097",
    }
    person = {
        "@context": {"@vocab": "https://openminds.om-i.org/props/"},
        "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000001",
        "@type": "https://openminds.om-i.org/types/Person",
        "givenName": "Ada",
        "https://openminds.om-i.org/props/familyName": "Lovelace",
        "https://openminds.om-i.org/props/digitalIdentifier": [orcid],
    }
    if extra_key:
        person[extra_key] = "x"
    if extra_key_in_link:
        orcid[extra_key_in_link] = "x"
    return person


def test_from_jsonld_accepts_properties_compact_or_expanded():
    person = omcore.Person.from_jsonld(_person_document())
    assert person.given_name == "Ada"
    assert person.family_name == "Lovelace"
    assert person.digital_identifiers[0].identifier == "https://orcid.org/0000-0002-1825-0097"


@pytest.mark.parametrize("extra_key", ["https://openminds.om-i.org/props/givenname", "nickname", "foo:bar"])
def test_from_jsonld_rejects_unexpected_keys_by_default(extra_key):
    with pytest.raises(NameError, match="Unexpected arguments"):
        omcore.Person.from_jsonld(_person_document(extra_key=extra_key))


def test_from_jsonld_rejects_unexpected_keys_in_linked_nodes_by_default():
    with pytest.raises(NameError, match="ORCID"):
        omcore.Person.from_jsonld(_person_document(extra_key_in_link="https://openminds.om-i.org/props/typo"))


def test_from_jsonld_ignore_unexpected_keys_applies_to_the_whole_document():
    space_key = "https://core.kg.ebrains.eu/vocab/meta/space"
    data = _person_document(extra_key=space_key, extra_key_in_link=space_key)
    person = omcore.Person.from_jsonld(data, ignore_unexpected_keys=True)
    assert person.given_name == "Ada"
    assert person.digital_identifiers[0].identifier == "https://orcid.org/0000-0002-1825-0097"
    # the choice does not outlast the call
    with pytest.raises(NameError):
        omcore.Person.from_jsonld(data)


def test_load_passes_ignore_unexpected_keys(tmp_path):
    path = tmp_path / "person.jsonld"
    path.write_text(json.dumps(_person_document(extra_key="nickname")))
    with pytest.raises(NameError):
        omcore.Person.load(str(path))
    assert omcore.Person.load(str(path), ignore_unexpected_keys=True).given_name == "Ada"


def test_save_same_person_twice_preserves_remote_only_properties(mock_client):
    """
    Metadata-harvesting scripts typically build a new Person object for each
    role a person has (developer, custodian, ...) and for each project, so the
    same person may be saved several times in a single run, from objects that
    contain only the name. The second and subsequent saves must not remove the
    contact information, ORCID, etc. already held in the KG.
    """
    person_id = "https://kg.ebrains.eu/api/instances/12345678-90ab-cdef-0123-4567890abcde"
    contact_id = "https://kg.ebrains.eu/api/instances/23456789-0abc-def0-1234-567890abcdef"
    orcid_id = "https://kg.ebrains.eu/api/instances/34567890-abcd-ef01-2345-67890abcdef0"
    mock_client.instances[person_id] = {
        "@id": person_id,
        "@type": ["https://openminds.om-i.org/types/Person"],
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/givenName": "Bilbo",
        "https://openminds.om-i.org/props/familyName": "Baggins",
        "https://openminds.om-i.org/props/alternateName": ["Barrel-rider"],
        "https://openminds.om-i.org/props/contactInformation": {"@id": contact_id},
        "https://openminds.om-i.org/props/digitalIdentifier": [{"@id": orcid_id}],
    }

    # first encounter, e.g. as a developer: found by querying the KG
    developer = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    developer.save(mock_client, space="common", activity_log=log)
    assert developer.id == person_id
    assert developer.contact_information == KGProxy(omcore.ContactInformation, contact_id)
    assert [entry.type for entry in log.entries] == ["no-op"]
    assert mock_client.updates == []

    # second encounter, e.g. as a custodian: found in the save cache
    custodian = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    custodian.save(mock_client, space="common", activity_log=log)
    assert custodian.id == person_id
    assert custodian.contact_information == KGProxy(omcore.ContactInformation, contact_id)
    assert custodian.digital_identifiers == [KGProxy(omcore.ORCID, orcid_id)]
    assert custodian.alternate_names == ["Barrel-rider"]
    assert [entry.type for entry in log.entries] == ["no-op"]
    assert mock_client.updates == []


def test_save_same_new_person_twice_does_not_duplicate(mock_client, monkeypatch):
    """
    Because the KG is only eventually consistent, an instance that has just been
    created may not yet appear in query results. When a harvesting script builds
    a new Person object for each role a person has, saving the second object
    must find the instance created from the first through the save cache,
    rather than creating a duplicate.
    """
    queries = []

    def query_not_yet_consistent(query, **kwargs):
        queries.append(query)
        return MockKGResponse([])

    monkeypatch.setattr(mock_client, "query", query_not_yet_consistent)

    # first encounter, e.g. as a developer: not in the KG, so created
    developer = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    developer.save(mock_client, space="common", activity_log=log)
    assert [entry.type for entry in log.entries] == ["create"]
    assert len(mock_client.instances) == 1
    assert len(queries) == 1

    # second encounter, e.g. as a custodian: the new instance is not yet visible
    # to queries, so it must be found in the save cache
    custodian = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    custodian.save(mock_client, space="common", activity_log=log)
    assert [entry.type for entry in log.entries] == ["no-op"]
    assert custodian.id == developer.id
    assert len(mock_client.instances) == 1
    assert mock_client.updates == []
    assert len(queries) == 1  # the KG was not queried again


PERSON_ID = "https://kg.ebrains.eu/api/instances/12345678-90ab-cdef-0123-4567890abcde"


def _person_in_kg(mock_client):
    mock_client.instances[PERSON_ID] = {
        "@id": PERSON_ID,
        "@type": ["https://openminds.om-i.org/types/Person"],
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/givenName": "Bilbo",
        "https://openminds.om-i.org/props/familyName": "Baggins",
    }


def test_rejected_update_is_not_seen_when_resolving(mock_client, mocker):
    """
    An object whose update was rejected must not be returned, with its unsaved changes,
    when a link to it is later resolved (see issue #80).
    """
    from fairgraph.errors import AuthorizationError

    _person_in_kg(mock_client)
    person = omcore.Person.from_uri(PERSON_ID, mock_client)
    person.given_name = "Frodo"
    mocker.patch.object(mock_client, "update_instance", side_effect=AuthorizationError("no write access"))
    person.save(mock_client, space="common", ignore_auth_errors=True)
    assert KGProxy(omcore.Person, PERSON_ID).resolve(mock_client).given_name == "Bilbo"


def test_resolving_twice_gives_independent_objects(mock_client):
    _person_in_kg(mock_client)
    proxy = KGProxy(omcore.Person, PERSON_ID)
    first = proxy.resolve(mock_client)
    first.given_name = "Frodo"
    second = proxy.resolve(mock_client)
    assert second is not first
    assert second.given_name == "Bilbo"


def test_exists_after_delete_queries_the_kg(mock_client, mocker):
    """After an object is deleted, an equal object must not be matched to the deleted instance."""
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    person.save(mock_client, space="common")
    person.delete(mock_client)
    query = mocker.spy(mock_client, "query")
    new_person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    assert not new_person.exists(mock_client)
    assert query.call_count == 1


def test_existence_cache_hit_when_instance_cannot_yet_be_retrieved(mock_client, mocker):
    """
    An object found in the existence cache is still treated as existing if retrieving it by id
    finds nothing, in case retrieval of a newly-created instance is also subject to delays.
    """
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    person.save(mock_client, space="common")
    mocker.patch.object(mock_client, "instance_from_full_uri", return_value=None)
    query = mocker.spy(mock_client, "query")
    new_person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    assert new_person.exists(mock_client)
    assert new_person.id == person.id
    assert query.call_count == 0


def test_existence_cache_is_not_shared_between_clients(mock_client):
    from test.utils import MockKGClient

    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    person.save(mock_client, space="common")
    other_client = MockKGClient()
    new_person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    assert not new_person.exists(other_client)
    assert new_person.id is None


def test_query_results_keep_release_status(mock_client, mocker):
    """
    Objects obtained by resolving a KGQuery (e.g. a reverse property) carry the release status
    they were retrieved with, so that resolving their own links uses the same release status.
    """
    contact_id = "https://kg.ebrains.eu/api/instances/23456789-0abc-def0-1234-567890abcdef"
    person_document = {
        "@id": PERSON_ID,
        "@type": ["https://openminds.om-i.org/types/Person"],
        "https://openminds.om-i.org/props/givenName": "Bilbo",
        "https://openminds.om-i.org/props/familyName": "Baggins",
        "https://openminds.om-i.org/props/contactInformation": {"@id": contact_id},
    }
    mock_client.instances[contact_id] = {
        "@id": contact_id,
        "@type": ["https://openminds.om-i.org/types/ContactInformation"],
        "https://openminds.om-i.org/props/email": "bilbo@bag-end.example",
    }
    mocker.patch.object(mock_client, "query", return_value=MockKGResponse([person_document]))
    retrieve = mocker.spy(mock_client, "instance_from_full_uri")

    person = KGQuery([omcore.Person], {"family_name": "Baggins"}).resolve(mock_client, release_status="in progress")
    assert person.release_status == "in progress"

    person.resolve(mock_client, follow_links={"contact_information": {}})
    assert retrieve.call_args.kwargs["release_status"] == "in progress"


def test_collection_upload_with_link_to_existing_instance(mock_client, mocker, tmp_path):
    """
    A node loaded from JSON-LD that links to an instance already in the KG (not in the collection)
    holds a KGProxy for that link. Uploading it must not fail when the link is part of the
    existence query (regression test for https://github.com/HumanBrainProject/fairgraph/issues/145).
    """
    funder_id = "https://kg.ebrains.eu/api/instances/2cd6bfcd-6e3b-4b53-8b18-5a1eb6dc6f64"
    path = tmp_path / "funding.jsonld"
    path.write_text(
        json.dumps(
            {
                "@context": {"@vocab": "https://openminds.om-i.org/props/"},
                # a blank-node id, so that the node's existence is checked by querying,
                # rather than by looking up its id
                "@id": "_:funding1",
                "@type": "https://openminds.om-i.org/types/Funding",
                "funder": {"@id": funder_id},
            }
        )
    )
    collection = Collection()
    collection.load(str(path))
    (funding,) = collection.nodes.values()
    # the link leaves the collection, so it cannot be resolved to a node
    assert isinstance(funding.funder, KGProxy)
    # the mock client cannot run a query that filters on a linked node,
    # so stub it out: an empty response means "no such instance in the KG"
    query = mocker.patch.object(mock_client, "query", return_value=MockKGResponse([]))

    collection.upload(mock_client, default_space="myspace", upload_log_path=str(tmp_path / "upload_log.txt"))

    query.assert_called_once()  # i.e. the existence query was built and run
    assert len(mock_client.instances) == 1
    (instance,) = mock_client.instances.values()
    assert instance["https://openminds.om-i.org/props/funder"] == {"@id": funder_id}


@skip_if_no_connection
def test_KGQuery_resolve(kg_client):
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)
    filters = {"study_targets": ca1, "model_scope": single_cell}
    q = KGQuery(omcore.Model, filters)
    models_q = q.resolve(kg_client, release_status="released")
    models_direct = omcore.Model.list(kg_client, release_status="released", space="model", api="query", **filters)
    assert models_q == models_direct


@skip_if_no_connection
def test_KGQuery_count(kg_client):
    ca1 = omterms.UBERONParcellation.by_name("CA1 field of hippocampus", kg_client)
    single_cell = omterms.ModelScope.by_name("single cell", kg_client)
    filters = {"study_targets": ca1, "scope": single_cell}
    q = KGQuery(omcore.Model, filters)
    n_models_q = q.count(kg_client, space="model", release_status="released")
    n_models_direct = omcore.Model.count(kg_client, release_status="released", space="model", api="query", **filters)
    assert n_models_q == n_models_direct
    assert n_models_q > 1


REVERSE_TEST_ID = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000001"


def _all_reverse_properties():
    import fairgraph.openminds.v4 as v4
    import fairgraph.openminds.v5 as v5

    for version in (v4, v5):
        for module_name in dir(version):
            module = getattr(version, module_name)
            if hasattr(module, "list_kg_classes"):
                for cls in module.list_kg_classes():
                    for prop in cls.reverse_properties:
                        yield cls, prop


def test_reverse_property_queries_are_valid_for_every_target_class(mock_client):
    # the forward property does not have the same Python name in all target classes (#92)
    reverse_properties = list(_all_reverse_properties())
    assert len(reverse_properties) > 1000
    for cls, prop in reverse_properties:
        class_filters = KGQuery.from_reverse_property(prop, REVERSE_TEST_ID)._class_filters()
        assert {target for target, _ in class_filters} == set(prop.types), (cls, prop.name)
        for target, filter in class_filters:
            if not hasattr(target, "generate_query") or target.__name__ == "MRIScannerUsage":
                continue  # embedded classes cannot be queried; MRIScannerUsage query generation fails separately
            target.generate_query(client=mock_client, space=None, filters=filter)


def test_reverse_property_query_uses_the_forward_property_name_of_each_class():
    query = KGQuery.from_reverse_property(omcore.License.get_property("is_applied_to"), REVERSE_TEST_ID)
    class_filters = dict((target.__name__, filter) for target, filter in query._class_filters())
    assert class_filters["DatasetVersion"] == {"license": REVERSE_TEST_ID}
    assert class_filters["ModelVersion"] == {"licenses": REVERSE_TEST_ID}


def test_KGQuery_repr_says_how_to_resolve():
    query = KGQuery.from_reverse_property(omcore.DatasetVersion.get_property("is_version_of"), REVERSE_TEST_ID)
    assert repr(query) == (
        "KGQuery([Dataset], filter={'has_versions': '00000000-0000-0000-0000-000000000001'}) "
        "[unresolved: call .resolve(client)]"
    )


def test_reverse_property_query_covers_every_forward_property_with_the_path():
    import fairgraph.openminds.v5.core as v5core

    query = KGQuery.from_reverse_property(v5core.BehavioralProtocol.get_property("used_in"), REVERSE_TEST_ID)
    assert [filter for target, filter in query._class_filters() if target is v5core.ProtocolExecution] == [
        {"behavioral_protocols": REVERSE_TEST_ID},
        {"protocols": REVERSE_TEST_ID},
    ]


def test_resolving_reverse_property_query_returns_each_node_once():
    import fairgraph.openminds.v5.core as v5core

    execution_id = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"

    class ClientLinkingThroughBothProperties:
        # the protocol execution links to the protocol through both "behavioralProtocol" and "protocol"
        def query(self, query, size, from_index, release_status):
            if query["meta"]["type"] == v5core.ProtocolExecution.type_:
                return MockKGResponse([{"@id": execution_id, "@type": [v5core.ProtocolExecution.type_]}])
            return MockKGResponse([])

    query = KGQuery.from_reverse_property(v5core.BehavioralProtocol.get_property("used_in"), REVERSE_TEST_ID)
    result = query.resolve(ClientLinkingThroughBothProperties())
    assert isinstance(result, v5core.ProtocolExecution)
    assert result.id == execution_id


@skip_if_no_connection
def test_count_reverse_link_with_different_forward_property_names(kg_client):
    # DatasetVersion has "license", ModelVersion and SoftwareVersion have "licenses" (#92)
    license = omcore.License.by_name("CC-BY-4.0", kg_client)
    assert license.is_applied_to.count(kg_client) > 0


def test_to_jsonld():
    person1 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(name="The Lonely Mountain")),
    )
    expected1 = {
        "@context": {"@vocab": "https://openminds.om-i.org/props/"},
        "@id": "0000",
        "@type": "https://openminds.om-i.org/types/Person",
        "affiliation": [
            {
                "@type": "https://openminds.om-i.org/types/Affiliation",
                "memberOf": {
                    "@type": "https://openminds.om-i.org/types/Organization",
                    "fullName": "The Lonely Mountain",
                },
            }
        ],
        "familyName": "Oakenshield",
        "givenName": "Thorin",
    }
    assert (
        person1.to_jsonld(embed_linked_nodes=LinkedNodeEmbedding.ALWAYS, include_empty_properties=False) == expected1
    )
    with pytest.raises(ValueError) as err:
        person1.to_jsonld(embed_linked_nodes=LinkedNodeEmbedding.NEVER, include_empty_properties=False)
        assert "Exporting as a stand-alone JSON-LD document requires @id to be defined" in err

    person2 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(id="1111", name="The Lonely Mountain")),
    )
    expected2a = {
        "@context": {"@vocab": "https://openminds.om-i.org/props/"},
        "@id": "0000",
        "@type": "https://openminds.om-i.org/types/Person",
        "affiliation": [
            {
                "@type": "https://openminds.om-i.org/types/Affiliation",
                "memberOf": {
                    "@id": "1111",
                    "@type": "https://openminds.om-i.org/types/Organization",
                    "fullName": "The Lonely Mountain",
                },
            }
        ],
        "familyName": "Oakenshield",
        "givenName": "Thorin",
    }
    expected2b = {
        "@context": {"@vocab": "https://openminds.om-i.org/props/"},
        "@id": "0000",
        "@type": "https://openminds.om-i.org/types/Person",
        "affiliation": [
            {
                "@type": "https://openminds.om-i.org/types/Affiliation",
                "memberOf": {"@id": "1111"},
            }
        ],
        "familyName": "Oakenshield",
        "givenName": "Thorin",
    }
    assert (
        person2.to_jsonld(embed_linked_nodes=LinkedNodeEmbedding.ALWAYS, include_empty_properties=False) == expected2a
    )
    assert (
        person2.to_jsonld(embed_linked_nodes=LinkedNodeEmbedding.NEVER, include_empty_properties=False) == expected2b
    )


@skip_if_using_production_server
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
        scope=omterms.ModelScope.by_name("subcellular", mock_client),
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


@skip_if_using_production_server
def test_save_existing_mock(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="http://example.org/00000000-0000-0000-0000-000000000000",
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
        scope=omterms.ModelScope.by_name("subcellular", mock_client),
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


@skip_if_using_production_server
def test_save_existing_mock_no_updates_allowed(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="http://example.org/00000000-0000-0000-0000-000000000000",
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
        scope=omterms.ModelScope.by_name("subcellular", mock_client),
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


@skip_if_using_production_server
def test_save_replace_existing_mock(mock_client):
    timestamp = datetime.now()
    new_model = omcore.Model(
        id="http://example.org/00000000-0000-0000-0000-000000000000",
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
        scope=omterms.ModelScope.by_name("subcellular", mock_client),
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


@skip_if_using_production_server
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


def _seed_person(mock_client, space, uuid="12345678-90ab-cdef-0123-4567890abcde"):
    person_id = f"https://kg.ebrains.eu/api/instances/{uuid}"
    mock_client.instances[person_id] = {
        "@id": person_id,
        "@type": ["https://openminds.om-i.org/types/Person"],
        "https://core.kg.ebrains.eu/vocab/meta/space": space,
        "https://openminds.om-i.org/props/givenName": "Bilbo",
        "https://openminds.om-i.org/props/familyName": "Baggins",
    }
    return person_id


def _seed_dataset(mock_client, short_name, space="myspace", uuid="12345678-90ab-cdef-0123-4567890abcdf"):
    dataset_id = f"https://kg.ebrains.eu/api/instances/{uuid}"
    mock_client.instances[dataset_id] = {
        "@id": dataset_id,
        "@type": ["https://openminds.om-i.org/types/Dataset"],
        "https://core.kg.ebrains.eu/vocab/meta/space": space,
        "https://openminds.om-i.org/props/shortName": short_name,
    }
    return dataset_id


def test_exists_does_not_match_a_longer_name(mock_client):
    """An object must not be identified with an existing one whose name merely contains its own"""
    _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="FOO")
    assert not dataset.exists(mock_client)
    assert dataset.id is None
    assert not dataset.exists(mock_client, existence_match="equals")


def test_exists_matches_the_same_name(mock_client):
    dataset_id = _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="FOO-BAR")
    assert dataset.exists(mock_client)
    assert dataset.id == dataset_id


def test_exists_ignores_case_when_matching(mock_client):
    dataset_id = _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="foo-bar")
    assert dataset.exists(mock_client)
    assert dataset.id == dataset_id


def test_exists_does_not_ignore_whitespace_when_matching(mock_client):
    _seed_dataset(mock_client, "FOO-BAR ")
    dataset = omcore.Dataset(short_name="FOO-BAR")
    assert not dataset.exists(mock_client)


def test_exists_with_contains_matches_a_longer_name(mock_client):
    dataset_id = _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="FOO")
    assert dataset.exists(mock_client, existence_match="contains")
    assert dataset.id == dataset_id


def test_exists_with_contains_does_not_affect_later_exact_lookups(mock_client):
    """Adopting a partial match must not make a later exact lookup find it, via the save cache"""
    _seed_dataset(mock_client, "FOO-BAR")
    assert omcore.Dataset(short_name="FOO").exists(mock_client, existence_match="contains")
    assert not omcore.Dataset(short_name="FOO").exists(mock_client)
    assert omcore.Dataset(short_name="FOO").exists(mock_client, existence_match="contains")


def test_exists_with_contains_uses_exact_matches_cached_by_earlier_saves(mock_client):
    dataset = omcore.Dataset(short_name="FOO")
    dataset.save(mock_client, space="myspace", recursive=False)
    other = omcore.Dataset(short_name="FOO")
    assert other.exists(mock_client, existence_match="contains")
    assert other.id == dataset.id


def test_exists_rejects_an_invalid_existence_match(mock_client):
    dataset = omcore.Dataset(short_name="FOO")
    with pytest.raises(ValueError, match="existence_match"):
        dataset.exists(mock_client, existence_match="fuzzy")
    with pytest.raises(ValueError, match="existence_match"):
        dataset.save(mock_client, space="myspace", recursive=False, existence_match="fuzzy")


def test_save_with_contains_updates_a_longer_name(mock_client):
    dataset_id = _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="FOO")
    dataset.save(mock_client, space="myspace", recursive=False, existence_match="contains")
    assert dataset.id == dataset_id
    assert len(mock_client.instances) == 1


def test_save_creates_a_new_object_when_only_a_longer_name_exists(mock_client):
    dataset_id = _seed_dataset(mock_client, "FOO-BAR")
    dataset = omcore.Dataset(short_name="FOO")
    dataset.save(mock_client, space="myspace", recursive=False)
    assert dataset.id != dataset_id
    assert len(mock_client.instances) == 2


def test_save_passes_existence_match_to_children(mock_client):
    child_id = _seed_person(mock_client, "myspace")
    parent = omcore.Dataset(short_name="FOO", custodians=[omcore.Person(given_name="Bil", family_name="Bag")])
    parent.save(mock_client, space="myspace", recursive=True, existence_match="contains")
    assert parent.custodians[0].id == child_id


def _spy_on_query(mock_client, monkeypatch):
    """Record the `restrict_to_spaces` argument of each query sent to the mock client"""
    restrictions = []
    original_query = mock_client.query

    def query(*args, **kwargs):
        restrictions.append(kwargs.get("restrict_to_spaces", None))
        return original_query(*args, **kwargs)

    monkeypatch.setattr(mock_client, "query", query)
    return restrictions


def test_save_recursive_finds_child_in_other_space(mock_client):
    """
    A locally-constructed child that already exists in a different space from its parent
    should be linked to the existing instance, not duplicated in the parent's space (#136).
    """
    person_id = _seed_person(mock_client, "common")
    model = omcore.Model(
        name="Dummy new model with an existing developer",
        developers=omcore.Person(given_name="Bilbo", family_name="Baggins"),
    )
    log = ActivityLog()
    with pytest.warns(UserWarning, match="already exists in space 'common'.*rather than created in space 'myspace'"):
        model.save(mock_client, space="myspace", recursive=True, activity_log=log)

    person_instances = [
        instance
        for instance in mock_client.instances.values()
        if "https://openminds.om-i.org/types/Person" in instance["@type"]
    ]
    assert len(person_instances) == 1
    assert model.developers.id == person_id
    assert model.developers.space == "common"
    person_entries = [entry for entry in log.entries if entry.cls == "Person"]
    assert len(person_entries) == 1
    assert person_entries[0].space == "common"
    assert person_entries[0].type != "create"
    assert model.space == "myspace"


def test_save_finds_object_in_other_space(mock_client):
    person_id = _seed_person(mock_client, "common")
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    with pytest.warns(UserWarning, match="already exists in space 'common'"):
        person.save(mock_client, space="myspace", recursive=False, activity_log=log)
    assert person.id == person_id
    assert person.space == "common"
    assert len(mock_client.instances) == 1
    assert [(entry.type, entry.space) for entry in log.entries] == [("no-op", "common")]


def test_save_prefers_instance_in_target_space(mock_client, monkeypatch, recwarn):
    """
    If the object exists both in the target space and elsewhere, the instance in the target space
    is used, and the other one is not treated as a duplicate.
    """
    _seed_person(mock_client, "common")
    target_id = _seed_person(mock_client, "myspace", uuid="23456789-0abc-def0-1234-567890abcdef")
    restrictions = _spy_on_query(mock_client, monkeypatch)
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    log = ActivityLog()
    person.save(mock_client, space="myspace", recursive=False, activity_log=log)
    assert person.id == target_id
    assert person.space == "myspace"
    assert restrictions == [None]
    assert [(entry.type, entry.space) for entry in log.entries] == [("no-op", "myspace")]
    assert not [w for w in recwarn if "already exists in space" in str(w.message)]


def test_save_new_object_queries_all_spaces_once(mock_client, monkeypatch):
    _seed_person(mock_client, "common")
    restrictions = _spy_on_query(mock_client, monkeypatch)
    person = omcore.Person(given_name="Frodo", family_name="Baggins")
    log = ActivityLog()
    person.save(mock_client, space="myspace", recursive=False, activity_log=log)
    assert restrictions == [None]
    assert [(entry.type, entry.space) for entry in log.entries] == [("create", "myspace")]
    assert len(mock_client.instances) == 2


def test_save_object_with_local_space_found_in_other_space(mock_client):
    person_id = _seed_person(mock_client, "common")
    person = omcore.Person(given_name="Bilbo", family_name="Baggins", space="myspace")
    log = ActivityLog()
    with pytest.warns(UserWarning, match="already exists in space 'common'.*rather than created in space 'myspace'"):
        person.save(mock_client, recursive=False, activity_log=log)
    assert person.id == person_id
    assert person.space == "common"
    assert [(entry.type, entry.space) for entry in log.entries] == [("no-op", "common")]
    assert len(mock_client.instances) == 1


def test_save_duplicates_in_target_space(mock_client):
    _seed_person(mock_client, "common")
    _seed_person(mock_client, "myspace", uuid="23456789-0abc-def0-1234-567890abcdef")
    _seed_person(mock_client, "myspace", uuid="34567890-abcd-ef01-2345-67890abcdef0")
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    with pytest.raises(Exception, match="Existence query is not specific enough"):
        person.save(mock_client, space="myspace", recursive=False)
    assert len(mock_client.instances) == 3


def test_save_retrieves_all_matches_if_more_than_query_size(mock_client, monkeypatch):
    """
    The existence query asks for only a few results. If more instances match, they are all retrieved,
    so that an instance in the target space is not missed.
    """
    for i in range(EXISTENCE_QUERY_SIZE + 1):
        _seed_person(mock_client, f"collab-{i}", uuid=f"00000000-0000-0000-0000-00000000000{i}")
    target_id = _seed_person(mock_client, "myspace", uuid="23456789-0abc-def0-1234-567890abcdef")

    sizes = []
    original_query = mock_client.query

    def paginated_query(*args, size=100, **kwargs):
        sizes.append(size)
        response = original_query(*args, size=size, **kwargs)
        total = response.total
        response.data = response.data[:size]
        response.total = total
        return response

    monkeypatch.setattr(mock_client, "query", paginated_query)
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    person.save(mock_client, space="myspace", recursive=False, ignore_duplicates=True)
    assert sizes == [EXISTENCE_QUERY_SIZE, EXISTENCE_QUERY_SIZE + 2]
    assert person.id == target_id


def test_exists_connection_lost(mock_client, monkeypatch):
    def disconnected_query(*args, **kwargs):
        raise ConnectionError(
            ("Connection aborted.", RemoteDisconnected("Remote end closed connection without response"))
        )

    monkeypatch.setattr(mock_client, "query", disconnected_query)
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    with pytest.warns(UserWarning, match="Timeout when checking for existence"):
        assert not person.exists(mock_client)


def test_exists_other_connection_error(mock_client, monkeypatch):
    def refused_query(*args, **kwargs):
        raise ConnectionError("Failed to establish a new connection: [Errno 61] Connection refused")

    monkeypatch.setattr(mock_client, "query", refused_query)
    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    with pytest.raises(ConnectionError, match="Connection refused"):
        person.exists(mock_client)
    with pytest.raises(ConnectionError, match="Connection refused"):
        person.save(mock_client, space="myspace", recursive=False)


def test_save_duplicates_in_other_spaces(mock_client):
    first_id = _seed_person(mock_client, "common")
    _seed_person(mock_client, "collab-foo", uuid="23456789-0abc-def0-1234-567890abcdef")

    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    with pytest.raises(Exception, match="Existence query is not specific enough"):
        person.save(mock_client, space="myspace", recursive=False)
    assert len(mock_client.instances) == 2

    person = omcore.Person(given_name="Bilbo", family_name="Baggins")
    with pytest.warns(UserWarning, match="already exists in space 'common'"):
        person.save(mock_client, space="myspace", recursive=False, ignore_duplicates=True)
    assert person.id == first_id
    assert len(mock_client.instances) == 2


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


def test_normalize_filter_with_invalid_keys():
    with pytest.raises(ValueError) as excinfo:
        omcore.ModelVersion.normalize_filter(
            {"authors": {"given_name": "Zaphod"}, "documentation": {"iri": "http://example.org"}}
        )  # should be "developers", "full_documentation"
    assert str(excinfo.value) == "Invalid filters: authors, documentation"
    with pytest.raises(ValueError) as excinfo:
        omcore.ModelVersion.normalize_filter(
            {"developers": {"digital_identifiers": {"id": "https://orcid.org/some-id"}}}
        )  # should be "identifier", not "id"
    assert str(excinfo.value) == "Invalid filter: id"


def test_class_docstring():
    assert "email address" in omcore.Person.__doc__


def test_property_names():
    assert omcore.Person.property_names == [
        "affiliations",
        "alternate_names",
        "associated_accounts",
        "contact_information",
        "digital_identifiers",
        "family_name",
        "given_name",
    ]
    assert omcore.Person.reverse_property_names == [
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
    assert omcore.Person.required_property_names == ["given_name"]


def test_diff():
    person1 = omcore.Person(
        id="0000",
        given_name="Thorin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(id="1000", name="The Lonely Mountain")),
    )
    person2 = omcore.Person(
        given_name="Thorin son of Thráin",
        family_name="Oakenshield",
        affiliations=omcore.Affiliation(member_of=omcore.Organization(id="1001", name="Erebor")),
    )
    expected = {
        "id": ("0000", None),
        "properties": {
            "given_name": ("Thorin", "Thorin son of Thráin"),
            "affiliations": (
                omcore.Affiliation(member_of=omcore.Organization(id="1000", name="The Lonely Mountain")),
                omcore.Affiliation(member_of=omcore.Organization(id="1001", name="Erebor")),
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


def _local_file_obj(tmp_path, algorithm, digest):
    source = tmp_path / "source.txt"
    source.write_text("There and back again\n")
    return omcore.File(
        name="source.txt",
        iri=IRI(source.as_uri()),
        hashes=omcore.Hash(algorithm=algorithm, digest=digest),
    )


@pytest.mark.parametrize("algorithm", ["MD5", "SHA1", "SHA-256"])
def test_file_download_checks_hash(tmp_path, algorithm):
    import hashlib

    content = b"There and back again\n"
    digest = hashlib.new(algorithm.lower().replace("-", ""), content).hexdigest()
    file_obj = _local_file_obj(tmp_path, algorithm, digest)
    local_filename = file_obj.download(tmp_path / "copy.txt", client=None, accept_terms_of_use=True)
    assert open(local_filename, "rb").read() == content


def test_file_download_raises_if_hash_does_not_match(tmp_path):
    file_obj = _local_file_obj(tmp_path, "MD5", "0" * 32)
    with pytest.raises(ValueError, match="does not match the MD5 digest"):
        file_obj.download(tmp_path / "copy.txt", client=None, accept_terms_of_use=True)
    # the check can be skipped
    file_obj.download(tmp_path / "copy2.txt", client=None, accept_terms_of_use=True, check_hash=False)


def test_file_download_skips_multipart_md5_digests(tmp_path):
    # e.g. a file uploaded to the EBRAINS data store in 4 parts
    file_obj = _local_file_obj(tmp_path, "MD5", "9b2cf535f27731c974343645a3985328-4")
    with pytest.warns(UserWarning, match="from an upload in several parts"):
        file_obj.download(tmp_path / "copy.txt", client=None, accept_terms_of_use=True)
    # no warning if the check was not requested
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        file_obj.download(tmp_path / "copy2.txt", client=None, accept_terms_of_use=True, check_hash=False)


def test_file_download_skips_unknown_hash_algorithms(tmp_path):
    file_obj = _local_file_obj(tmp_path, "NOT-AN-ALGORITHM", "1234")
    file_obj.download(tmp_path / "copy.txt", client=None, accept_terms_of_use=True)


def test_file_from_local_file():
    file_obj = omcore.File.from_local_file("test/utils.py")
    assert file_obj.name == "test/utils.py"
    assert file_obj.storage_size.value == float(os.stat("test/utils.py").st_size)
    # the controlled terms are the instances from the openMINDS library, not new objects
    assert file_obj.storage_size.unit is omterms.UnitOfMeasurement.byte
    assert file_obj.format.id == "https://openminds.om-i.org/instances/contentTypes/text_x-python"
    assert file_obj.hashes.digest == sha1sum("test/utils.py")


def test_file_from_local_file_with_unknown_type(tmp_path):
    path = tmp_path / "recording.unknownextension"
    path.write_bytes(b"\x00\x01")
    file_obj = omcore.File.from_local_file(str(path))
    assert file_obj.format is None
    assert file_obj.storage_size.value == 2.0


@skip_if_no_connection
def test_dataset_version_download(mocker):
    mock_urlretrieve = mocker.patch(
        "fairgraph.openminds.core.products.dataset_version.urlretrieve",
        lambda url, local_filename: (local_filename, None),
    )
    fake_dsv = omcore.DatasetVersion(
        repository=omcore.FileRepository(iri=IRI("https://data-proxy.ebrains.eu/api/v1/buckets/foo/bar"))
    )
    local_dir = tempfile.mkdtemp()
    local_filename, repository_url = fake_dsv.download(local_dir, client=None, accept_terms_of_use=True)
    os.rmdir(local_dir)
    assert repository_url == "https://data-proxy.ebrains.eu/api/v1/buckets/foo/bar"
    assert str(local_filename) == os.path.join(local_dir, "bar.zip")


@skip_if_no_connection
def test_person_me(kg_client):
    person = omcore.Person.me(kg_client, allow_multiple=False)
    # the following assumes that anyone running these tests is represented in the KG
    assert isinstance(person, omcore.Person)


# def test_children():


def test_with_new_namespace_from_core():
    data = {
        "https://openminds.om-i.org/props/hasVersion": {
            "@id": "https://kg.ebrains.eu/api/instances/7035d53f-1597-4a45-9f72-23c2c933ec66"
        },
        "@type": "https://openminds.om-i.org/types/Model",
        "https://openminds.om-i.org/props/description": "The scaffolding procedure has been enhanced compared to version 1.0. It's able to generate a scalable cerebellar structure, embedding specific 3D positions for each neuron and specific pair connections. Customized placement strategies allow to match layered density and encumbrance for each neuron type. Customized connection strategies allow to match anisotropic geometrical fields of intersection, and statistical convergence and divergence ratios.\nThe scaffold can host different neuron models. Several input stimulation patterns can be used to investigate network complex dynamics, revealing the relationships between structural constraints and underlying neuron mechanisms with the cerebellar circuit functioning, over space and time.\n\nMain link to Sonata conversion can be found here:\nhttps://github.com/SelezioneCasuale/scaffold/tree/sonata-version/scaffold",
        "https://openminds.om-i.org/props/studyTarget": [
            {"@id": "https://kg.ebrains.eu/api/instances/ab532423-1fd7-4255-8c6f-f99dc6df814f"},
            {"@id": "https://kg.ebrains.eu/api/instances/a70b0307-22fc-4730-a61f-fd279f43a3cf"},
        ],
        "https://core.kg.ebrains.eu/vocab/meta/revision": "_hEUXXvy--q",
        "https://openminds.om-i.org/props/custodian": [
            {"@id": "https://kg.ebrains.eu/api/instances/2905ce6c-bc89-4c99-b8b0-0fa9a17d1897"},
            {"@id": "https://kg.ebrains.eu/api/instances/3477f916-5494-42ae-8b07-d2cb48231657"},
            {"@id": "https://kg.ebrains.eu/api/instances/a594cfe2-f53a-470f-b52e-697b8d5a8958"},
            {"@id": "https://kg.ebrains.eu/api/instances/5dcb9bd9-f93f-48c4-88e0-ff0ed4221ac8"},
            {"@id": "https://kg.ebrains.eu/api/instances/5ad4749a-6e5a-4512-86ff-b89834c1b87c"},
        ],
        "https://openminds.om-i.org/props/developer": [
            {"@id": "https://kg.ebrains.eu/api/instances/2905ce6c-bc89-4c99-b8b0-0fa9a17d1897"},
            {"@id": "https://kg.ebrains.eu/api/instances/3477f916-5494-42ae-8b07-d2cb48231657"},
            {"@id": "https://kg.ebrains.eu/api/instances/a594cfe2-f53a-470f-b52e-697b8d5a8958"},
            {"@id": "https://kg.ebrains.eu/api/instances/5dcb9bd9-f93f-48c4-88e0-ff0ed4221ac8"},
            {"@id": "https://kg.ebrains.eu/api/instances/5ad4749a-6e5a-4512-86ff-b89834c1b87c"},
        ],
        "https://openminds.om-i.org/props/fullName": "Scaffold Model of Cerebellum microcircuit version 2.0",
        "https://core.kg.ebrains.eu/vocab/meta/space": "model",
        "https://openminds.om-i.org/props/abstractionLevel": {
            "@id": "https://kg.ebrains.eu/api/instances/57becc19-f0a1-4d23-99bb-eb3b7d3cdb9a"
        },
        "@id": "https://kg.ebrains.eu/api/instances/708024f7-9dd7-4c92-ae95-936db23c6d99",
        "https://openminds.om-i.org/props/scope": {
            "@id": "https://kg.ebrains.eu/api/instances/6c678004-b8e0-4339-90c5-824e66503eb9"
        },
        "http://schema.org/identifier": ["https://kg.ebrains.eu/api/instances/708024f7-9dd7-4c92-ae95-936db23c6d99"],
        "https://core.kg.ebrains.eu/vocab/meta/firstReleasedAt": "2022-02-04T15:11:40.157Z",
        "https://core.kg.ebrains.eu/vocab/meta/lastReleasedAt": "2023-03-23T10:09:30.130Z",
    }
    orig_type = omcore.Model.type_
    obj = omcore.Model.from_jsonld(data, ignore_unexpected_keys=True, release_status="released")
    assert obj.abstraction_level
    assert len(obj.developers) == 5
    omcore.Model.type_ = orig_type


def test_with_new_namespace_from_query():
    data = {
        "@id": "https://kg.ebrains.eu/api/instances/708024f7-9dd7-4c92-ae95-936db23c6d99",
        "https://schema.hbp.eu/myQuery/space": "model",
        "@type": "https://openminds.om-i.org/types/Model",
        "abstractionLevel": {"@id": "https://kg.ebrains.eu/api/instances/57becc19-f0a1-4d23-99bb-eb3b7d3cdb9a"},
        "custodian": [
            {
                "@id": "https://kg.ebrains.eu/api/instances/2905ce6c-bc89-4c99-b8b0-0fa9a17d1897",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/3477f916-5494-42ae-8b07-d2cb48231657",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/a594cfe2-f53a-470f-b52e-697b8d5a8958",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/5dcb9bd9-f93f-48c4-88e0-ff0ed4221ac8",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/5ad4749a-6e5a-4512-86ff-b89834c1b87c",
                "@type": "https://openminds.om-i.org/types/Person",
            },
        ],
        "description": "The scaffolding procedure has been enhanced compared to version 1.0. It's able to generate a scalable cerebellar structure, embedding specific 3D positions for each neuron and specific pair connections. Customized placement strategies allow to match layered density and encumbrance for each neuron type. Customized connection strategies allow to match anisotropic geometrical fields of intersection, and statistical convergence and divergence ratios.\nThe scaffold can host different neuron models. Several input stimulation patterns can be used to investigate network complex dynamics, revealing the relationships between structural constraints and underlying neuron mechanisms with the cerebellar circuit functioning, over space and time.\n\nMain link to Sonata conversion can be found here:\nhttps://github.com/SelezioneCasuale/scaffold/tree/sonata-version/scaffold",
        "developer": [
            {
                "@id": "https://kg.ebrains.eu/api/instances/2905ce6c-bc89-4c99-b8b0-0fa9a17d1897",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/3477f916-5494-42ae-8b07-d2cb48231657",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/a594cfe2-f53a-470f-b52e-697b8d5a8958",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/5dcb9bd9-f93f-48c4-88e0-ff0ed4221ac8",
                "@type": "https://openminds.om-i.org/types/Person",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/5ad4749a-6e5a-4512-86ff-b89834c1b87c",
                "@type": "https://openminds.om-i.org/types/Person",
            },
        ],
        "digitalIdentifier": [],
        "fullName": "Scaffold Model of Cerebellum microcircuit version 2.0",
        "hasVersion": [
            {
                "@id": "https://kg.ebrains.eu/api/instances/7035d53f-1597-4a45-9f72-23c2c933ec66",
                "@type": "https://openminds.om-i.org/types/ModelVersion",
            }
        ],
        "homepage": None,
        "howToCite": None,
        "scope": [
            {
                "@id": "https://kg.ebrains.eu/api/instances/6c678004-b8e0-4339-90c5-824e66503eb9",
                "@type": "https://openminds.om-i.org/types/ModelScope",
            }
        ],
        "shortName": None,
        "studyTarget": [
            {
                "@id": "https://kg.ebrains.eu/api/instances/ab532423-1fd7-4255-8c6f-f99dc6df814f",
                "@type": "https://openminds.om-i.org/types/Species",
            },
            {
                "@id": "https://kg.ebrains.eu/api/instances/a70b0307-22fc-4730-a61f-fd279f43a3cf",
                "@type": "https://openminds.om-i.org/types/UBERONParcellation",
            },
        ],
        "about": [],
        "hasPart": [],
        "@context": {"@vocab": "https://openminds.om-i.org/props/"},
    }
    # omcore.set_error_handling("error")
    orig_types = (omcore.Model.type_, omcore.Person.type_)
    obj = omcore.Model.from_jsonld(data, ignore_unexpected_keys=True, release_status="released")
    assert obj.abstraction_level
    assert len(obj.developers) == 5
    omcore.Model.type_, omcore.Person.type_ = orig_types


@skip_if_no_connection
def test_by_name_searches_all_name_like_properties(kg_client):
    # License has both "full_name" and "short_name"; only the first used to be searched
    # https://github.com/HumanBrainProject/fairgraph/issues/131
    licence = omcore.License.by_name("CC-BY-NC-4.0", kg_client)
    assert licence is not None
    assert licence.short_name == "CC-BY-NC-4.0"
    assert omcore.License.by_name(licence.full_name, kg_client) == licence


@skip_if_no_connection
def test_by_name_searches_synonyms(kg_client):
    mouse = omterms.Species.by_name("Mus musculus", kg_client)
    assert omterms.Species.by_name("house mouse", kg_client) == mouse


@skip_if_no_connection
def test_by_name_is_case_sensitive_by_default(kg_client):
    assert omterms.Species.by_name("mus musculus", kg_client) is None
    assert omterms.Species.by_name("mus musculus", kg_client, case_sensitive=False).name == "Mus musculus"


@skip_if_no_connection
def test_by_name_ignore_accents(kg_client):
    # the KG does no accent folding of its own, so this exercises the generated character classes
    plain = omcore.Person.by_name("Muller", kg_client, match="contains", all=True) or []
    folded = omcore.Person.by_name("Muller", kg_client, match="contains", all=True, ignore_accents=True) or []
    assert len(folded) > len(plain)
    assert {person.id for person in plain} < {person.id for person in folded}
    assert any("ü" in person.family_name for person in folded)


@skip_if_no_connection
def test_by_name_match_within(kg_client):
    mouse = omterms.Species.by_name("Mus musculus", kg_client)
    assert omterms.Species.by_name("recordings from Mus musculus", kg_client, match="within") == mouse


@skip_if_no_connection
def test_by_name_returns_none_when_nothing_matches(kg_client):
    assert omterms.Species.by_name("definitely not a species", kg_client) is None


@skip_if_no_connection
def test_by_name_requires_a_name_like_property(kg_client):
    with pytest.raises(AttributeError):
        omcore.DOI.by_name("10.25493/ANYTHING", kg_client)


# --- existence_match="normalized" (issue #184) ---

CHATELET_ID = "https://kg.ebrains.eu/api/instances/56789012-cdef-0123-4567-890abcdef012"
CHATELET_ORCID_ID = "https://kg.ebrains.eu/api/instances/67890123-def0-1234-5678-90abcdef0123"
EXAMPLE_ORCID = "https://orcid.org/0000-0002-1825-0097"


def _seed_named_person(mock_client, given_name, family_name, person_id=CHATELET_ID, orcid_id=None):
    mock_client.instances[person_id] = {
        "@id": person_id,
        "@type": ["https://openminds.om-i.org/types/Person"],
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/givenName": given_name,
        "https://openminds.om-i.org/props/familyName": family_name,
    }
    if orcid_id:
        mock_client.instances[orcid_id] = {
            "@id": orcid_id,
            "@type": ["https://openminds.om-i.org/types/ORCID"],
            "https://core.kg.ebrains.eu/vocab/meta/space": "common",
            "https://openminds.om-i.org/props/identifier": EXAMPLE_ORCID,
        }
        mock_client.instances[person_id]["https://openminds.om-i.org/props/digitalIdentifier"] = [{"@id": orcid_id}]
    return person_id


def test_exists_normalized_ignores_accents(mock_client):
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    assert not omcore.Person(given_name="Emilie", family_name="du Chatelet").exists(mock_client)
    person = omcore.Person(given_name="Emilie", family_name="du Chatelet")
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID


def test_exists_normalized_ignores_differences_in_whitespace(mock_client):
    _seed_named_person(mock_client, " Émilie", "du  Châtelet ")
    person = omcore.Person(given_name="Emilie", family_name="du Chatelet")
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID


def test_exists_normalized_does_not_match_a_longer_name(mock_client):
    _seed_named_person(mock_client, "Émilie", "du Châtelet-Lomont")
    person = omcore.Person(given_name="Emilie", family_name="du Chatelet")
    assert not person.exists(mock_client, existence_match="normalized")


def test_save_normalized_adopts_the_stored_spelling(mock_client):
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    person = omcore.Person(given_name="emilie", family_name="Du  Chatelet")
    log = ActivityLog()
    person.save(mock_client, space="common", existence_match="normalized", activity_log=log)
    assert person.id == CHATELET_ID
    assert (person.given_name, person.family_name) == ("Émilie", "du Châtelet")
    assert person.modified_data() == {}
    assert [entry.type for entry in log.entries] == ["no-op"]
    assert mock_client.updates == []


def test_exists_normalized_prefers_the_exact_match(mock_client):
    other_id = "https://kg.ebrains.eu/api/instances/78901234-ef01-2345-6789-0abcdef01234"
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    _seed_named_person(mock_client, "Emilie", "du Chatelet", person_id=other_id)
    person = omcore.Person(given_name="emilie", family_name="du chatelet")
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == other_id
    person = omcore.Person(given_name="Émilie", family_name="du Châtelet")
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID


def test_exists_normalized_raises_if_there_is_no_single_best_match(mock_client):
    other_id = "https://kg.ebrains.eu/api/instances/78901234-ef01-2345-6789-0abcdef01234"
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    _seed_named_person(mock_client, "Emilie", "du Chatelet", person_id=other_id)
    with pytest.raises(Exception, match="not specific enough"):
        omcore.Person(given_name="Émilie", family_name="du Chatelet").exists(mock_client, existence_match="normalized")
    person = omcore.Person(given_name="Émilie", family_name="du Chatelet")
    assert person.exists(mock_client, existence_match="normalized", ignore_duplicates=True)
    assert person.id in (CHATELET_ID, other_id)


def test_exists_normalized_does_not_affect_later_exact_lookups(mock_client):
    """A normalized match must not make a later exact lookup find it, via the save cache"""
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    assert omcore.Person(given_name="Emilie", family_name="du Chatelet").exists(
        mock_client, existence_match="normalized"
    )
    assert not omcore.Person(given_name="Emilie", family_name="du Chatelet").exists(mock_client)


def test_exists_normalized_for_a_class_without_an_override(mock_client):
    dataset_id = _seed_dataset(mock_client, "Café  au lait")
    dataset = omcore.Dataset(short_name="cafe au lait")
    assert not dataset.exists(mock_client)
    assert dataset.exists(mock_client, existence_match="normalized")
    assert dataset.id == dataset_id


def test_exists_normalized_finds_a_person_by_orcid(mock_client):
    _seed_named_person(mock_client, "Gabrielle Émilie", "Le Tonnelier de Breteuil", orcid_id=CHATELET_ORCID_ID)
    person = omcore.Person(
        given_name="Émilie", family_name="du Châtelet", digital_identifiers=[omcore.ORCID(identifier=EXAMPLE_ORCID)]
    )
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID
    # the names differ, so the local ones are kept, and would be saved
    assert person.family_name == "du Châtelet"


def test_exists_normalized_finds_a_person_by_a_linked_orcid(mock_client):
    _seed_named_person(mock_client, "Gabrielle Émilie", "Le Tonnelier de Breteuil", orcid_id=CHATELET_ORCID_ID)
    person = omcore.Person(
        given_name="Émilie",
        family_name="du Châtelet",
        digital_identifiers=[KGProxy(omcore.ORCID, CHATELET_ORCID_ID)],
    )
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID


def test_exists_normalized_falls_back_to_names_without_an_orcid_match(mock_client):
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    person = omcore.Person(
        given_name="Emilie", family_name="du Chatelet", digital_identifiers=[omcore.ORCID(identifier=EXAMPLE_ORCID)]
    )
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID


def test_exists_equals_ignores_the_orcid(mock_client):
    _seed_named_person(mock_client, "Gabrielle Émilie", "Le Tonnelier de Breteuil", orcid_id=CHATELET_ORCID_ID)
    person = omcore.Person(
        given_name="Émilie", family_name="du Châtelet", digital_identifiers=[omcore.ORCID(identifier=EXAMPLE_ORCID)]
    )
    assert not person.exists(mock_client)


def test_exists_normalized_finds_an_organization_by_ror_id(mock_client):
    ror_id = "https://kg.ebrains.eu/api/instances/89012345-f012-3456-7890-abcdef012345"
    _seed_lonely_mountain(mock_client)
    mock_client.instances[ror_id] = {
        "@id": ror_id,
        "@type": ["https://openminds.om-i.org/types/RORID"],
        "https://core.kg.ebrains.eu/vocab/meta/space": "common",
        "https://openminds.om-i.org/props/identifier": "https://ror.org/000000000",
    }
    mock_client.instances[LONELY_MOUNTAIN_ID]["https://openminds.om-i.org/props/digitalIdentifier"] = [{"@id": ror_id}]
    org = omcore.Organization(
        full_name="Erebor", digital_identifiers=[omcore.RORID(identifier="https://ror.org/000000000")]
    )
    assert not org.exists(mock_client)
    assert org.exists(mock_client, existence_match="normalized")
    assert org.id == LONELY_MOUNTAIN_ID


def test_exists_normalized_finds_an_organization_by_name(mock_client):
    _seed_lonely_mountain(mock_client)
    org = omcore.Organization(full_name="Kingdom  under the Lonely Mountain ")
    assert org.exists(mock_client, existence_match="normalized")
    assert org.id == LONELY_MOUNTAIN_ID


def test_exists_normalized_skips_an_identifier_with_a_local_id(mock_client, mocker):
    _seed_named_person(mock_client, "Émilie", "du Châtelet", orcid_id=CHATELET_ORCID_ID)
    orcid = omcore.ORCID(identifier=EXAMPLE_ORCID, id="_:000001")
    person = omcore.Person(given_name="Emilie", family_name="du Chatelet", digital_identifiers=[orcid])
    query = mocker.spy(mock_client, "query")
    assert person.exists(mock_client, existence_match="normalized")
    assert person.id == CHATELET_ID
    assert orcid.id == "_:000001"
    # only the name query was run, not one for the local identifier
    assert query.call_count == 1


@pytest.mark.parametrize("existence_match,expect_new", [("equals", True), ("normalized", False)])
def test_collection_upload_with_existence_match(mock_client, tmp_path, existence_match, expect_new):
    _seed_named_person(mock_client, "Émilie", "du Châtelet")
    collection = Collection(omcore.Person(given_name="Emilie", family_name="du Chatelet"))
    collection.upload(
        mock_client,
        default_space="common",
        upload_log_path=str(tmp_path / "upload_log.txt"),
        existence_match=existence_match,
    )
    (person,) = collection.nodes.values()
    if expect_new:
        assert person.id != CHATELET_ID
        assert len(mock_client.instances) == 2
    else:
        assert person.id == CHATELET_ID
        assert person.given_name == "Émilie"
        assert len(mock_client.instances) == 1
        assert mock_client.updates == []
