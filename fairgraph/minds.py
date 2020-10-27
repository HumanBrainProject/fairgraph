"""
"Minimal Information for Neuroscience DataSets" - metadata common to all neuroscience
datasets independent of the type of investigation

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


import sys
import inspect
import os
from datetime import datetime
try:
    basestring
except NameError:
    basestring = str
    raw_input = input
try:
    from urllib.parse import urlparse, quote_plus, parse_qs, urlencode
except ImportError:  # Python 2
    from urlparse import urlparse, parse_qs
    from urllib import quote_plus, urlencode

import requests
from tqdm import tqdm

from fairgraph.base import KGObject, KGProxy, KGQuery, cache, as_list, Field
from fairgraph.data import FileAssociation, CSCSFile
from fairgraph.commons import QuantitativeValue
from fairgraph.utility import in_notebook


class MINDSObject(KGObject):
    """
    Base class for MINDS metadata
    """
    namespace = "minds"
    context = [
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "schema": "http://schema.org/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "prov": "http://www.w3.org/ns/prov#",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "minds": 'https://schema.hbp.eu/minds/',
            "uniminds": 'https://schema.hbp.eu/uniminds/',
        }
    ]


class Person(MINDSObject):
    """
    A person associated with research data or models, for example as an experimentalist,
    or a data analyst.
    """
    _path = "/core/person/v1.0.0"
    type = ["minds:Person"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("shortname", basestring, "https://schema.hbp.eu/minds/shortName", required=False, multiple=False))


class Activity(MINDSObject):
    """
    A research activity.
    """
    _path = "/core/activity/v1.0.0"
    type = ["minds:Activity"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("ethics_approval", "minds.EthicsApproval", "https://schema.hbp.eu/minds/ethicsApproval", required=False, multiple=True),
      Field("ethics_authority", "minds.EthicsAuthority", "https://schema.hbp.eu/minds/ethicsAuthority", required=False, multiple=True),
      Field("methods", "minds.Method", "https://schema.hbp.eu/minds/methods", required=False, multiple=True),
      Field("preparation", "minds.Preparation", "https://schema.hbp.eu/minds/preparation", required=False, multiple=False),
      Field("protocols", "minds.Protocol", "https://schema.hbp.eu/minds/protocols", required=False, multiple=True))



class AgeCategory(MINDSObject):
    """
    An age category, e.g. "adult", "juvenile"
    """
    _path = "/core/agecategory/v1.0.0"
    type = ["minds:Agecategory"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class EthicsApproval(MINDSObject):
    """
    Record of an  ethics approval.
    """
    _path = "/ethics/approval/v1.0.0"
    type = ["minds:Approval"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("generated_by", "minds.EthicsAuthority", "https://schema.hbp.eu/minds/generatedBy", required=False, multiple=True))


class EthicsAuthority(MINDSObject):
    """
    A entity legally authorised to approve or deny permission to conduct an experiment on ethical grounds.
    """
    _path = "/ethics/authority/v1.0.0"
    type = ["minds:Authority"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      #Field("generated_by", KGObject, "https://schema.hbp.eu/minds/generatedBy", required=False, multiple=False))
    )

terms_of_use = """
# EBRAINS Knowledge Graph Data Platform Citation Requirements

This text is provided to describe the requirements for citing data found via
EBRAINS Knowledge Graph Data Platform (KG): https://kg.ebrains.eu/search.
It is meant to provide a more human-readable form of key parts of the KG Terms
of Service, but in the event of disagreement between the KG Terms of Service
and these Citation Requirements, the former is to be taken as authoritative.

## Dataset licensing

All datasets in the KG have explicit licensing conditions attached. The
license is typically one of the Creative Commons licenses. You must follow the
licensing conditions attached to the dataset, including all restrictions on
commercial use, requirements for attribution or requirements to share-alike.

## EBRAINS Knowledge Graph citation policy

If you use of the software and datasets found via the KG, the KG Pyxus API, KG
REST API or fairgraph library in your scientific publication you must follow
the following citation policy:

1. Cite "EBRAINS Knowledge Graph Data Platform: https://www.ebrains.eu/search"

2. For a dataset is released under a Creative Commons license which includes
   "Attribution", please cite:

    1. The primary publication listed under the dataset.

    2. The dataset DOI, if using a collection of single datasets.

    3. The parent project DOI, if using multiple dataset from the same project

    4. In cases where a primary publication is not provided, and only in such
       cases, the names of the Data Contributors should be cited (Data
       provided by Contributor 1, Contributor 2, ..., and Contributor N) in
       addition to the citation of the Site and the DOI for the data.

3. For software, you must cite software as defined in the software's
   respective citation policy. If you can not find a citation or
   acknowledgement policy for the software, please use the open source
   repository link as the citation link.

Failure to cite data or software used in a publication or presentation
constitutes scientific misconduct. Failure to cite data or software used in a
scientific publication must be corrected by issuing an official Erratum and
correction of the given article if it is discovered post-publication.
"""


class Dataset(MINDSObject):
    """
    A collection of related data files.
    """
    _path = "/core/dataset/v1.0.0"
    type = ["minds:Dataset"]
    accepted_terms_of_use = False
    fields = (
      Field("activity", Activity, "https://schema.hbp.eu/minds/activity", required=False, multiple=True),
      # to be merged in a method:
      Field("container_url_as_ZIP", bool, "https://schema.hbp.eu/minds/containerUrlAsZIP", required=False, multiple=False),
      Field("container_url", basestring, "https://schema.hbp.eu/minds/container_url", required=False, multiple=False),
      Field("datalink", basestring, "http://schema.org/datalink", required=False, multiple=False),

      Field("dataset_doi", basestring, "https://schema.hbp.eu/minds/datasetDOI", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("external_datalink", basestring, "https://schema.hbp.eu/minds/external_datalink", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=True, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("release_date", datetime, "https://schema.hbp.eu/minds/release_date", required=False, multiple=False, strict=False),
      Field("component", "minds.PLAComponent", "https://schema.hbp.eu/minds/component", required=False, multiple=True),
      Field("contributors", Person, "https://schema.hbp.eu/minds/contributors", required=False, multiple=True),
      Field("doireference", basestring, "https://schema.hbp.eu/minds/doireference", required=False, multiple=False),
      Field("embargo_status", "minds.EmbargoStatus", "https://schema.hbp.eu/minds/embargo_status", required=False, multiple=False),
      Field("formats", "minds.Format", "https://schema.hbp.eu/minds/formats", required=False, multiple=True),
      Field("license", "minds.License", "https://schema.hbp.eu/minds/license", required=False, multiple=False),
      #Field("license_info", basestring, "https://schema.hbp.eu/minds/license_info", required=False, multiple=False),
      Field("modality", "minds.Modality", "https://schema.hbp.eu/minds/modality", required=False, multiple=True),
      Field("owners", Person, "https://schema.hbp.eu/minds/owners", required=False, multiple=True),
      Field("parcellation_atlas", "minds.ParcellationAtlas", "https://schema.hbp.eu/minds/parcellationAtlas", required=False, multiple=True),
      Field("parcellation_region", "minds.ParcellationRegion", "https://schema.hbp.eu/minds/parcellationRegion", required=False, multiple=True),
      Field("part_of", basestring, "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/partOf", required=False, multiple=False),
      Field("publications", "minds.Publication", "https://schema.hbp.eu/minds/publications", required=False, multiple=True),
      Field("reference_space", "minds.ReferenceSpace", "https://schema.hbp.eu/minds/reference_space", required=False, multiple=True),
      Field("specimen_group", "minds.SpecimenGroup", "https://schema.hbp.eu/minds/specimen_group", required=False, multiple=True))

    def download(self, local_directory, accept_terms_of_use=False):
        # todo: add support for download as zip
        # todo: check hashes
        if not (accept_terms_of_use or self.accepted_terms_of_use):
            if in_notebook():
                from IPython.display import display, Markdown
                display(Markdown(terms_of_use))
            else:
                print(terms_of_use)
            user_response = raw_input("Do you accept the EBRAINS KG Terms of Service? ")
            if user_response in ('y', 'Y', 'yes', 'YES'):
                self.__class__.accepted_terms_of_use = True
            else:
                raise Exception("Please accept the terms of use before downloading the dataset")

        parts = urlparse(self.container_url)
        query_dict = parse_qs(parts.query)
        query_dict['format'] = "json"
        url = parts._replace(query=urlencode(query_dict, True)).geturl()
        response = requests.get(url)
        if response.status_code not in (200, 204):
            raise IOError(
                "Unable to download dataset. Response code {}".format(response.status_code))
        contents = response.json()
        total_data_size = sum(item["bytes"] for item in contents) // 1024
        progress_bar = tqdm(total=total_data_size)
        for entry in sorted(contents,
                            key=lambda entry: entry["content_type"] != "application/directory"):
            # take directories first
            local_path = os.path.join(local_directory, entry["name"])
            #if entry["name"].endswith("/"):
            if entry["content_type"] == "application/directory":
                os.makedirs(local_path, exist_ok=True)
            else:
                response2 = requests.get(self.container_url + "/" + entry["name"])
                if response2.status_code in (200, 204):
                    with open(local_path, "wb") as fp:
                        fp.write(response2.content)
                    progress_bar.update(entry["bytes"] // 1024)
                else:
                    raise IOError(
                        "Unable to download file '{}'. Response code {}".format(
                            local_path, response2.status_code))
        progress_bar.close()

    def methods(self, client, api="query", scope="released"):
        """Return a list of experimental methods associated with the dataset"""
        filter = {
            "dataset": self.id
        }
        instances = client.query_kgquery(Method.path, "fgDatasets", filter=filter, scope=scope)
        return [Method.from_kg_instance(inst, client) for inst in instances]

    @classmethod
    def list(cls, client, size=100, from_index=0, api="query",
             scope="released", resolved=False, **filters):
        """List all objects of this type in the Knowledge Graph"""
        if api == "nexus":
            context = {
                'nsg': 'https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/',
                'prov': 'http://www.w3.org/ns/prov#'
            }
            filter_queries = []
            for name, value in filters.items():
                if name == "method":
                    filter_queries.append({
                        "path": "minds:specimen_group / minds:subjects / minds:samples / minds:methods / schema:name",
                        "op": "eq",
                        "value": value.name
                    })
                else:
                    raise Exception("The only supported filters are by specimen group. You specified {name}".format(name=name))
            if len(filter_queries) == 0:
                return client.list(cls, api="nexus", size=size)
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
            return super(Dataset, cls).list(client, size, from_index, api,
                                                scope, resolved, **filters)
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")


class EmbargoStatus(MINDSObject):
    """
    Information about the embargo period during which a given dataset cannot be publicly shared.
    """
    _path = "/core/embargostatus/v1.0.0"
    type = ["minds:Embargostatus"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class File(MINDSObject):
    """
    Metadata about a single file.
    """
    _path = "/core/file/v0.0.4"
    type = ["minds:File"]
    fields = (
      Field("absolute_path", basestring, "http://hbp.eu/minds#absolute_path", required=False, multiple=False),
      Field("byte_size", int, "http://hbp.eu/minds#byte_size", required=False, multiple=False),
      Field("content_type", basestring, "http://hbp.eu/minds#content_type", required=False, multiple=False),
      Field("hash", basestring, "http://hbp.eu/minds#hash", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("last_modified", datetime, "http://hbp.eu/minds#last_modified", required=False, multiple=False),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("relative_path", basestring, "http://hbp.eu/minds#relative_path", required=False, multiple=False))


class FileAssociation(MINDSObject):
    """
    A link between a file and a dataset.
    """
    _path = "/core/fileassociation/v1.0.0"
    type = ["minds:Fileassociation"]
    fields = (
      Field("from", File, "https://schema.hbp.eu/linkinginstance/from", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      Field("to", Dataset, "https://schema.hbp.eu/linkinginstance/to", required=False, multiple=False))


class Format(MINDSObject):
    """
    A file/data format.
    """
    _path = "/core/format/v1.0.0"
    type = ["minds:Format"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class License(MINDSObject):
    """
    A license governing sharing of a dataset.
    """
    _path = "/core/licensetype/v1.0.0"
    type = ["minds:Licensetype"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #ield("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class Method(MINDSObject):
    """
    An experimental method.
    """
    _path = "/experiment/method/v1.0.0"
    # also see "/core/method/v1.0.0"
    type = ["minds:Method"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class Modality(MINDSObject):
    """
    A recording modality.
    """
    _path = "/core/modality/v1.0.0"
    type = ["minds:Modality"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class ParcellationAtlas(MINDSObject):
    """
    A brain atlas in which the brain of a given species of animal is divided into regions.
    """
    _path = "/core/parcellationatlas/v1.0.0"
    type = ["minds:Parcellationatlas"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class ParcellationRegion(MINDSObject):
    """
    A brain region as defined by a brain atlas.
    """
    _path = "/core/parcellationregion/v1.0.0"
    type = ["minds:Parcellationregion"]
    fields = (
      Field("alias", basestring, "https://schema.hbp.eu/minds/alias", required=False, multiple=False),
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("url", basestring, "https://schema.hbp.eu/viewer/url", required=False, multiple=False),
      Field("species", "minds.Species", "https://schema.hbp.eu/minds/species", required=False, multiple=False))


class PLAComponent(MINDSObject):
    """
    A data or software component, as defined in the HBP "project lifecycle" application.
    """
    _path = "/core/placomponent/v1.0.0"
    type = ["minds:Placomponent"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("component", basestring, "https://schema.hbp.eu/minds/component", required=False, multiple=False))


class Preparation(MINDSObject):
    """
    An experimental preparation.
    """
    _path = "/core/preparation/v1.0.0"
    type = ["minds:Preparation"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class Protocol(MINDSObject):
    """
    An experimental procotol.
    """
    _path = "/experiment/protocol/v1.0.0"
    type = ["minds:Protocol"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class Publication(MINDSObject):
    """
    A scientific publication.
    """
    _path = "/core/publication/v1.0.0"
    type = ["minds:Publication"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("cite", basestring, "https://schema.hbp.eu/minds/cite", required=False, multiple=False),
      Field("doi", basestring, "https://schema.hbp.eu/minds/doi", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("authors", Person, "https://schema.hbp.eu/minds/authors", required=False, multiple=True))


class ReferenceSpace(MINDSObject):
    """
    A reference space for a brain atlas.
    """
    _path = "/core/referencespace/v1.0.0"
    type = ["minds:Referencespace"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False))
    )


class Role(MINDSObject):
    """
    The role of a person within an experiment.
    """
    _path = "/prov/role/v1.0.0"
    type = ["minds:Role"]
    fields = (
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))

class Sample(MINDSObject):
    """
    A sample of neural tissue.
    """
    _path = "/experiment/sample/v1.0.0"
    type = ["minds:Sample"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("container_url", basestring, "https://schema.hbp.eu/minds/container_url", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      #Field("weight_post_fixation", QuantitativeValue, "https://schema.hbp.eu/minds/weightPostFixation", required=False, multiple=False),
      Field("weight_post_fixation", basestring, "https://schema.hbp.eu/minds/weightPostFixation", required=False, multiple=False),
      #Field("weight_pre_fixation", QuantitativeValue, "https://schema.hbp.eu/minds/weightPreFixation", required=False, multiple=False),
      Field("weight_pre_fixation", basestring, "https://schema.hbp.eu/minds/weightPreFixation", required=False, multiple=False),
      Field("methods", Method, "https://schema.hbp.eu/minds/methods", required=False, multiple=True),
      Field("parcellation_atlas", ParcellationAtlas, "https://schema.hbp.eu/minds/parcellationAtlas", required=False, multiple=False),
      Field("parcellation_region", ParcellationRegion, "https://schema.hbp.eu/minds/parcellationRegion", required=False, multiple=True),
      Field("reference", basestring, "https://schema.hbp.eu/brainviewer/reference", required=False, multiple=False))


class Sex(MINDSObject):
    """
    The sex of an animal or person from whom/which data were obtained.
    """
    _path = "/core/sex/v1.0.0"
    type = ["minds:Sex"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class SoftwareAgent(MINDSObject):
    """
    Software that performed a given activity.
    """
    _path = "/core/softwareagent/v1.0.0"
    type = ["minds:Softwareagent"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("description", basestring, "http://schema.org/description", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False))


class Species(MINDSObject):
    """
    The species of an experimental subject, expressed with the binomial nomenclature.
    """
    _path = "/core/species/v1.0.0"
    type = ["minds:Species"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      #Field("alternate_of", KGObject, "http://www.w3.org/ns/prov#alternateOf", required=False, multiple=False))
    )


class SpecimenGroup(MINDSObject):
    """
    A group of experimental subjects.
    """
    _path = "/core/specimengroup/v1.0.0"
    type = ["minds:Specimengroup"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("subjects", "minds.Subject", "https://schema.hbp.eu/minds/subjects", required=False, multiple=True))


class Subject(MINDSObject):
    """
    The organism that is the subject of an experimental investigation.
    """
    _path = "/experiment/subject/v1.0.0"
    type = ["minds:Subject"]
    fields = (
      # Field("alternatives", KGObject, "https://schema.hbp.eu/inference/alternatives", required=False, multiple=True),
      Field("cause_of_death", basestring, "https://schema.hbp.eu/minds/causeOfDeath", required=False, multiple=False),
      Field("genotype", basestring, "https://schema.hbp.eu/minds/genotype", required=False, multiple=False),
      Field("identifier", basestring, "http://schema.org/identifier", required=False, multiple=True),
      Field("name", basestring, "http://schema.org/name", required=False, multiple=False),
      #Field("associated_with", Person, "http://www.w3.org/ns/prov#qualifiedAssociation", required=False, multiple=False),
      Field("strain", basestring, "https://schema.hbp.eu/minds/strain", required=False, multiple=False),
      Field("strains", basestring, "https://schema.hbp.eu/minds/strains", required=False, multiple=True),
      #Field("weight", QuantitativeValue, "https://schema.hbp.eu/minds/weight", required=False, multiple=False),
      Field("weight", basestring, "https://schema.hbp.eu/minds/weight", required=False, multiple=False),
      #Field("age", QuantitativeValue, "https://schema.hbp.eu/minds/age", required=False, multiple=False),
      Field("age", basestring, "https://schema.hbp.eu/minds/age", required=False, multiple=False),
      Field("age_category", AgeCategory, "https://schema.hbp.eu/minds/age_category", required=False, multiple=False),
      Field("samples", Sample, "https://schema.hbp.eu/minds/samples", required=False, multiple=True),
      Field("sex", Sex, "https://schema.hbp.eu/minds/sex", required=False, multiple=True),  # should be multiple=False, but some nodes have both
      Field("species", Species, "https://schema.hbp.eu/minds/species", required=False, multiple=False))


def list_kg_classes():
    """List all KG classes defined in this module"""
    classes = [obj for name, obj in inspect.getmembers(sys.modules[__name__])
               if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]
    classes.remove(MINDSObject)
    return classes


# Alias some classes to reflect names used in KG Search
Project = PLAComponent


if __name__=='__main__':

    import os
    from fairgraph import minds, KGClient
    token = os.environ['HBP_token']
    client = KGClient(token)
    for cls in minds.list_kg_classes():
        print(cls.__name__)
