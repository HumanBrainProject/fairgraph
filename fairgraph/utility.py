"""


"""

# Copyright 2019 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from urllib.parse import urlparse, quote_plus
except ImportError:  # Python 2
    from urlparse import urlparse
    from urllib import quote_plus
try:
    basestring
except NameError:
    basestring = str
from pyld import jsonld


ATTACHMENT_SIZE_LIMIT = 1024 * 1024  # 1 MB


standard_context = {
    # workaround. Need to implement context handling properly
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "prov": "http://www.w3.org/ns/prov#",
    "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
    "minds": "https://schema.hbp.eu/minds/",
    "uniminds": "https://schema.hbp.eu/uniminds/",
    "name": "schema:name",
    "description": "schema:description",
    "brainRegion": "nsg:brainRegion",
    "species": "nsg:species",
    "modelOf": "nsg:modelOf",
    "mainModelScript": "nsg:mainModelScript",
    "release": "nsg:release",
    "version": "schema:version",
    "generatedAtTime": "prov:generatedAtTime",
    "isPartOf": "nsg:isPartOf",  # not sure about prefix,
    "partOf": "nsg:partOf",
    "parameters": "nsg:parameters",
    "morphology": "nsg:morphology",
    "eModel": "nsg:eModel",
    "images": "nsg:images",
    "address": "schema:address",
    "parentOrganization": "schema:parentOrganization",
    "code_format": "nsg:code_format",
    "license": "schema:license",
    "distribution": "schema:distribution",
    "oldUUID": "nsg:providerId",
    "wasAssociatedWith": "prov:wasAssociatedWith",
    "strain": "nsg:strain",
    "sex": "nsg:sex",
    "age": "nsg:age",
    "deathDate": "schema:deathDate",
    "eType": "nsg:eType",
    "protocol": "nsg:protocol",
    "wasDerivedFrom": "prov:wasDerivedFrom",
    "hadMember": "prov:hadMember",
    "channelName": "nsg:channelName",
    "author": "schema:author",
    "dateCreated": "schema:dateCreated",
    "alias": "nsg:alias",
    "celltype": "nsg:celltype",
    "testType": "nsg:testType",
    "referenceData": "nsg:referenceData",
    "dataType": "nsg:dataType",
    "recordingModality": "nsg:recordingModality",
    "scoreType": "nsg:scoreType",
    "score": "nsg:score",
    "status": "nsg:status",
    "used": "prov:used",
    "modelUsed": "prov:used",
    "testUsed": "prov:used",
    "dataUsed": "prov:used",
    "startedAtTime": "prov:startedAtTime",
    "endedAtTime": "prov:endedAtTime",
    "generated": "prov:generated",
    "wasGeneratedBy": "prov:wasGeneratedBy",
    "wasAttributedTo": "prov:wasAttributedTo",
    "passedValidation": "nsg:passedValidation",
    "passed": "nsg:passedValidation",
    "repository": "schema:codeRepository",
    "path": "nsg:path",
    "implements": "nsg:implements",
    "normalizedScore": "nsg:normalizedScore",
    "collabID": "nsg:collabID",
    "hash": "nsg:digest",
    "familyName": "schema:familyName",
    "givenName": "schema:givenName",
    "email": "schema:email",
    "affiliation": "schema:affiliation",
    "organization": "nsg:organization",
    "channelType": "nsg:channelType",
    "morphologyType": "nsg:morphologyType",
    "atTime" : "nsg:atTime",
    "identifier": "schema:identifier",
}


def as_list(obj):
    if obj is None:
        return []
    elif isinstance(obj, (dict, basestring)):
        return [obj]
    try:
        L = list(obj)
    except TypeError:
        L = [obj]
    return L


def expand_uri(uri_list, context, client=None):
    if client:
        full_context = [standard_context]
        for item in as_list(context):
            if "{{base}}" in item:
                pass  # tmp hack, need to implement context handling properly
                #full_context.append(item.replace("{{base}}", client.nexus_endpoint))
            else:
                full_context.append(item)
    else:
        full_context = context
    doc = {
        "@type": uri_list,
        "@context": full_context
    }
    # print(doc)
    # print(jsonld.expand(doc))
    # print("----")
    expanded_uris = tuple(jsonld.expand(doc)[0]["@type"])
    for uri in expanded_uris:
        if not uri.startswith("http"):
            raise ValueError("Problem expanding '{}'. Context = {}".format(uri_list, full_context))
    return expanded_uris


def compact_uri(uri_list, context):
    return tuple(as_list(jsonld.compact({"@type": uri_list}, context)["@type"]))


def namespace_from_id(id):
    parts = urlparse(id)
    path_parts = parts.path.split("/")
    assert path_parts[2] == "data"
    return path_parts[3]


def in_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        elif shell == 'TerminalInteractiveShell':
            return False
        else:
            return False
    except NameError:
        return False
