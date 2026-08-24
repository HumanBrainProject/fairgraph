# encoding: utf-8
"""
Tests of KGObject.by_name() using the local instance library
(no Knowledge Graph connection needed).

Regression test for https://github.com/HumanBrainProject/fairgraph/issues/130:
by_name() raised TypeError ("object of type 'NoneType' has no len()")
instead of returning None when no instance matched.
"""

from openminds.properties import Property

from fairgraph.kgobject import KGObject

import pytest


class MockNamedTerm(KGObject):
    """A mock controlled-term-like class with an empty instance library."""

    type_ = "https://openminds.ebrains.eu/mock/MockNamedTerm"
    default_space = "mock"
    _instance_lookup = None
    properties = [
        Property("name", str, "https://openminds.ebrains.eu/vocab/name", multiple=False, required=False)
    ]
    reverse_properties = []

    @classmethod
    def instances(cls):
        return []


def test_by_name_no_match_returns_none():
    assert MockNamedTerm.by_name("definitely not a term") is None


def test_by_name_contains_no_match_returns_none():
    assert MockNamedTerm.by_name("definitely not a term", match="contains") is None


def test_by_name_match_found():
    obj = MockNamedTerm(id="https://mock/kg/instances/00000000-0000-0000-0000-000000000001",
                        space="mock", name="Rattus norvegicus")
    MockNamedTerm._instance_lookup = {"Rattus norvegicus": [obj]}
    try:
        assert MockNamedTerm.by_name("Rattus norvegicus") is obj
    finally:
        MockNamedTerm._instance_lookup = None


def test_by_name_multiple_matches_warns_and_returns_first():
    obj1 = MockNamedTerm(id="https://mock/kg/instances/00000000-0000-0000-0000-000000000002",
                         space="mock", name="Mus musculus")
    obj2 = MockNamedTerm(id="https://mock/kg/instances/00000000-0000-0000-0000-000000000003",
                         space="mock", name="Mus musculus")
    MockNamedTerm._instance_lookup = {"Mus musculus": [obj1, obj2]}
    try:
        with pytest.warns(UserWarning, match="Multiple objects"):
            result = MockNamedTerm.by_name("Mus musculus")
        assert result is obj1
        assert MockNamedTerm.by_name("Mus musculus", all=True) == [obj1, obj2]
    finally:
        MockNamedTerm._instance_lookup = None


def test_by_name_invalid_match_raises_valueerror():
    try:
        MockNamedTerm.by_name("anything", match="approximate")
    except ValueError as err:
        assert "match" in str(err)
    else:
        raise AssertionError("ValueError not raised for invalid 'match' value")
