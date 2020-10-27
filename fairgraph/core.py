"""
Metadata for entities that are used in multiple contexts (e.g. in both electrophysiology and in simulation).

"""

# Copyright 2018-2019 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import unicode_literals
import sys
import inspect
import logging
try:
    basestring
except NameError:
    basestring = str
from datetime import date, datetime
from dateutil import parser as date_parser
from .base import KGObject, KGProxy, KGQuery, cache, as_list, Field
from .errors import ResourceExistsError
from .commons import Address, Species, Strain, Genotype, Sex, Age, QuantitativeValue, Handedness, Group

DEFAULT_NAMESPACE = None
# core is used everywhere, so it makes no sense to set a default namespace
# the namespace to be used in a given context should be set using "use_namespace()"


logger = logging.getLogger("fairgraph")

class Subject(KGObject):
    """The individual organism that is the subject of an experimental study."""
    namespace = DEFAULT_NAMESPACE
    _path = "/core/subject/v0.1.2"
    type = ["nsg:Subject", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "prov": "http://www.w3.org/ns/prov#",
        "name": "schema:name",
        "value": "schema:value",
        "minValue": "schema:minValue",
        "maxValue": "schema:maxValue",
        "unitCode": "schema:unitCode",
        "label": "rdfs:label",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "species": "nsg:species",  # change from nsg:species to "http://dbpedia.org/ontology/Species" ?
        "strain": "nsg:strain",
        "age": "nsg:age",  # change from nsg:age to "http://dbpedia.org/ontology/age" ?
        "period": "nsg:period",
        "sex": "nsg:sex",
        "genotype": "nsg:genotype",
        "handedness": "nsg:handedness",
        "deathDate": "schema:deathDate",
	"group": "nsg:group",
        "providerId": "nsg:providerId"
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("species", Species, "species", required=True),
        Field("strain", Strain, "strain"),
        Field("genotype", Genotype, "genotype"),
        Field("sex", Sex, "sex"),
        Field("handedness", Handedness, "handedness"),
        Field("age", Age, "age"),
        Field("death_date", date, "deathDate"),
	Field("group", Group, "group")
    )

    def __init__(self, name, species, age=None, sex=None, handedness=None, strain=None, genotype=None, death_date=None, group=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class Organization(KGObject):
    """
    An organization associated with research data or models, e.g. a university, lab or department.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/core/organization/v0.1.0"
    type = ["nsg:Organization"]
    context = {
        "schema": "http://schema.org/",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "parentOrganization": "schema:parentOrganization",
        "address": "schema:address",
        "addressLocality": "schema:addressLocality",
        "addressCountry": "schema:addressCountry",
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("address", Address, "address"),
        Field("parent", "core.Organization", "parentOrganization")
    )

    def __init__(self, name, address=None, parent=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class Person(KGObject):
    """
    A person associated with research data or models, for example as an experimentalist,
    or a data analyst.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/core/person/v0.1.0"
    type = ["nsg:Person", "prov:Agent"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "familyName": "schema:familyName",
        "givenName": "schema:givenName",
        "email": "schema:email",
        "affiliation": "schema:affiliation"
    }
    fields = (
        Field("family_name", basestring, "familyName", required=True, doc="Family name / surname"),
        Field("given_name", basestring, "givenName", required=True, doc="Given name"),
        Field("email", basestring, "email", doc="e-mail address"),
        Field("affiliation", Organization, "affiliation",
              doc="Organization to which person belongs")
    )
    existence_query_fields = ("family_name", "given_name")

    def __init__(self, family_name, given_name, email=None,
                 affiliation=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    @property
    def full_name(self):
        return '{self.given_name} {self.family_name}'.format(self=self)

    @classmethod
    def list(cls, client, size=100, api="query", scope="released", resolved=False, **filters):
        """List all objects of this type in the Knowledge Graph"""
        if api == 'nexus':
            context = {
                "schema": "http://schema.org/"
            }
            filter_queries = []
            for name, value in filters.items():
                if name in ("first_name", "given_name"):
                    filter_queries.append({
                        'path': 'schema:givenName',
                        'op': 'eq',
                        'value': value
                    })
                elif name in ("family_name", "last_name", "surname"):
                    filter_queries.append({
                        "path": "schema:familyName",
                        "op": "eq",
                        "value": value
                    })
                elif name == "email":
                    filter_queries.append({
                        "path": "schema:email",
                        "op": "eq",
                        "value": value
                    })
                else:
                    raise ValueError(
                        "The only supported filters are by first (given) name, "
                        "last (family) name or email. You specified {name}".format(name=name))
            if len(filter_queries) == 0:
                return client.list(cls, size=size)
            elif len(filter_queries) == 1:
                filter_query = filter_queries[0]
            else:
                filter_query = {
                    "op": "and",
                    "value": filter_queries
                }
            filter_query = {"nexus": filter_query}
            return KGQuery(cls, filter_query, context).resolve(client, api="nexus", size=size)
        elif api == "query":
            return super(Person, cls).list(client, size=size, api=api,
                                           scope=scope, resolved=resolved, **filters)
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")

    def resolve(self, client, api="query", use_cache=True):
        if hasattr(self.affiliation, "resolve"):
            self.affiliation = self.affiliation.resolve(client, api=api, use_cache=use_cache)
        return self

    @classmethod
    def me(cls, client, api="query", allow_multiple=False):
        """Return the Person who is currently logged-in.

        (the user associated with the token stored in the client).

        If the Person node does not exist in the KG, it will be created.
        """
        user_info = client.user_info()
        given_name = user_info["givenName"]
        family_name = user_info["familyName"]
        email = [entry["value"] for entry in user_info["emails"] if entry["primary"]][0]
        # first look for a node that matches name and primary email
        people = Person.list(client, api=api, scope="latest", family_name=family_name,
                             given_name=given_name, email=email, resolved=False)
        # if we don't find a node, try to match by any email
        if not people:
            for entry in user_info["emails"]:
                people.extend(Person.list(client, api=api, scope="latest", email=entry["value"],
                                          resolved=False))
        # if we still don't find a node, try to match by name
        if not people:
            people = Person.list(client, api=api, scope="latest", family_name=family_name,
                                 given_name=given_name, resolved=False)
        # otherwise, create a new node
        if people:
            if isinstance(people, list):
                if len(people) > 1:
                    if allow_multiple:
                        return people
                    else:
                        raise Exception("Found multiple entries. "
                                        "Use the 'allow_multiple' option to avoid this error.")
                else:
                    people = people[0]
            return people
        else:
            person = Person(family_name=family_name, given_name=given_name, email=email)
            # todo: add linked organization based on user_info affiliation
            person.save(client)
            return person


class Protocol(KGObject):
    """
    An experimental protocol.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/core/protocol/v0.1.0"
    type = ["nsg:Protocol", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "prov": "http://www.w3.org/ns/prov#"
    }

    def __init__(self, name, steps, materials, author,
                 date_published, identifier, id=None, instance=None):
        self.name = name
        self.steps = steps
        self.materials = materials
        self.author = author
        self.date_published = date_published
        self.identifier = identifier
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.identifier!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, resolved=False):
        """docstring"""
        D = instance.data
        assert 'nsg:Protocol' in D["@type"]
        return cls(D["name"],
                   D["nsg:steps"],
                   [Material.from_jsonld(material) for material in D["nsg:materials"]],
                   KGProxy(Person, D["schema:author"]),
                   D["schema:datePublished"],
                   KGProxy(Identifier, D["schema:identifier"]),
                   D["@id"], instance=instance)

    def _build_data(self, client, all_fields=False):
        """docstring"""
        data = {}
        data["name"] = self.name
        data["nsg:steps"] = self.steps
        if self.materials:
            data["nsg:materials"] = [material.to_jsonld() for material in self.materials]
        if self.author:
            if self.author.id is None:
                self.author.save(client)
            data["schema:author"] = {
                "@type": self.author.type,
                "@id": self.author.id
            }
        if self.date_published:
            data["schema:datePublished"] = self.date_published
        if self.identifier:
            if self.identifier.id is None:
                self.identifier.save(client)
            data["schema:identifier"] = {
                "@type": self.identifier.type,
                "@id": self.identifier.id
            }
        return data


class Identifier(KGObject):
    namespace = "nexus"
    _path = "/schemaorgsh/identifier/v0.1.0"
    type = ["schema:Identifier"]


class Material(object):
    """Metadata about a chemical product or other material used in an experimental protocol."""

    def __init__(self, name, molar_weight, formula, stock_keeping_unit, identifier, vendor):
        self.name = name
        self.molar_weight = molar_weight
        self.formula = formula
        self.stock_keeping_unit = stock_keeping_unit
        self.identifier = identifier
        self.vendor = vendor

    def to_jsonld(self, client=None):
        return {
            "nsg:reagentName": self.name,
            "nsg:reagentMolarWeight": self.molar_weight.to_jsonld(),
            "nsg:reagentLinearFormula": self.formula,
            "schema:sku": self.stock_keeping_unit,
            "schema:identifier": {
                "@id": self.identifier.id,
            },
            "nsg:reagentVendor": {
                "@type": self.vendor.type,
                "@id": self.vendor.id
            }
        }

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        return cls(data["name"],
                   QuantitativeValue.from_jsonld(data["nsg:reagentMolarWeight"]),
                   data["nsg:reagentLinearFormula"],
                   data["schema:sku"],
                   KGProxy(Identifier, data["schema:identifier"]["@id"]),
                   KGProxy(Organization, data["nsg:reagentVendor"]["@id"]))


class Collection(KGObject):
    """A collection of other metadata objects"""
    namespace = DEFAULT_NAMESPACE
    _path = "/core/collection/v0.1.0"
    type = ["nsg:Collection", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "size": "schema:size",
        "hadMember": "prov:hadMember"
    }
    fields = (
        Field("name", basestring, "name", required=True),
        Field("members", KGObject, "hadMember", required=True, multiple=True)
    )

    def __init__(self, name, members, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    @property
    def size(self):
        return len(as_list(self.members))

    # def __repr__(self):
    #     return ('{self.__class__.__name__}('
    #             '{self.name!r}, {self.size!r}, {self.id})'.format(self=self))

    # @classmethod
    # @cache
    # def from_kg_instance(cls, instance, client, resolved=False):
    #     """
    #     docstring
    #     """
    #     D = instance.data
    #     for otype in cls.type:
    #         assert otype in D["@type"]

    #     return cls(name=D["name"],
    #                members=[KGProxy(None, member_uri["@id"])
    #                         for member_uri in D["hadMember"]],
    #                id=D["@id"],
    #                instance=instance)

    def _build_data(self, client, all_fields=False):
        """docstring"""
        data = {}
        data["name"] = self.name
        data["size"] = len(as_list(self.members))
        data["hadMember"] = [{
            "@type": member.type,
            "@id": member.id
        } for member in as_list(self.members)]
        return data


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
            if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]


def use_namespace(namespace):
    """Set the namespace for all classes in this module."""
    for cls in list_kg_classes():
        cls.namespace = namespace
