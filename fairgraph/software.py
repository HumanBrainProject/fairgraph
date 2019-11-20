# encoding: utf-8
"""
Metadata about, or related to, software
"""

# Copyright 2018-2019 CNRS and Universität Trier

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
import datetime
from dateutil import parser as date_parser

from .base import KGObject, cache, KGProxy, build_kg_object, Distribution, as_list, KGQuery, OntologyTerm
from .core import Organization, Person
from .commons import License

logger = logging.getLogger("fairgraph")

DEFAULT_NAMESPACE = "softwarecatalog"


class SoftwareCategory(OntologyTerm):
    iri_map = {
        "application": "https://www.wikidata.org/wiki/Q166142",
        "plug-in": "https://www.wikidata.org/wiki/Q184148"
    }


class OperatingSystem(OntologyTerm):
    iri_map = {
        "Linux": "http://dbpedia.org/resource/Linux",
        "MacOS": "http://dbpedia.org/resource/MacOS",
        "Windows": "http://dbpedia.org/resource/Microsoft_Windows",
        "Windows XP": "http://dbpedia.org/resource/Windows_XP",
        "Windows Vista": "http://dbpedia.org/resource/Windows_Vista",
        "Windows 7": "http://dbpedia.org/resource/Windows_7",
        "Windows 10": "http://dbpedia.org/resource/Windows_10"
    }


class ProgrammingLanguage(OntologyTerm):
    iri_map = {
        "Python": "https://www.wikidata.org/wiki/Q28865",
        "C++": "https://www.wikidata.org/wiki/Q2407",
        "C": "https://www.wikidata.org/wiki/Q15777",
        "Java": "https://www.wikidata.org/wiki/Q251",
        "Perl": "https://www.wikidata.org/wiki/Q42478",
        "Javascript": "https://www.wikidata.org/wiki/Q2005"
    }


class Device(OntologyTerm):
    iri_map = {
        "Mobile": "https://www.wikidata.org/wiki/Q5082128",
        "Desktop Computer": "https://www.wikidata.org/wiki/Q56155"
    }

class Language(OntologyTerm):
    iri_map = {
        "English": "https://www.wikidata.org/wiki/Q1860",
        "German": "https://www.wikidata.org/wiki/Q188"
    }


class Software(KGObject):
    namespace = DEFAULT_NAMESPACE
    _path = "/software/software/v0.1.2"
    type = ["prov:Entity", "nsg:Software"]

    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }

    def __init__(self, name, version, providerId=None, summary=None, description=None, identifier=None,
                 citation=None, license=None, release_date=None, previous_version=None,
                 authors=None, project=None, image=None, categories=None, subcategories=None,
                 operating_system=None, release_notes=None, screenshots=None, requirements=None, headline=None, copyright=None,
                 programmingLanguage=None, components=None, part_of=None,
                 funding=None, languages=None, features=None, keywords=None, is_free=None,
                 homepage=None, documentation=None, help=None, code=None, devices=None, id=None, instance=None):
        self.name = name
        self.version = version
        self.providerId = providerId
        self.description = description
        self.identifier = identifier
        self.citation = citation
        self.license = license
        self.release_date = release_date
        self.previous_version = previous_version
        self.authors = authors
        self.project = project
        self.image = image
        self.categories = categories
        self.subcategories = subcategories
        self.operating_system = operating_system
        self.release_notes = release_notes
        self.screenshots = screenshots
        self.requirements = requirements
        self.headline = headline
        self.copyright = copyright
        self.programmingLanguage = programmingLanguage
        self.components = components
        self.part_of = part_of
        self.funding = funding
        self.languages = languages
        self.features = features
        self.keywords = keywords
        self.is_free = is_free
        self.homepage = homepage
        self.documentation = documentation
        self.help = help
        self.code = code
        self.devices = devices
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.version!r}, '
                '{self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True, resolved=False):
        D = instance.data
        assert 'nsg:Software' in D["@type"]
        obj = cls(name=D["schema:name"],
                  version=D["schema:version"],
                  providerId=D.get("schema:providerId"),
                  description=D.get("schema:description"),
                  #identifier=build_kg_object(Identifier, D .get("schema:identifier")),  # todo: implement commons.Identifier
                  citation=D.get("schema:citation"),
                  license=build_kg_object(License, D.get("schema:license")),
                  release_date=date_parser.parse(D.get("schema:dateCreated"))
                               if "schema:dateCreated" in D else None,
                  previous_version=build_kg_object(Software, D.get("prov:wasRevisionOf")),
                  authors=build_kg_object(Person, D.get("schema:author")),
                  project=build_kg_object(SoftwareProject, D.get("schema:project")),  # todo: add link to SoftwareProject to schema?
                  image=D["schema:image"]["@id"] if "schema:image" in D else None,
                  categories=build_kg_object(SoftwareCategory, D.get("schema:applicationCategory")),
                  subcategories=build_kg_object(SoftwareCategory, D.get("schema:applicationSubCategory")),
                  operating_system=build_kg_object(OperatingSystem, D.get("schema:operatingSystem")),
                  release_notes=D.get("schema:releaseNotes"),  # should probably contain ["@id"] ?
                  screenshots=D["schema:screenshot"]["@id"] if "schema:screenshot" in D else None,
                  requirements=D.get("schema:requirements"),
                  headline=D.get("schema:headline"),
                  copyright=build_kg_object(Organization, D.get("schema:copyrightHolder")),
                  components=build_kg_object(Software, D.get("schema:hasPart")),
                  part_of=build_kg_object(Software, D.get("schema:partOf")),
                  funding=build_kg_object(Organization, D.get("schema:funder")),
                  programmingLanguage=build_kg_object(ProgrammingLanguage, D.get("schema:programmingLanguage")),
                  features=build_kg_object(SoftwareFeature, D.get("schema:feature")),  # todo: implement SoftwareFeature
                  keywords=D.get("schema:keywords"),
                  is_free=D.get("schema:isAccessibleForFree"),
                  homepage=D["schema:url"]["@id"] if "schema:url" in D else None,
                  documentation=D["schema:documentation"]["@id"] if "schema:documentation" in D else None,
                  help=D["schema:help"]["@id"] if "schema:help" in D else None,
                  code=D["schema:code"]["@id"] if "schema:code" in D else None,
                  devices=build_kg_object(Device, D.get("schema:device")),
                  languages=build_kg_object(Language,D.get("schema:language")),
                  id=D.get("@id"),
                  instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["schema:name"] = self.name
        data["schema:version"] = self.version
        if self.providerId:
            data["schema:providerId"] = self.providerId
        if self.description:
            data["schema:description"] = self.description
        if self.identifier:
            data["schema:identifier"] = self.identifier.to_jsonld()
        if self.citation:
            data["schema:citation"] = self.citation
        if self.license:
            data["schema:license"] = self.license.to_jsonld()
        if self.release_date:
            data["schema:dateCreated"] = self.release_date.isoformat()
            data["schema:copyrightYear"] = self.release_date.year
        if self.previous_version:
            data["prov:wasRevisionOf"] = {
                "@id": self.previous_version.id,
                "@type": self.previous_version.type
            }
        if self.authors:
            data["schema:author"] = [{
                    "@id": person.id,
                    "@type": person.type
                } for person in as_list(self.authors)]
        if self.image:
            data["schema:image"] = {"@id": self.image}
        if self.categories:
            data["schema:applicationCategory"] = [cat.to_jsonld() for cat in as_list(self.categories)]
        if self.subcategories:
            data["schema:applicationSubCategory"] = [cat.to_jsonld() for cat in as_list(self.subcategories)]
        if self.operating_system:
            data["schema:operatingSystem"] = [os.to_jsonld()
                                              for os in as_list(self.operating_system)]
        if self.release_notes:
            data["schema:releaseNotes"] = self.release_notes
        if self.screenshots:
            data["schema:screenshot"] = {"@id": self.screenshots}
        if self.requirements:
            data["schema:requirements"] = self.requirements
        if self.headline:
            data["schema:headline"] = self.headline
        if self.copyright:
            data["schema:copyrightHolder"] = {
                "@id": self.copyright.id,
                "@type": self.copyright.type
            }
        if self.components:
            data["schema:hasPart"] = [{
                    "@id": part.id,
                    "@type": part.type
                } for part in as_list(self.components)]
        if self.part_of:
            data["schema:partOf"] = [{
                    "@id": parent.id,
                    "@type": parent.type
                } for parent in as_list(self.part_of)]
        if self.funding:
            data["schema:funder"] = [{
                    "@id": org.id,
                    "@type": org.type
                } for org in as_list(self.funding)]
        if self.programmingLanguage:
            data["schema:programmingLanguage"] = [lang.to_jsonld() for lang in as_list(self.programmingLanguage)]
        if self.features:
            data["schema:feature"] = [{
                    "@id": feature.id,
                    "@type": feature.type
                } for feature in as_list(self.features)]
        if self.keywords:
            data["schema:keywords"] = self.keywords
        if self.is_free:
            data["schema:isAccessibleForFree"] = self.is_free
        if self.homepage:
            data["schema:url"] = {"@id": self.homepage}
        if self.documentation:
            data["schema:documentation"] = {"@id": self.documentation}
        if self.help:
            data["schema:help"] = {"@id": self.help}
        if self.code:
            data["schema:code"] = {"@id": self.code}
        if self.devices:
            data["schema:device"] = [dev.to_jsonld() for dev in as_list(self.devices)]
        if self.project:
            data["schema:project"] = {
                "@id": self.project.id,
                "@type": self.project.type
            }
        if self.languages:
            [lang.to_jsonld() for lang in as_list(self.languages)]
        return data


class SoftwareFeature(KGObject):
    path = NAMESPACE + "/software/softwarefeature/v0.1.1"
    type = ["prov:Entity", "nsg:SoftwareFeature"]

    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }

    def __init__(self, name,description=None, feature=None, id=None, instance=None):
        self.name = name
        self.description = description
        self.feature = feature
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, '
                '{self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:SoftwareFeature' in D["@type"]
        obj = cls(name=D["schema:name"],
                  description=D.get("schema:description"),
                  feature=build_kg_object(SoftwareFeature, D.get("schema:feature")),
                  id=D.get("@id"),
                  instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["schema:name"] = self.name
        if self.feature:
            data["schema:feature"] = self.feature
        if self.description:
            data["schema:description"] = self.description

        return data


class SoftwareFeatureCategory(KGObject):
    path = NAMESPACE + "/software/softwarefeaturecategory/v0.1.1"
    type = ["prov:Entity", "nsg:SoftwareFeatureCategory"]

    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }

    def __init__(self, name, description=None, features=None, id=None, instance=None):
        self.name = name
        self.features = features
        self.description = description
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, '
                '{self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:SoftwareFeatureCategory' in D["@type"]
        obj = cls(name=D["schema:name"],
                  description=D.get("schema:description"),
                  features=(build_kg_object(SoftwareCategory, D["schema:feature"]) if D["schema:feature"][0]["@type"] == "nsg:SoftwareFeature" else build_kg_object(SoftwareFeatureCategory, D["schema:feature"])) if "schema:feature" in D else None,
                  id=D.get("@id"),
                  instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["schema:name"] = self.name
        if self.features:
            data["schema:feature"] = [{
                    "@id": feature.id,
                    "@type": feature.type
                } for feature in as_list(self.features)]

        if self.description:
            data["schema:description"] = self.description

        return data


class SoftwareProject(KGObject):
    path = NAMESPACE + "/software/softwareproject/v0.1.0"
    type = ["prov:Entity", "nsg:SoftwareProject"]

    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }

    def __init__(self, name, description=None, instances=None, id=None, instance=None):
        self.name = name
        self.description = description
        self.instances = instances
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, '
                '{self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:SoftwareProject' in D["@type"]
        obj = cls(name=D["schema:name"],
                  description=D.get("schema:description"),
                  instances=build_kg_object(Software, D.get("schema:instance")),
                  id=D.get("@id"),
                  instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["schema:name"] = self.name
        if self.instances:
            data["schema:instance"] = [{
                "@id": instance.id,
                "@type": instance.type
            } for instance in as_list(self.instances)]
        if self.description:
            data["schema:description"] = self.description

        return data


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
            if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]


def use_namespace(namespace):
    """Set the namespace for all classes in this module."""
    for cls in list_kg_classes():
        cls.namespace = namespace
