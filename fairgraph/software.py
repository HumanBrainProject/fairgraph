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


import sys
import logging
import datetime
import inspect
try:
    basestring
except NameError:
    basestring = str
from dateutil import parser as date_parser

from .base import (KGObject, cache, KGProxy, build_kg_object, Distribution, as_list, KGQuery,
                   OntologyTerm, IRI, Field)
from .core import Organization, Person
from .commons import License, Language

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


class SoftwareFeatureCategory(KGObject):
    """A grouping of related software features"""
    namespace = DEFAULT_NAMESPACE
    _path = "/software/softwarefeaturecategory/v1.0.0"
    type = ["prov:Entity", "nsg:SoftwareFeatureCategory"]
    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }
    fields = (
        Field("name", basestring, "schema:name", required=True),
        Field("description", basestring, "schema:description"),
        Field("features", "software.SoftwareFeature", "schema:feature", multiple=True),
    )

    def __init__(self, name, description=None, features=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class SoftwareFeature(KGObject):
    """Functionality provided by a piece of software"""
    namespace = DEFAULT_NAMESPACE
    _path = "/software/softwarefeature/v1.0.0"
    type = ["prov:Entity", "nsg:SoftwareFeature"]
    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }
    fields = (
        Field("name", basestring, "schema:name", required=True),
        Field("description", basestring, "schema:description"),
        Field("category", SoftwareFeatureCategory, "schema:feature", multiple=True),
    )

    def __init__(self, name, description=None, category=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class SoftwareProject(KGObject):
    """A grouping of different versions of a given piece of software"""
    namespace = DEFAULT_NAMESPACE
    _path = "/software/softwareproject/v1.0.0"
    type = ["prov:Entity", "nsg:SoftwareProject"]
    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/"
    }
    fields = (
        Field("name", basestring, "schema:name", required=True),
        Field("description", basestring, "schema:description"),
        Field("instances", "software.Software", "schema:instance", multiple=True)
    )

    def __init__(self, name, description=None, instances=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, '
                '{self.id})'.format(self=self))


class Software(KGObject):
    """A specific release or version of a piece of software"""
    namespace = DEFAULT_NAMESPACE
    _path = "/software/software/v1.0.0"
    type = ["prov:Entity", "nsg:Software"]
    context = {
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/",
        # "name"
        # "version"
        # description
        # citation
        # license
        # dateCreated
        # wasRevisionOf
        # author
        # project
        # image
        # applicationCategory
        # applicationSubCategory
    }
    fields = (
        Field("name", basestring, "schema:name", required=True),
        Field("version", basestring, "schema:version", required=True),
        Field("providerId", basestring, "schema:providerId"),
        Field("summary", basestring, "schema:headline"),
        Field("description", basestring, "schema:description"),
        Field("citation", basestring, "schema:citation"),
        Field("license", License, "schema:license", multiple=True),
        Field("release_date", datetime.date, "schema:dateCreated"),  # use prov?
        Field("previous_version", "software.Software", "prov:wasRevisionOf"),
        Field("authors", Person, "schema:author", multiple=True),
        Field("project", SoftwareProject, "schema:project"),
        Field("image", IRI, "schema:image"),
        Field("categories", SoftwareCategory, "schema:applicationCategory", multiple=True),
        Field("subcategories", SoftwareCategory, "schema:applicationSubCategory", multiple=True),
        Field("operating_system", OperatingSystem, "schema:operatingSystem", multiple=True),
        Field("release_notes", basestring, "schema:releaseNotes"),  # or use IRI?
        Field("screenshots", IRI, "schema:screenshot", multiple=True),
        Field("requirements", basestring, "schema:requirements"),
        Field("headline", basestring, "schema:headline"),
        Field("copyright", Organization, "schema:copyrightHolder", multiple=True),
        Field("components", "software.Software", "schema:hasPart", multiple=True),
        Field("part_of", "software.Software", "schema:partOf", multiple=True),
        Field("funding", Organization, "schema:funder", multiple=True),
        Field("programming_language", ProgrammingLanguage, "schema:encodingFormat", multiple=True),
        Field("features", SoftwareFeature, "schema:feature", multiple=True),
        Field("keywords", basestring, "schema:keywords", multiple=True),  # use Keyword class
        Field("is_free", bool, "schema:isAccessibleForFree"),
        Field("homepage", IRI, "schema:url"),
        Field("documentation", IRI, "schema:documentation"),
        Field("help", IRI, "schema:support"),
        Field("code", IRI, "schema:code"),
        Field("devices", Device, "schema:device", multiple=True),
        Field("languages", Language,"schema:language", multiple=True),
        # input_format
        # output_format
        # application category
    )

    def __init__(self, name, version, providerId=None, description=None, summary=None, identifier=None,
                 citation=None, license=None, release_date=None, previous_version=None,
                 authors=None, project=None, image=None, categories=None, subcategories=None,
                 operating_system=None, release_notes=None, screenshots=None, requirements=None, headline=None, copyright=None,
                 programming_language=None, components=None, part_of=None,
                 funding=None, languages=None, features=None, keywords=None, is_free=None,
                 homepage=None, documentation=None, help=None, code=None, devices=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    def _build_data(self, client):
        """docstring"""
        data = super(Software, self)._build_data(client)
        if self.release_date:
            data["schema:copyrightYear"] = self.release_date.year
        return data


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
            if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]


def use_namespace(namespace):
    """Set the namespace for all classes in this module."""
    for cls in list_kg_classes():
        cls.namespace = namespace
