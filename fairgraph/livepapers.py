"""
Metadata for Live Papers.

"""

# Copyright 2021 CNRS

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
from .base import KGObject, Distribution, HasAliasMixin
from .fields import Field
from datetime import datetime, date
from .core import Person
from .commons import License


logger = logging.getLogger("fairgraph")

DEFAULT_NAMESPACE = "modelvalidation"


class LivePaperResourceItem(KGObject):
    """
    Individual resource items in a Live Paper resource section.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/livepapers/resourceitem/v0.1.1"
    type = ["prov:Entity", "nsg:Entity", "nsg:LivePaperResourceItem"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "schema": "http://schema.org/",
            "name": "schema:name",
            "url": "schema:url",
            "identifier": "schema:identifier",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "partOf": "nsg:partOf"
        }
    ]
    fields = (
        Field("distribution", Distribution, "distribution", required=True, multiple=False),
        Field("name", str, "name", required=True, multiple=False),
        Field("view_url", str, "url", required=False, multiple=False),  # for model catalog url
        Field("identifier", str, "identifier", required=True, multiple=False),
        Field("resource_type", str, "resourceType", required=False, multiple=False),
        Field("order", int, "order", required=False, multiple=False),
        Field("part_of", "livepapers.LivePaperResourceSection", "partOf", required=True, multiple=False)
    )
    existence_query_fields = ["identifier", "part_of"]


class LivePaperResourceSection(KGObject):
    """
    Data associated with Live Paper resource sections.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/livepapers/resourcesection/v0.1.1"
    type = ["prov:Entity", "prov:Collection", "nsg:LivePaperResourceSection"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "name": "schema:name",
            "description": "schema:description",
            "hadMember": "prov:hadMember",
            "logo": "schema:logo",
            "partOf": "nsg:partOf"
        }
    ]
    fields = (
        Field("order", int, "order", required=True, multiple=False),
        Field("section_type", str, "sectionType", required=True, multiple=False),
        Field("name", str, "name", required=True, multiple=False),
        Field("icon", str, "logo", required=True, multiple=False),
        Field("description", str, "description", required=False, multiple=False),
        Field("data", LivePaperResourceItem, "^nsg:partOf", reverse="section", required=False, multiple=True),
        Field("part_of", "livepapers.LivePaper", "partOf", required=True, multiple=False)
    )
    existence_query_fields = ["name", "part_of"]  # would be better to use sectionType


class LivePaper(KGObject, HasAliasMixin):
    """
    Data for generating live papers.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/livepapers/livepaper/v0.1.1"
    type = ["prov:Entity", "nsg:LivePaper"]
    query_id = "fgSimpleAlt"
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "dateCreated": "schema:dateCreated",
            "dateModified": "schema:dateModified",
            "publication": "nsg:publication",
            "version": "nsg:version",
            "author": "schema:author",
            "owner": "nsg:owner",
            "contributor": "schema:contributor",
            "datePublished": "schema:datePublished",
            "license": "schema:license",
            "resourceSection": "schema:LivePaperResourceSection",
            "dcterms": "http://purl.org/dc/terms/",
            "hasPart": "dcterms:hasPart",
            "citation": "schema:citation",
            "identifier": "schema:identifier",
            "associatedIdentifier": "nsg:associatedIdentifier",
            "collabID": "nsg:collabID",
            "headline": "schema:headline",
            "journal": "nsg:journalName",
            "correspondingAuthorIndex": "nsg:correspondingAuthorIndex",
            "accessCode": "schema:accessCode",
            "alias": "nsg:alias",
            "abstract": "schema:abstract",
            "label": "rdfs:label"
        }
    ]
    fields = (
        Field("name", str, "name", required=True, multiple=False),
        Field("alias", str, "alias", required=False, multiple=False),
        Field("description", str, "description", required=False, multiple=False),
        Field("date_created", (date, datetime), "dateCreated", required=False, multiple=False),
        Field("date_modified", datetime, "dateModified", required=False, multiple=False),
        Field("version", str, "version", multiple=False),
        Field("original_authors", Person, "author", required=True, multiple=True),
        Field("corresponding_author_index", int, "correspondingAuthorIndex", required=False, multiple=True),
        Field("custodian", Person, "owner", required=False, multiple=False),
        Field("live_paper_authors", Person, "contributor", required=False, multiple=True),
        Field("collab_id", str, "collabID", required=True, multiple=False),
        Field("date_published", date, "datePublished", required=False, multiple=False),
        Field("title", str, "headline", required=True, multiple=False),
        Field("journal", str, "journal", required=False, multiple=False),
        Field("url", Distribution, "distribution", required=False, multiple=False),
        Field("citation", str, "citation", required=False, multiple=False),
        Field("doi", str, "identifier", required=False, multiple=False),
        Field("associated_paper_doi", str, "associatedIdentifier", required=False, multiple=False),
        Field("abstract", str, "abstract", required=False, multiple=False),
        Field("license", License, "license", required=False, multiple=False),
        Field("resource_section", LivePaperResourceSection, "^nsg:partOf", reverse="part_of", multiple=True),
        Field("access_code", str, "accessCode", required=False, multiple=True)
    )


"""
{
    "@context": [
        {
            "imports": {
                "@id": "owl:imports",
                "@type": "@id",
                "@container": "@set"
            },
            "owl": "http://www.w3.org/2002/07/owl#"
        },
        "https://nexus.humanbrainproject.org/v0/contexts/neurosciencegraph/core/data/v0.3.1",
        "https://nexus.humanbrainproject.org/v0/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "schema": "http://schema.org/",
            "url": "schema:url"
        },
        {
            "this": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/resourceitem/v0.1.0/shapes/"
        }
    ],
    "@id": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/resourceitem/v0.1.0",
    "@type": "nxv:Schema",
    "imports": [
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0",
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/typedlabeledontologyterm/v0.1.2"
    ],
    "shapes": [
        {
            "@id": "this:LivePaperResourceItemShape",
            "@type": "sh:NodeShape",
            "and": [
                {
                    "node": "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0/shapes/EntityShape"
                },
                {
                    "property": [
                        {
                            "datatype": "xsd:string",
                            "description": "URL for application that can load/use the item",
                            "maxCount": 1,
                            "name": "View URL",
                            "path": "schema:url"
                        },
                    ]
                }
            ],
            "label": "This shape corresponds to a research object hosted outside EBRAINS, included in an EBRAINS Live Paper",
            "nodekind": "sh:BlankNodeOrIRI",
            "targetClass": "nsg:LivePaperResourceItem"
        }
    ]
}
"""


"""
{
    "@context": [
        {
            "imports": {
                "@id": "owl:imports",
                "@type": "@id",
                "@container": "@set"
            },
            "owl": "http://www.w3.org/2002/07/owl#"
        },
        "https://nexus.humanbrainproject.org/v0/contexts/neurosciencegraph/core/data/v0.3.1",
        "https://nexus.humanbrainproject.org/v0/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "hadMember": "prov:hadMember",
            "logo": "schema:logo"
        },
        {
            "this": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/resourcesection/v0.1.0/shapes/"
        }
    ],
    "@id": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/resourcesection/v0.1.0",
    "@type": "nxv:Schema",
    "imports": [
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0",
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/typedlabeledontologyterm/v0.1.2"
    ],
    "shapes": [
        {
            "@id": "this:LivePaperResourceSectionShape",
            "@type": "sh:NodeShape",
            "and": [
                {
                    "node": "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0/shapes/EntityShape"
                },
                {
                    "property": [
                        {
                            "datatype": "xsd:string",
                            "description": "an icon for the section",
                            "maxCount": 1,
                            "name": "Icon",
                            "path": "schema:logo"
                        },
                        {
                            "description": "Research objects included in this section",
                            "name": "Resource Item",
                            "path": "prov:hadMember"
                        }
                    ]
                }
            ],
            "label": "This shape corresponds to a subsection of an EBRAINS Live Paper",
            "nodekind": "sh:BlankNodeOrIRI",
            "targetClass": "nsg:LivePaperResourceSection"
        }
    ]
}
"""


"""
{
    "@context": [
        {
            "imports": {
                "@id": "owl:imports",
                "@type": "@id",
                "@container": "@set"
            },
            "owl": "http://www.w3.org/2002/07/owl#"
        },
        "https://nexus.humanbrainproject.org/v0/contexts/neurosciencegraph/core/data/v0.3.1",
        "https://nexus.humanbrainproject.org/v0/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "dateCreated": "schema:dateCreated",
            "dateModified": "schema:dateModified",
            "publication": "nsg:publication",
            "version": "nsg:version",
            "author": "schema:author",
            "owner": "nsg:owner",
            "contributor": "schema:contributor",
            "datePublished": "schema:datePublished",
            "license": "schema:license",
            "resourceSection": "schema:LivePaperResourceSection",
            "dcterms": "http://purl.org/dc/terms/",
            "hasPart": "dcterms:hasPart",
            "citation": "schema:citation",
            "identifier": "schema:identifier",
        },
        {
            "this": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/livepaper/v0.1.0/shapes/"
        }
    ],
    "@id": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/livepapers/livepaper/v0.1.0",
    "@type": "nxv:Schema",
    "imports": [
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0",
        "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/typedlabeledontologyterm/v0.1.2"
    ],
    "shapes": [
        {
            "@id": "this:LivePaperShape",
            "@type": "sh:NodeShape",
            "and": [
                {
                    "node": "https://nexus.humanbrainproject.org/v0/schemas/neurosciencegraph/commons/entity/v0.1.0/shapes/EntityShape"
                },
                {
                    "property": [
                        {
                            "description": "Date at which this entity last modified.",
                            "maxCount": 1,
                            "name": "Modification date",
                            "nodeKind": "xsd:dateTime",
                            "path": "schema:dateModified"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "the version of the Live Paper",
                            "maxCount": 1,
                            "minCount": 1,
                            "name": "Version",
                            "path": "nsg:version"
                        },
                        {
                            "description": "Author(s) of the original paper",
                            "minCount": 1,
                            "name": "Author",
                            "node": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/commons/person/v0.1.0/shapes/PersonShape",
                            "path": "schema:author"
                        },
                        {
                            "description": "Custodian / corresponding author of the Live Paper",
                            "minCount": 1,
                            "name": "Owner",
                            "node": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/commons/person/v0.1.0/shapes/PersonShape",
                            "path": "nsg:owner"
                        },
                                                {
                            "description": "Additional contributors to the Live Paper",
                            "name": "Additional contributors",
                            "node": "https://nexus.humanbrainproject.org/v0/schemas/modelvalidation/commons/person/v0.1.0/shapes/PersonShape",
                            "path": "schema:contributor"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "collab id of the Live Paper",
                            "maxCount": 1,
                            "name": "collab id",
                            "path": "nsg:collabID"
                        },
                        {
                            "description": "Publication date of original paper",
                            "maxCount": 1,
                            "name": "Publication date",
                            "nodeKind": "xsd:dateTime",
                            "path": "schema:datePublished"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "title of the original paper",
                            "minCount": 1,
                            "maxCount": 1,
                            "name": "Title",
                            "path": "schema:title"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "name of the journal where original article published",
                            "maxCount": 1,
                            "name": "Journal name",
                            "path": "nsg:journalName"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "DOI of the original article",
                            "maxCount": 1,
                            "name": "DOI",
                            "path": "schema:identifier"
                        },
                        {
                            "datatype": "xsd:string",
                            "description": "abstract of the original paper",
                            "maxCount": 1,
                            "name": "Description",
                            "path": "schema:description"
                        },
                        {
                            "class": "nsg:LivePaperResourceSection",
                            "description": "Subsections of the Live Paper.",
                            "name": "Resource Section",
                            "path": "dcterms:hasPart"
                        }
                    ]
                }
            ],
            "label": "This shape corresponds to EBRAINS Live Papers",
            "nodekind": "sh:BlankNodeOrIRI",
            "targetClass": "nsg:LivePaper"
        }
    ]
}
"""