# encoding: utf-8
"""
Tests of fairgraph.base module.
"""

from datetime import date, datetime
from fairgraph.embedded import EmbeddedMetadata
from fairgraph.kgobject import KGObject
from fairgraph.kgproxy import KGProxy
from fairgraph.properties import Property
from fairgraph.caching import generate_cache_key
import pytest


class MockEmbeddedObject(EmbeddedMetadata):
    type_ = "https://openminds.ebrains.eu/mock/MockEmbeddedObject"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "mock": "https://openminds.ebrains.eu/mock/",
    }
    properties = [
        Property(
            "a_string",
            str,
            "https://openminds.ebrains.eu/vocab/aString",
            multiple=False,
            required=False,
        ),
        Property(
            "a_date",
            date,
            "https://openminds.ebrains.eu/vocab/aDate",
            multiple=False,
            required=False,
        ),
        Property(
            "a_number",
            float,
            "https://openminds.ebrains.eu/vocab/aNumber",
            multiple=False,
            required=True,
        ),
    ]
    existence_query_properties = ("a_number",)


class MockKGObject2(KGObject):
    default_space = "mock"
    type_ = "https://openminds.ebrains.eu/mock/MockKGObject2"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "mock": "https://openminds.ebrains.eu/mock/",
    }
    properties = [Property("a", int, "https://openminds.ebrains.eu/vocab/A", multiple=False, required=True)]


class MockKGObject(KGObject):
    default_space = "mock"
    type_ = "https://openminds.ebrains.eu/mock/MockKGObject"
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "mock": "https://openminds.ebrains.eu/mock/",
    }
    properties = [
        Property(
            "a_required_string",
            str,
            "https://openminds.ebrains.eu/vocab/aRequiredString",
            multiple=False,
            required=True,
        ),
        Property(
            "a_required_list_of_strings",
            str,
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings",
            multiple=True,
            required=True,
        ),
        Property(
            "an_optional_string",
            str,
            "https://openminds.ebrains.eu/vocab/anOptionalString",
            multiple=False,
            required=False,
        ),
        Property(
            "an_optional_list_of_strings",
            str,
            "https://openminds.ebrains.eu/vocab/anOptionalListOfStrings",
            multiple=True,
            required=False,
        ),
        Property(
            "a_required_datetime",
            datetime,
            "https://openminds.ebrains.eu/vocab/aRequiredDateTime",
            multiple=False,
            required=True,
        ),
        Property(
            "a_required_list_of_datetimes",
            datetime,
            "https://openminds.ebrains.eu/vocab/aRequiredListOfDateTimes",
            multiple=True,
            required=True,
        ),
        Property(
            "an_optional_datetime",
            datetime,
            "https://openminds.ebrains.eu/vocab/anOptionalDateTime",
            multiple=False,
            required=False,
        ),
        Property(
            "an_optional_list_of_datetimes",
            datetime,
            "https://openminds.ebrains.eu/vocab/anOptionalListOfDateTimes",
            multiple=True,
            required=False,
        ),
        Property(
            "a_required_linked_object",
            ["test_base.MockKGObject", MockKGObject2],
            "https://openminds.ebrains.eu/vocab/aRequiredLinkedObject",
            multiple=False,
            required=True,
        ),
        Property(
            "a_required_list_of_linked_objects",
            ["test_base.MockKGObject", MockKGObject2],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfLinkedObjects",
            multiple=True,
            required=True,
        ),
        Property(
            "an_optional_linked_object",
            MockKGObject2,
            "https://openminds.ebrains.eu/vocab/anOptionalLinkedObject",
            multiple=False,
            required=False,
        ),
        Property(
            "an_optional_list_of_linked_objects",
            ["test_base.MockKGObject", MockKGObject2],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfLinkedObjects",
            multiple=True,
            required=False,
        ),
        Property(
            "a_required_embedded_object",
            MockEmbeddedObject,
            "https://openminds.ebrains.eu/vocab/aRequiredEmbeddedObject",
            multiple=False,
            required=True,
        ),
        Property(
            "a_required_list_of_embedded_objects",
            MockEmbeddedObject,
            "https://openminds.ebrains.eu/vocab/aRequiredListOfEmbeddedObjects",
            multiple=True,
            required=True,
        ),
        Property(
            "an_optional_embedded_object",
            MockEmbeddedObject,
            "https://openminds.ebrains.eu/vocab/anOptionalEmbeddedObject",
            multiple=False,
            required=False,
        ),
        Property(
            "an_optional_list_of_embedded_objects",
            MockEmbeddedObject,
            "https://openminds.ebrains.eu/vocab/anOptionalListOfEmbeddedObjects",
            multiple=True,
            required=False,
        ),
    ]
    existence_query_properties = (
        "a_required_string",
        "a_required_datetime",
        "a_required_linked_object",
        "a_required_embedded_object",
    )


ID_NAMESPACE = "https://kg.ebrains.eu/api/instances/"


class TestKGObject(object):
    object_counter = 0

    def _construct_embedded_object_required_properties(self, n):
        return MockEmbeddedObject(a_number=float(n))

    def _construct_object_required_properties(self):
        data = {
            "https://openminds.ebrains.eu/vocab/aRequiredDateTime": "1789-07-14T00:00:00",
            "https://openminds.ebrains.eu/vocab/aRequiredEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": -1.0,
            },
            "https://openminds.ebrains.eu/vocab/aRequiredLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002",
            },
            "https://openminds.ebrains.eu/vocab/aRequiredListOfDateTimes": [
                "1900-01-01T00:00:00",
                "2000-01-01T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 100.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 200.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": ["banana", "pear"],
            "https://openminds.ebrains.eu/vocab/aRequiredString": "apple",
        }
        return MockKGObject(
            id=f"{ID_NAMESPACE}00000000-0000-0000-0000-000000000002",
            data=data,
            a_required_string="apple",
            a_required_list_of_strings=["banana", "pear"],
            a_required_datetime=datetime(1789, 7, 14),
            a_required_list_of_datetimes=[datetime(1900, 1, 1), datetime(2000, 1, 1)],
            a_required_linked_object=MockKGObject2(
                a=1234,
                id="https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234",
            ),
            a_required_list_of_linked_objects=[
                MockKGObject2(
                    a=2345,
                    id="https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000002345",
                ),
                MockKGObject2(
                    a=3456,
                    id="https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000003456",
                ),
            ],
            a_required_embedded_object=self._construct_embedded_object_required_properties(41),
            a_required_list_of_embedded_objects=[
                self._construct_embedded_object_required_properties(42),
                self._construct_embedded_object_required_properties(43),
            ],
        )

    def _construct_object_all_properties(self):
        data = {
            "https://openminds.ebrains.eu/vocab/aRequiredDateTime": "1789-07-14T00:00:00",
            "https://openminds.ebrains.eu/vocab/aRequiredEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": -1.0,
            },
            "https://openminds.ebrains.eu/vocab/aRequiredLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002",
            },
            "https://openminds.ebrains.eu/vocab/aRequiredListOfDateTimes": [
                "1900-01-01T00:00:00",
                "2000-01-01T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 100.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 200.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": ["banana", "pear"],
            "https://openminds.ebrains.eu/vocab/aRequiredString": "apple",
            "https://openminds.ebrains.eu/vocab/anOptionalDateTime": "1605-11-05T00:00:00",
            "https://openminds.ebrains.eu/vocab/anOptionalEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": 17.0,
            },
            "https://openminds.ebrains.eu/vocab/anOptionalLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000123"
            },
            "https://openminds.ebrains.eu/vocab/anOptionalListOfDateTimes": [
                "1899-12-31T00:00:00",
                "1999-12-31T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 18.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 19.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfStrings": "plum, peach, apricot",
            "https://openminds.ebrains.eu/vocab/anOptionalString": "melon",
        }
        return MockKGObject(
            id=f"{ID_NAMESPACE}00000000-0000-0000-0000-000000000001",
            data=data,
            a_required_string="apple",
            a_required_list_of_strings=["banana", "pear"],
            an_optional_string="melon",
            an_optional_list_of_strings=["plum, peach, apricot"],
            a_required_datetime=datetime(1789, 7, 14),
            a_required_list_of_datetimes=[datetime(1900, 1, 1), datetime(2000, 1, 1)],
            an_optional_datetime=datetime(1605, 11, 5),
            an_optional_list_of_datetimes=[datetime(1899, 12, 31), datetime(1999, 12, 31)],
            a_required_linked_object=self._construct_object_required_properties(),
            a_required_list_of_linked_objects=[
                self._construct_object_required_properties(),
                self._construct_object_required_properties(),
            ],
            an_optional_linked_object=MockKGObject2(
                a=123,
                id="https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000123",
            ),
            an_optional_list_of_linked_objects=[
                MockKGObject2(
                    a=1234,
                    id="https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234",
                ),
                self._construct_object_required_properties(),
            ],
            a_required_embedded_object=self._construct_embedded_object_required_properties(-1),
            a_required_list_of_embedded_objects=[
                self._construct_embedded_object_required_properties(100),
                self._construct_embedded_object_required_properties(200),
            ],
            an_optional_embedded_object=self._construct_embedded_object_required_properties(17),
            an_optional_list_of_embedded_objects=[
                self._construct_embedded_object_required_properties(18),
                self._construct_embedded_object_required_properties(19),
            ],
        )

    def test_construct_object_all_properties(self):
        obj = self._construct_object_all_properties()
        assert obj.a_required_string == "apple"
        assert obj.an_optional_datetime == datetime(1605, 11, 5)
        assert isinstance(obj.a_required_linked_object, MockKGObject)
        assert obj.a_required_linked_object.a_required_linked_object.a == 1234
        assert obj.an_optional_list_of_embedded_objects[1].a_number == 19.0

    def test_uuid(self):
        obj = self._construct_object_required_properties()
        # this should probably be a UUID object but it"s not at present
        assert obj.uuid == "00000000-0000-0000-0000-000000000002"

    def test_build_existence_query(self):
        obj = self._construct_object_all_properties()
        expected = {
            "a_required_datetime": "1789-07-14T00:00:00",
            "a_required_embedded_object__a_number": -1.0,
            "a_required_linked_object": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002",
            "a_required_string": "apple",
        }
        assert obj._build_existence_query() == expected

    def test_build_data_all_properties(self):
        obj = self._construct_object_all_properties()
        expected = {
            "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000001",
            "@type": ["https://openminds.ebrains.eu/mock/MockKGObject"],
            "https://openminds.ebrains.eu/vocab/aRequiredDateTime": "1789-07-14T00:00:00",
            "https://openminds.ebrains.eu/vocab/aRequiredEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": -1.0,
            },
            "https://openminds.ebrains.eu/vocab/aRequiredLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002",
            },
            "https://openminds.ebrains.eu/vocab/aRequiredListOfDateTimes": [
                "1900-01-01T00:00:00",
                "2000-01-01T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 100.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 200.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": ["banana", "pear"],
            "https://openminds.ebrains.eu/vocab/aRequiredString": "apple",
            "https://openminds.ebrains.eu/vocab/anOptionalDateTime": "1605-11-05T00:00:00",
            "https://openminds.ebrains.eu/vocab/anOptionalEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": 17.0,
            },
            "https://openminds.ebrains.eu/vocab/anOptionalLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000123"
            },
            "https://openminds.ebrains.eu/vocab/anOptionalListOfDateTimes": [
                "1899-12-31T00:00:00",
                "1999-12-31T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 18.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 19.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002"},
            ],
            "https://openminds.ebrains.eu/vocab/anOptionalListOfStrings": "plum, peach, apricot",
            "https://openminds.ebrains.eu/vocab/anOptionalString": "melon",
        }
        assert obj.to_jsonld(include_empty_properties=True) == expected

    def test_modified_data(self):
        obj = self._construct_object_all_properties()
        expected = {}
        assert obj.modified_data() == expected

        obj.a_required_string = "pomme"
        obj.an_optional_list_of_embedded_objects = [
            self._construct_embedded_object_required_properties(-18),
            self._construct_embedded_object_required_properties(19),
        ]
        expected = {
            "https://openminds.ebrains.eu/vocab/aRequiredString": "pomme",
            "https://openminds.ebrains.eu/vocab/anOptionalListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": -18,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 19,
                },
            ],
        }
        assert obj.modified_data() == expected

    def test_update(self):
        obj = self._construct_object_required_properties()
        assert obj.an_optional_datetime == None
        new_data = {
            "@id": obj.id,
            "@type": obj.type_,
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": ["kumquat", "bilberry"],
            "https://openminds.ebrains.eu/vocab/anOptionalDateTime": "1789-07-14T00:00:00",
        }
        obj._update_empty_properties(new_data, client=None)
        assert obj.a_required_list_of_strings == [
            "banana",
            "pear",
        ]  # unchanged because already set
        assert obj.an_optional_datetime == datetime(1789, 7, 14)

    def test_exists__it_does_exist(self):
        orig_object = self._construct_object_required_properties()

        class MockClient:
            def instance_from_full_uri(self, id, use_cache=True, scope="in progress", require_full_data=True):
                data = orig_object.to_jsonld(include_empty_properties=True)
                data["https://core.kg.ebrains.eu/vocab/meta/space"] = "collab-foobar"
                data["@id"] = orig_object.id
                data["@context"] = orig_object.context
                data["@type"] = orig_object.type_
                return data

        MockKGObject.set_error_handling("none")  # stop the constructor from complaining
        new_obj = MockKGObject(id=orig_object.id, a_required_list_of_strings=["coconut"], an_optional_string="lime")
        MockKGObject.set_error_handling("error")
        assert new_obj.a_required_list_of_strings == ["coconut"]
        assert new_obj.remote_data == {}
        assert new_obj.a_required_embedded_object == None

        assert (
            new_obj.exists(MockClient()) and new_obj.space == "collab-foobar"
        )  # has the side-effect of setting .remote_data

        assert new_obj.a_required_embedded_object == MockEmbeddedObject(a_number=41.0)
        expected = {
            "@context": MockKGObject.context,
            "@id": orig_object.id,
            "@type": MockKGObject.type_,
            "https://core.kg.ebrains.eu/vocab/meta/space": "collab-foobar",
            "https://openminds.ebrains.eu/vocab/aRequiredDateTime": "1789-07-14T00:00:00",
            "https://openminds.ebrains.eu/vocab/aRequiredEmbeddedObject": {
                "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                "https://openminds.ebrains.eu/vocab/aNumber": 41.0,
            },
            "https://openminds.ebrains.eu/vocab/aRequiredLinkedObject": {
                "@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"
            },
            "https://openminds.ebrains.eu/vocab/aRequiredListOfDateTimes": [
                "1900-01-01T00:00:00",
                "2000-01-01T00:00:00",
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfEmbeddedObjects": [
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 42.0,
                },
                {
                    "@type": ["https://openminds.ebrains.eu/mock/MockEmbeddedObject"],
                    "https://openminds.ebrains.eu/vocab/aNumber": 43.0,
                },
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfLinkedObjects": [
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000002345"},
                {"@id": "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000003456"},
            ],
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": [
                "banana",
                "pear",
            ],  # still the same value, represents what is thought to be in the KG
            "https://openminds.ebrains.eu/vocab/aRequiredString": "apple",
        }
        assert new_obj.remote_data == expected
        assert new_obj.a_required_list_of_strings == ["coconut"]
        assert new_obj.an_optional_string == "lime"
        assert new_obj.a_required_datetime == datetime(1789, 7, 14)

        expected = {
            "https://openminds.ebrains.eu/vocab/aRequiredListOfStrings": "coconut",  # note no square brackets, single item in list. Is this desired?
            "https://openminds.ebrains.eu/vocab/anOptionalString": "lime",
        }
        assert new_obj.modified_data() == expected

    def test_exists__it_does_not_exist(self):
        pass

    def test_repr(self):
        orig_object = self._construct_object_required_properties()
        assert repr(orig_object) == (
            "MockKGObject(a_required_string='apple', a_required_list_of_strings=['banana', 'pear'], "
            "a_required_datetime=datetime.datetime(1789, 7, 14, 0, 0), "
            "a_required_list_of_datetimes=[datetime.datetime(1900, 1, 1, 0, 0), "
            "datetime.datetime(2000, 1, 1, 0, 0)], a_required_linked_object=MockKGObject2(a=1234, "
            "space=None, id=https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234), "
            "a_required_list_of_linked_objects=[MockKGObject2(a=2345, space=None, "
            "id=https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000002345), "
            "MockKGObject2(a=3456, space=None, id=https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000003456)], "
            "a_required_embedded_object=MockEmbeddedObject(a_number=41.0), "
            "a_required_list_of_embedded_objects=[MockEmbeddedObject(a_number=42.0), "
            "MockEmbeddedObject(a_number=43.0)], space=None, "
            "id=https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000000002)"
        )


def test_generate_cache_key():
    with pytest.raises(TypeError):
        generate_cache_key(None)


class TestKGProxy:
    def test_initialization_with_class(self):
        uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"
        proxy = KGProxy(MockKGObject, uri)
        assert proxy.cls is MockKGObject
        assert proxy.id == uri

    def test_initialization_with_string(self):
        uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"
        proxy = KGProxy("test_base.MockKGObject", uri)
        assert proxy.cls is MockKGObject
        assert proxy.id == uri

    def test_properties(self):
        uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"
        proxy = KGProxy(MockKGObject, uri)
        assert proxy.type == "https://openminds.ebrains.eu/mock/MockKGObject"
        assert proxy.classes == [MockKGObject]
        assert proxy.uuid == "00000000-0000-0000-0000-000000001234"

    def test_repr(self):
        uri = "https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234"
        proxy = KGProxy(MockKGObject, uri)
        assert repr(proxy) == (
            "KGProxy([<class 'test.test_base.MockKGObject'>], "
            "'https://kg.ebrains.eu/api/instances/00000000-0000-0000-0000-000000001234')"
        )
