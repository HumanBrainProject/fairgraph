import os
import tempfile
import pytest
from fairgraph.utility import (
    expand_filter,
    compact_uri,
    in_notebook,
    accepted_terms_of_use,
    sha1sum,
    normalize_data,
)
from .utils import kg_client, skip_if_no_connection


def test_expand_filter():
    filter = {
        "developers__affiliations__member_of__alias": "CNRS",
        "digital_identifier__identifier": "https://doi.org/some-doi",
    }
    result = expand_filter(filter)
    expected = {
        "developers": {"affiliations": {"member_of": {"alias": "CNRS"}}},
        "digital_identifier": {"identifier": "https://doi.org/some-doi"},
    }
    assert result == expected


def test_compact_uri():
    context = {"foaf": "http://xmlns.com/foaf/0.1/"}
    uri_list = "http://xmlns.com/foaf/0.1/Person"
    result = compact_uri(uri_list, context)
    assert result == "foaf:Person"

    uri_list = ["http://xmlns.com/foaf/0.1/Person", "foaf:homepage"]
    result = compact_uri(uri_list, context)
    assert result == ("foaf:Person", "foaf:homepage")

    uri_list = "http://purl.org/dc/elements/1.1/creator"
    with pytest.raises(ValueError):
        result = compact_uri(uri_list, context, strict=True)
    result = compact_uri(uri_list, context)
    assert result == uri_list


def test_in_notebook():
    assert not in_notebook()


@skip_if_no_connection
def test_accepted_terms_of_use(kg_client, mocker):
    result = accepted_terms_of_use(kg_client, accept_terms_of_use=True)
    assert result is True
    mocker.patch("builtins.input")
    result = accepted_terms_of_use(kg_client, accept_terms_of_use=False)
    assert result is False
    mocker.patch("builtins.input", lambda prompt: "yes")
    result = accepted_terms_of_use(kg_client, accept_terms_of_use=False)
    assert result is True


def test_sha1sum():
    fp = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    fp.write(b"0" * 256)
    fp.close()
    assert sha1sum(fp.name) == "80a963e503e9ed478c2cc528fd344d58122929c2"
    os.remove(fp.name)


def test_normalize_data():
    data = {
        "@id": "http://example.org/00000000-0000-0000-0000-000000000000",
        "@type": "https://openminds.ebrains.eu/core/Person",
        "affiliation": {
            "@type": "https://openminds.ebrains.eu/core/Affiliation",
            "memberOf": {
                "@type": "https://openminds.ebrains.eu/core/Organization",
                "fullName": "The Lonely Mountain",
            },
        },
        "familyName": "Oakenshield",
        "givenName": "Thorin",
        "alternateName": None
    }
    context = {"@vocab": "https://openminds.ebrains.eu/vocab/"}
    expected = {
        "@id": "http://example.org/00000000-0000-0000-0000-000000000000",
        "@type": "https://openminds.ebrains.eu/core/Person",
        "https://openminds.ebrains.eu/vocab/affiliation": {
            "@type": "https://openminds.ebrains.eu/core/Affiliation",
            "https://openminds.ebrains.eu/vocab/memberOf": {
                "@type": "https://openminds.ebrains.eu/core/Organization",
                "https://openminds.ebrains.eu/vocab/fullName": "The Lonely Mountain",
            },
        },
        "https://openminds.ebrains.eu/vocab/familyName": "Oakenshield",
        "https://openminds.ebrains.eu/vocab/givenName": "Thorin",
        "https://openminds.ebrains.eu/vocab/alternateName": None
    }
    assert normalize_data(data, context) == expected


