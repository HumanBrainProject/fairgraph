"""
core

"""

from __future__ import unicode_literals
import logging
from .base import KGObject, KGProxy, cache, as_list
from .errors import ResourceExistsError
from .commons import Address, Species, Strain, Sex, Age, QuantitativeValue

#NAMESPACE = "neuralactivity"
NAMESPACE = "neurosciencegraph"
#NAMESPACE = "brainsimulation"

logger = logging.getLogger("fairgraph")


class Subject(KGObject):
    """docstring"""
    path = NAMESPACE + "/core/subject/v0.1.0"
    type = ["nsg:Subject", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "prov": "http://www.w3.org/ns/prov#",
        "name": "schema:name",
        "value": "schema:value",
        "unitCode": "schema:unitCode",
        "label": "rdfs:label",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "species": "nsg:species",  # change from nsg:species to "http://dbpedia.org/ontology/Species" ?
        "strain": "nsg:strain",
        "age": "nsg:age",  # change from nsg:age to "http://dbpedia.org/ontology/age" ?
        "period": "nsg:period",
        "sex": "nsg:sex",
        "deathDate": "schema:deathDate",
        "providerId": "nsg:providerId"
    }

    def __init__(self, name, species, strain, sex, age, death_date, id=None, instance=None):
        self.name = name
        self.species = species
        self.strain = strain
        self.sex = sex
        self.age = age
        self.death_date = death_date
        self.id = id
        self.instance = instance

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.name!r}, {self.species!r}, {self.strain!r}, {self.sex!r}, '
        #        f'{self.age!r}, {self.death_date!r}, {self.id})')
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.species!r}, {self.strain!r}, {self.sex!r}, '
                '{self.age!r}, {self.death_date!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        """docstring"""
        D = instance.data
        assert 'nsg:Subject' in D["@type"]
        return cls(D["name"],
                   Species.from_jsonld(D["species"]),
                   Strain.from_jsonld(D.get("strain", None)),
                   Sex.from_jsonld(D["sex"]),
                   Age.from_jsonld(D["age"]),
                   D.get("deathDate", None), D["@id"],
                   instance=instance)

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        data["providerId"] = self.name
        data["species"] = self.species.to_jsonld()
        if self.strain:
            data["strain"] = self.strain.to_jsonld()
        if self.age:
            data["age"] = self.age.to_jsonld()
        if self.sex:
            data["sex"] = self.sex.to_jsonld()
        if self.death_date:
            data["deathDate"] = self.death_date
        return data


class Organization(KGObject):
    """docstring"""
    path = NAMESPACE + "/core/organization/v0.1.0"
    type = "nsg:Organization"
    context = {
        "schema": "http://schema.org/",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "parentOrganization": "schema:parentOrganization",
        "address": "schema:address",
        "addressLocality": "schema:addressLocality",
        "addressCountry": "schema:addressCountry",
    }

    def __init__(self, name, address=None, parent=None, id=None, instance=None):
        self.name = name
        self.address = address
        self.parent = parent
        self.id = id
        self.instance = instance

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.name!r}, {self.address!r}, {self.parent}, {self.id})')
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.address!r}, {self.parent}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        """docstring"""
        D = instance.data
        assert 'nsg:Organization' in D["@type"]
        if "parentOrganization" in D:
            parent = KGProxy(cls, D["parentOrganization"]["@id"])
        else:
            parent = None
        if "address" in D:
            address = Address(D["address"]["addressLocality"], D["address"]["addressCountry"])
        else:
            address = None
        return cls(D["name"], address, parent, id=D["@id"], instance=instance)

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.address:
            data["address"] = {
                "@type": "schema:PostalAddress",
                "addressLocality": self.address.locality,
                "addressCountry": self.address.country
            }
        if self.parent:
            if self.parent.id is None:
                self.parent.save(client)
            data["parent"] = {
                "@type": self.parent.type,
                "@id": self.parent.id
            }
        return data


class Person(KGObject):
    """docstring"""
    path = NAMESPACE + "/core/person/v0.1.0"
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

    def __init__(self, family_name, given_name, email, affiliation=None, id=None, instance=None):
        self.family_name = family_name
        self.given_name = given_name
        self.email = email
        self.affiliation = affiliation
        self.id = id
        self.instance = instance

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.family_name!r}, {self.given_name!r}, {self.email}, {self.id})')
        return ('{self.__class__.__name__}('
                '{self.family_name!r}, {self.given_name!r}, {self.email}, {self.id})'.format(self=self))

    @property
    def full_name(self):
        return '{self.given_name} {self.family_name}'.format(self=self)

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        """docstring"""
        D = instance.data
        assert 'nsg:Person' in D["@type"]
        if "affiliation" in D:
            affiliation = KGProxy(Organization, D["affiliation"]["@id"])
        else:
            affiliation = None
        return cls(D["familyName"], D["givenName"], D.get("email", None),
                   affiliation, D["@id"], instance=instance)

    @property
    def _existence_query(self):
        return {
            "op": "and",
            "value": [
                {
                    "path": "schema:familyName",
                    "op": "eq",
                    "value": self.family_name
                },
                {
                    "path": "schema:givenName",
                    "op": "eq",
                    "value": self.given_name
                }
            ]
        }

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["familyName"] = self.family_name
        data["givenName"] = self.given_name
        if self.email:
            data["email"] = self.email
        if self.affiliation:
            if self.affiliation.id is None:
                self.affiliation.save(client)
            data["affiliation"] = {
                "@type": self.affiliation.type,
                "@id": self.affiliation.id
            }
        return data

    def resolve(self, client):
        if hasattr(self.affiliation, "resolve"):
            self.affiliation = self.affiliation.resolve(client)


class Protocol(KGObject):
    path = NAMESPACE + "/core/protocol/v0.1.0"
    type = ["nsg:Protocol", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "prov": "http://www.w3.org/ns/prov#"
    }

    def __init__(self, name, steps, materials, author, date_published, identifier, id=None, instance=None):
        self.name = name
        self.steps = steps
        self.materials = materials
        self.author = author
        self.date_published = date_published
        self.identifier = identifier
        self.id = id
        self.instance = instance

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.identifier!r}, {self.id})')
        return ('{self.__class__.__name__}('
                '{self.identifier!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
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

    def _build_data(self, client):
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
    path = "nexus/schemaorgsh/identifier/v0.1.0/"
    type = "schema:Identifier"


class Material(object):

    def __init__(self, name, molar_weight, formula, stock_keeping_unit, identifier, vendor):
        self.name = name
        self.molar_weight = molar_weight
        self.formula = formula
        self.stock_keeping_unit = stock_keeping_unit
        self.identifier = identifier
        self.vendor = vendor

    def to_jsonld(self):
        return {
            "nsg:reagentName": self.name,
            "nsg:reagentMolarWeight": self.molar_weight.to_jsonld(),
            "nsg:reagentLinearFormula": self.formula,
            "schema:sku": self.stock_keeping_unit,
            "schema:identifier": {
                #"@type": "",
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
    """docstring"""
    path = NAMESPACE + "/core/collection/v0.1.0"
    type = ["nsg:Collection", "prov:Entity"]
    context = {
        "schema": "http://schema.org/",
        "prov": "http://www.w3.org/ns/prov#",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "name": "schema:name",
        "size": "schema:size",
        "hadMember": "prov:hadMember"
    }

    def __init__(self, name, members, id=None, instance=None):
        self.name = name
        self.members = members
        self.id = id
        self.instance = instance

    @property
    def size(self):
        return len(as_list(self.members))

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.size!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        """
        docstring
        """
        D = instance.data
        for otype in cls.type:
            assert otype in D["@type"]

        return cls(name=D["name"],
                   members=[KGProxy(None, member_uri["@id"])
                            for member_uri in D["hadMember"]],
                   id=D["@id"],
                   instance=instance)

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        data["size"] = len(as_list(self.members))
        data["hadMember"] = [{
            "@type": member.type,
            "@id": member.id
        } for member in as_list(self.members)]
        return data
