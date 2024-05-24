from datetime import date
from uuid import uuid4
from fairgraph.base import ErrorHandling
from fairgraph.properties import Property
from fairgraph.kgobject import KGObject
from fairgraph.embedded import EmbeddedMetadata
from fairgraph.kgproxy import KGProxy
import pytest


class SomeOrganization(KGObject):
    default_space = "common"
    type_ = "https://openminds.ebrains.eu/test/Organization"
    context = {
        "vocab": "https://openminds.ebrains.eu/vocab/",
    }
    properties = [
        Property("name", str, "vocab:fullName", multiple=False, required=True),
        Property("alias", str, "vocab:shortName", multiple=False, required=False),
    ]
    reverse_properties = []
    existence_query_properties = ("name",)


class SomeAffiliation(EmbeddedMetadata):
    type_ = "https://openminds.ebrains.eu/test/Affiliation"
    context = {
        "vocab": "https://openminds.ebrains.eu/vocab/",
    }
    properties = [
        Property("end_date", date, "vocab:endDate", multiple=False, required=False),
        Property("member_of", (SomeOrganization,), "vocab:memberOf", multiple=False, required=False),
        Property("start_date", date, "vocab:startDate", multiple=False, required=False),
    ]
    reverse_properties = []


class SomeContactInformation(KGObject):
    default_space = "restricted"
    type_ = "https://openminds.ebrains.eu/test/ContactInformation"
    context = {
        "vocab": "https://openminds.ebrains.eu/vocab/",
    }
    properties = [Property("email", str, "vocab:email", multiple=False, required=True)]
    reverse_properties = []
    existence_query_properties = ("email",)


def test_serialize_embedded():
    property_embedded_metadata = Property(
        "affiliations", (SomeAffiliation,), "vocab:affiliation", multiple=True, required=False
    )

    client = None
    test_affiliation = SomeAffiliation(
        start_date=date(2023, 1, 1),
        member_of=SomeOrganization(
            name="Acme Corporation",
            alias="acme",
            id=f"https://kg.ebrains.eu/api/instances/{uuid4()}",
        ),
    )
    result = property_embedded_metadata.serialize(test_affiliation, follow_links=False)
    expected = {
        "@type": [SomeAffiliation.type_],
        "https://openminds.ebrains.eu/vocab/memberOf": {"@id": test_affiliation.member_of.id},
        "https://openminds.ebrains.eu/vocab/startDate": "2023-01-01",
    }
    assert result == expected


def test_serialize_no_multiple():
    property_no_multiple = Property(
        "contact_information",
        (SomeContactInformation,),
        "vocab:contactInformation",
        multiple=False,
        required=False,
        error_handling=ErrorHandling.error,
    )
    client = None

    # single object
    test_info = SomeContactInformation(
        email="someone@example.com", id=f"https://kg.ebrains.eu/api/instances/{uuid4()}"
    )
    result = property_no_multiple.serialize(test_info, follow_links=False)
    expected = {"@id": test_info.id}
    assert result == expected

    # single proxy
    test_info = KGProxy(SomeContactInformation, f"https://kg.ebrains.eu/api/instances/{uuid4()}")
    result = property_no_multiple.serialize(test_info, follow_links=False)
    expected = {"@id": test_info.id}
    assert result == expected

    # two objects, strict
    property_no_multiple.error_handling = ErrorHandling.error
    test_info = [
        SomeContactInformation(email="someone@example.com", id=f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
        SomeContactInformation(email="sameperson@example.com", id=f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
    ]
    with pytest.raises(ValueError):
        result = property_no_multiple.serialize(test_info, follow_links=False)

    # two objects, not strict
    property_no_multiple.error_handling = ErrorHandling.none
    test_info = [
        SomeContactInformation(email="someone@example.com", id=f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
        SomeContactInformation(email="sameperson@example.com", id=f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
    ]
    result = property_no_multiple.serialize(test_info, follow_links=False)
    expected = [{"@id": test_info[0].id}, {"@id": test_info[1].id}]
    assert result == expected

    # two proxies, not strict
    property_no_multiple.error_handling = ErrorHandling.none
    test_info = [
        KGProxy(SomeContactInformation, f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
        KGProxy(SomeContactInformation, f"https://kg.ebrains.eu/api/instances/{uuid4()}"),
    ]
    result = property_no_multiple.serialize(test_info, follow_links=False)
    expected = [{"@id": test_info[0].id}, {"@id": test_info[1].id}]
    assert result == expected


def test_deserialize():
    date_property = Property("the_date", date, "TheDate", error_handling=ErrorHandling.error)
    with pytest.raises(ValueError):
        date_property.deserialize(42, client=None)

    integer_property = Property("the_number", int, "TheNumber", error_handling=ErrorHandling.error)
    assert integer_property.deserialize(42, client=None) == 42
    assert integer_property.deserialize(42.0, client=None) == 42
    assert integer_property.deserialize("42", client=None) == 42
    assert integer_property.deserialize([42, 42, 42], client=None) == [42, 42, 42]
    assert integer_property.deserialize(["42", 42, "42"], client=None) == [42, 42, 42]

    object_property = Property("the_object", SomeOrganization, "TheObject", error_handling=ErrorHandling.error)
    obj_data = {
        "@id": "https://kg.ebrains.eu/api/instances/the_id",
        "@type": SomeOrganization.type_,
        "https://openminds.ebrains.eu/vocab/fullName": "The University",
        "https://openminds.ebrains.eu/vocab/shortName": "TU",
    }
    expected_obj = SomeOrganization(name="The University", alias="TU", id="https://kg.ebrains.eu/api/instances/the_id")
    assert object_property.deserialize(obj_data, client=None) == expected_obj

    assert object_property.deserialize(None, client=None) is None

    assert object_property.deserialize([None, obj_data, None, obj_data], client=None) == [expected_obj, expected_obj]

    assert object_property.deserialize({"@list": [None, obj_data, None, obj_data]}, client=None) == [
        expected_obj,
        expected_obj,
    ]


def test_get_filter_value():
    date_property = Property("the_date", date, "TheDate", error_handling=ErrorHandling.error)
    assert date_property.get_filter_value(date(2023, 6, 2)) == "2023-06-02"

    integer_property = Property("the_number", int, "TheNumber", error_handling=ErrorHandling.error)
    assert integer_property.get_filter_value(42) == 42

    object_property = Property("the_object", SomeOrganization, "TheObject", error_handling=ErrorHandling.error)
    obj = SomeOrganization(name="The University", alias="TU", id="https://kg.ebrains.eu/api/instances/the_id")
    assert object_property.get_filter_value(obj) == "https://kg.ebrains.eu/api/instances/the_id"
