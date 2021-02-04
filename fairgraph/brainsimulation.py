"""
Metadata for model building, simulation and validation.

"""

# Copyright 2018-2020 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import os.path
import logging
from datetime import datetime, date
import mimetypes
import sys
import json
import inspect
from dateutil import parser as date_parser
import requests
from .base import (KGObject, cache, KGProxy, build_kg_object, Distribution, as_list, KGQuery,
                   Field, IRI, upload_attachment)
from .commons import BrainRegion, CellType, Species, AbstractionLevel, ModelScope, OntologyTerm
from .core import Organization, Person, Age, Collection
from .utility import compact_uri, standard_context
from .computing import ComputingEnvironment


logger = logging.getLogger("fairgraph")
mimetypes.init()

DEFAULT_NAMESPACE = "modelvalidation"

from .utility import ATTACHMENT_SIZE_LIMIT


class HasAliasMixin(object):

    @classmethod
    def from_alias(cls, alias, client, api="query"):
        context = {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"
        }
        query = {
            "nexus": {
                "path": "nsg:alias",
                "op": "eq",
                "value": alias
            },
            "query": {
                "alias": alias
            }
        }
        return KGQuery(cls, query, context).resolve(client, api=api)


class ModelProject(KGObject, HasAliasMixin):
    """
    Representation of a neuroscience model or modelling project.

    We distinguish a model in an abstract sense (this class), which may have multiple
    parameterizations and multiple implementations, from a specific version and
    parameterization of a model - see :class:`ModelInstance` and :class:`ModelScript`
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/modelproject/v0.1.1"
    type = ["prov:Entity", "nsg:ModelProject"]
    context = {
        "name": "schema:name",
        "label": "rdfs:label",
        "alias": "nsg:alias",
        "author": "schema:author",
        "owner": "nsg:owner",
        "organization": "nsg:organization",
        "PLAComponents": "nsg:PLAComponents",
        "private": "nsg:private",
        "collabID": "nsg:collabID",
        "brainRegion": "nsg:brainRegion",
        "species": "nsg:species",
        "celltype": "nsg:celltype",
        "abstractionLevel": "nsg:abstractionLevel",
        "modelOf": "nsg:modelOf",
        "description": "schema:description",
        "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
        "prov": "http://www.w3.org/ns/prov#",
        "schema": "http://schema.org/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "dateCreated": "schema:dateCreated",
        "dcterms": "http://purl.org/dc/terms/",
        "instances": "dcterms:hasPart",
        "oldUUID": "nsg:providerId",
        "partOf": "nsg:partOf",
        "hasPart": "dcterms:hasPart"
    }
    fields = (
        Field("name", str, "name", required=True),
        Field("owners", Person, "owner", required=True, multiple=True),
        Field("authors", Person, "author", required=True, multiple=True),
        Field("description", str, "description", required=True),
        Field("date_created", datetime, "dateCreated", required=True),
        Field("private", bool, "private", required=True),
        Field("collab_id", str, "collabID"),
        Field("alias", str, "alias"),
        Field("organization", Organization, "organization", multiple=True),
        Field("pla_components", str, "PLAComponents", multiple=True),
        Field("brain_region", BrainRegion, "brainRegion", multiple=True),
        Field("species", Species, "species"),
        Field("celltype", CellType, "celltype"),
        Field("abstraction_level", AbstractionLevel, "abstractionLevel"),
        Field("model_of", ModelScope, "modelOf"),
        Field("old_uuid", str, "oldUUID"),
        Field("parents", "brainsimulation.ModelProject", "partOf", multiple=True),
        #Field("instances", ("brainsimulation.ModelInstance", "brainsimulation.MEModel"),
        #      "dcterms:hasPart", multiple=True),
        # todo: kg query returns "hasPart", while nexus instances mostly use "dcterms:hasPart"
        #       suggest changing all instances to store "hasPart", with corrected context if needed
        Field("instances", ("brainsimulation.ModelInstance", "brainsimulation.MEModel"),
              "hasPart", multiple=True),
        Field("images", dict, "images", multiple=True)  # type should be Distribution?
    )
    # allow multiple projects with the same name
    existence_query_fields = ("name", "date_created")

    def __init__(self, name, owners, authors, description, date_created, private, collab_id=None,
                 alias=None, organization=None, pla_components=None, brain_region=None,
                 species=None, celltype=None, abstraction_level=None, model_of=None,
                 old_uuid=None, parents=None, instances=None, images=None,
                 id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    def authors_str(self, client):
        api = self.instance.data.get("fg:api", "query")
        return ", ".join("{obj.given_name} {obj.family_name}".format(obj=obj.resolve(client, api=api))
                         for obj in self.authors)

    #def sub_projects(self):


class ModelInstance(KGObject):
    """
    A specific implementation, code version and parameterization of a model.

    See also: :class:`ModelProject`, :class:`MEModel`, :class:`ModelScript`
    """
    #path = DEFAULT_NAMESPACE + "/simulation/modelinstance/v0.1.2"
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/modelinstance/v0.1.1"
    type = ["prov:Entity", "nsg:ModelInstance"]
    # ScientificModelInstance
    #   - model -> linked ModelProject using partOf
    #   - version -> add field to ModelInstance.
    #   - description -> part of Entity
    #   - parameters -> linked ModelParameters
    #   - source -> (e.g. git repository) -> linked ModelScript
    #   - timestamp -> prov:generatedAtTime
    #   - code_format -> linked ModelScript
    #   - hash - general feature, don't put in schema
    #   - morphology - not needed for all models, use MEModel where we have a morphology
    # modelinstance/v0.1.2
    #   - fields of Entity + modelOf, brainRegion, species
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {"oldUUID": "nsg:providerId",
         "generatedAtTime": "prov:generatedAtTime",
         "alternateOf": "prov:alternateOf"}
    ]
    # fields:
    #  - fields of ModelInstance + eModel, morphology, mainModelScript, isPartOf (an MEModelRelease)
    fields = (
        Field("name", str, "name", required=True),
        Field("brain_region", BrainRegion, "brainRegion", required=False),
        Field("species", Species, "species", required=False),
        Field("model_of", (CellType, BrainRegion), "modelOf", required=False),  # should be True, but causes problems for a couple of cases at the moment
        Field("main_script", "brainsimulation.ModelScript", "mainModelScript", required=True),
        Field("release", str, "release", required=False),
        Field("version", str, "version", required=True),
        Field("timestamp", datetime, "generatedAtTime", required=False),
        Field("part_of", KGObject, "isPartOf"),
        Field("description", str, "description"),
        Field("parameters", str, "parameters"),
        Field("old_uuid", str, "oldUUID"),
        Field("alternate_of", KGObject, "alternateOf")
    )

    def __init__(self, name, main_script, version, timestamp=None,
                 brain_region=None, species=None, model_of=None, release=None,
                 part_of=None, description=None, parameters=None,
                 old_uuid=None, alternate_of=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)

    @property
    def project(self):
        query = {
            "nexus": {
                "path": "dcterms:hasPart",
                "op": "eq",
                "value": self.id
            },
            "query": {
                "instances": self.id  # untested
            }
        }
        context = {
            "dcterms": "http://purl.org/dc/terms/"
        }
        return KGQuery(ModelProject, query, context)


class MEModel(ModelInstance):
    """
    A specific implementation, code version and parameterization of a single neuron model
    with a defined morphology (M) and electrical (E) behaviour.

    This is a specialized sub-class of :class:`ModelInstance`.

    See also: :class:`ModelProject`, :class:`ModelScript`, :class:`Morphology`, :class:`EModel`
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/memodel/v0.1.2"  # latest is 0.1.4, but all the data is currently under 0.1.2
    type = ["prov:Entity", "nsg:MEModel", "nsg:ModelInstance"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {"oldUUID": "nsg:providerId",
         "generatedAtTime": "prov:generatedAtTime",
         "alternateOf": "prov:alternateOf"}
    ]
    # fields:
    #  - fields of ModelInstance + eModel, morphology, mainModelScript, isPartOf (an MEModelRelease)
    fields = list(ModelInstance.fields) + [
        Field("morphology", "brainsimulation.Morphology", "morphology", required=True),
        Field("e_model",  "brainsimulation.EModel", "eModel", required=True),
        #Field("project", ModelProject, "isPartOf", required=True)  # conflicts with project property in parent class. To fix.
    ]

    def __init__(self, name, e_model, morphology, main_script, version, timestamp=None, #project,
                 brain_region=None, species=None, model_of=None,
                 release=None, part_of=None, description=None, parameters=None,
                 old_uuid=None, alternate_of=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class Morphology(KGObject):
    """
    The morphology of a single neuron model, typically defined as a set of cylinders or
    truncated cones connected in a tree structure.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/morphology/v0.1.1"
    type = ["prov:Entity", "nsg:Morphology"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0"
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("cell_type", CellType, "modelOf"),
        Field("distribution", Distribution, "distribution")
    )

    def __init__(self, name, cell_type=None, morphology_file=None, distribution=None,
                 id=None, instance=None):
        super(Morphology, self).__init__(name=name, cell_type=cell_type,
                                         distribution=distribution, id=id, instance=instance)
        if morphology_file:
            if distribution:
                raise ValueError("Cannot provide both morphology_file and distribution")
            self.morphology_file = morphology_file

    @property
    def morphology_file(self):
        if isinstance(self.distribution, list):
            return [d.location for d in self.distribution]
        elif self.distribution is None:
            return None
        else:
            return self.distribution.location

    @morphology_file.setter
    def morphology_file(self, value):
        if isinstance(value, list):
            self.distribution = [Distribution(location=mf) for mf in value]
        else:
            self.distribution = Distribution(location=value)


class ModelScript(KGObject):
    """
    Code or markup defining all or part of a model.

    See also: :class:`ModelInstance`, :class:`MEModel`, :class:`EModel`
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/emodelscript/v0.1.0"
    type = ["prov:Entity", "nsg:EModelScript"]  # generalize to other sub-types of script
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "license": "schema:license"
        }
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("code_format", str, "code_format"),
        Field("license", str, "license"),
        Field("distribution", Distribution, "distribution")
    )

    def __init__(self, name, code_location=None, code_format=None, license=None,
                 distribution=None, id=None, instance=None):
        super(ModelScript, self).__init__(name=name, code_format=code_format, license=license,
                                          distribution=distribution, id=id, instance=instance)
        if code_location and distribution:
            raise ValueError("Cannot provide both code_location and distribution")
        if code_location:
            self.distribution = Distribution(location=code_location)

    @property
    def code_location(self):
        if self.distribution:
            return self.distribution.location
        else:
            return None

    @code_location.setter
    def code_location(self, value):
        self.distribution = Distribution(location=value)


class EModel(ModelInstance):
    """The electrical component of an :class:`MEModel`"""
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/emodel/v0.1.1"
    type = ["prov:Entity", "nsg:EModel"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0"
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("brain_region", BrainRegion, "brainRegion", required=False),
        Field("species", Species, "species", required=False),
        Field("model_of", (CellType, BrainRegion), "modelOf", required=False),
        Field("main_script", "brainsimulation.ModelScript", "mainModelScript", required=False),
        Field("release", str, "release", required=False),
        Field("version", str, "version", required=False),
        Field("timestamp", datetime, "generatedAtTime", required=False),
        Field("part_of", KGObject, "isPartOf"),
        Field("description", str, "description"),
        Field("parameters", str, "parameters"),
        Field("old_uuid", str, "oldUUID")
    )

    def __init__(self, name, main_script=None, version=None, timestamp=None, #project,
                 brain_region=None, species=None, model_of=None,
                 release=None, part_of=None, description=None, parameters=None,
                 old_uuid=None, id=None, instance=None):
        args = locals()
        args.pop("self")
        KGObject.__init__(self, **args)


class ValidationTestDefinition(KGObject, HasAliasMixin):
    """Definition of a model validation test.

    See also: :class:`ValidationScript`, :class:`ValidationActivity`, :class:`ValidationResult`
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/validationtestdefinition/v0.1.0"
    #path = DEFAULT_NAMESPACE + "/simulation/validationtestdefinition/v0.1.2"
    type = ["prov:Entity", "nsg:ValidationTestDefinition"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "alias": "nsg:alias",
            "author": "schema:author",
            "brainRegion": "nsg:brainRegion",
            "species": "nsg:species",
            "celltype": "nsg:celltype",
            "abstractionLevel": "nsg:abstractionLevel",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "dateCreated": "schema:dateCreated",
            "testType": "nsg:testType",
            "referenceData": "nsg:referenceData",
            "dataType": "nsg:dataType",
            "recordingModality": "nsg:recordingModality",
            "status": "nsg:status",
            "scoreType": "nsg:scoreType",
            "oldUUID": "nsg:providerId"
        }
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("authors", Person, "author", multiple=True, required=True),
        Field("description", str, "description", required=True),
        Field("date_created", (date, datetime), "dateCreated", required=True),
        Field("alias", str, "alias"),
        Field("brain_region", BrainRegion, "brainRegion", multiple=True),
        Field("species", Species, "species"),
        Field("celltype", CellType, "celltype", multiple=True),
        Field("test_type", str, "testType"),
        Field("age", Age, "age"),
        Field("reference_data", KGObject, "referenceData", multiple=True),  # to fix: should be a Collection?
        Field("data_type", str, "dataType"),
        Field("recording_modality", str, "recordingModality"),
        Field("score_type", str, "scoreType"),
        Field("status", str, "status"),
        Field("old_uuid", str, "oldUUID")
    )

    @property
    def scripts(self):
        query = {
            "nexus": {
                "path": "nsg:implements",
                "op": "eq",
                "value": self.id
            },
            "query": {
                "test_definition": self.id
            }
        }
        context = {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"
        }
        return KGQuery(ValidationScript, query, context)


class ValidationScript(KGObject):  # or ValidationImplementation
    """
    Code implementing a particular model validation test.

    See also: :class:`ValidationTestDefinition`, :class:`ValidationActivity`,
     :class:`ValidationResult`
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/validationscript/v0.1.0"
    type = ["prov:Entity", "nsg:ModelValidationScript"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "dateCreated": "schema:dateCreated",
            "repository": "schema:codeRepository",
            "version": "schema:version",
            "parameters": "nsg:parameters",
            "path": "nsg:path",
            "implements": "nsg:implements",
            "oldUUID": "nsg:providerId"
        }
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("date_created", (date, datetime), "dateCreated", required=True),
        Field("repository", IRI, "repository"),
        Field("version", str, "version"),
        Field("description", str, "description"),
        Field("parameters", str, "parameters"),
        Field("test_class", str, "path"),
        Field("test_definition", ValidationTestDefinition, "implements"),
        Field("old_uuid", str, "oldUUID")
    )


class ValidationResult(KGObject):
    """
    The results of running a model validation test.

    Including a numerical score, and optional additional data.

    See also: :class:`ValidationTestDefinition`, :class:`ValidationScript`,
    :class:`ValidationActivity`.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/validationresult/v0.1.0"
    #path = DEFAULT_NAMESPACE + "/simulation/validationresult/v0.1.1"
    type = ["prov:Entity", "nsg:ValidationResult"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "dateCreated": "schema:dateCreated",
            "score": "nsg:score",
            "normalizedScore": "nsg:normalizedScore",
            "passed": "nsg:passedValidation",
            "wasGeneratedBy": "prov:wasGeneratedBy",
            "hadMember": "prov:hadMember",
            "collabID": "nsg:collabID",
            "oldUUID": "nsg:providerId",
            "hash": "nsg:digest"
        }
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("generated_by", "brainsimulation.ValidationActivity", "wasGeneratedBy"),
        Field("description", str, "description"),
        Field("score", (float, int), "score"),
        Field("normalized_score", (float, int), "normalizedScore"),
        Field("passed", bool, "passedValidation"),
        Field("timestamp", (date, datetime), "dateCreated"),
        Field("additional_data", KGObject, "hadMember", multiple=True),
        Field("old_uuid", str, "oldUUID"),
        Field("collab_id", str, "collabID"),
        Field("hash", str, "hash")
    )


class ValidationActivity(KGObject):
    """
    Record of the validation of a model against experimental data.

    Links a :class:`ModelInstance`, a :class:`ValidationTestDefinition` and a
    reference data set to a :class:`ValidationResult`.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/modelvalidation/v0.2.0"  # only present in nexus-int
    type = ["prov:Activity", "nsg:ModelValidation"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "generated": "prov:generated",
            "used": "prov:used",
            "modelUsed": "prov:used",
            "testUsed": "prov:used",
            "dataUsed": "prov:used",
            "startedAtTime": "prov:startedAtTime",
            "endedAtTime": "prov:endedAtTime",
            "wasAssociatedWith": "prov:wasAssociatedWith",
            "referenceData": "nsg:referenceData"
        }
    ]
    fields = (
        Field("model_instance", (ModelInstance, MEModel), "modelUsed", required=True),
        Field("test_script", ValidationScript, "testUsed", required=True),
        Field("reference_data", Collection, "dataUsed", required=True),
        Field("timestamp", datetime, "startedAtTime", required=True),
        Field("result", ValidationResult, "generated"),
        Field("started_by", Person, "wasAssociatedWith"),
        Field("end_timestamp", datetime, "endedAtTime")
    )
    existence_query_fields = ("timestamp",)  # todo: add model_instance and test_script

    @property
    def duration(self):
        if self.end_timestamp:
            return self.end_timestamp - self.start_timestamp
        else:
            return 0.0

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, resolved=False):
        D = instance.data
        if resolved:
            D = cls._fix_keys(D)
        for otype in as_list(cls.type):
            if otype not in D["@type"]:
                # todo: profile - move compaction outside loop?
                compacted_types = compact_uri(D["@type"], standard_context)
                if otype not in compacted_types:
                    print("Warning: type mismatch {} - {}".format(otype, compacted_types))

        def filter_by_kg_type(items, type_name):
            filtered_items = []
            for item in as_list(items):
                if (type_name in item["@type"]
                    or type_name in compact_uri(item["@type"], standard_context)):
                    filtered_items.append(item)
            return filtered_items
        try:
            model_instance = filter_by_kg_type(D["modelUsed"], "nsg:ModelInstance")[0]
        except KeyError:
            model_instance = filter_by_kg_type(D["used"], "nsg:ModelInstance")[0]
        try:
            reference_data = filter_by_kg_type(D["dataUsed"], "nsg:Collection")[0]
        except KeyError:
            reference_data = filter_by_kg_type(D["used"], "nsg:Collection")[0]
        try:
            test_script = filter_by_kg_type(D["testUsed"], "nsg:ModelValidationScript")[0]
        except KeyError:
            test_script = filter_by_kg_type(D["used"], "nsg:ModelValidationScript")[0]
        end_timestamp = D.get("endedAtTime")
        if end_timestamp:
            end_timestamp = date_parser.parse(end_timestamp)
        obj = cls(model_instance=build_kg_object(None, model_instance),
                  test_script=build_kg_object(ValidationScript, test_script),
                  reference_data=build_kg_object(None, reference_data),
                  timestamp=date_parser.parse(D.get("startedAtTime")),
                  result=build_kg_object(ValidationResult, D.get("generated")),
                  started_by=build_kg_object(Person, D.get("wasAssociatedWith")),
                  end_timestamp=end_timestamp,
                  id=D["@id"],
                  instance=instance)
        return obj


class Simulation(KGObject):
    """
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/simulationactivity/v0.3.2"
    type = ["prov:Activity", "nsg:Simulation"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "schema": "http://schema.org/",
            "name": "schema:name",
            "identifier": "schema:identifier",
            "description": "schema:description",
            "prov": "http://www.w3.org/ns/prov#",
            "generated": "prov:generated",
            "used": "prov:used",
            "modelUsed": "prov:used",
            "configUsed": "prov:used",
            "envUsed": "prov:used",
            "startedAtTime": "prov:startedAtTime",
            "endedAtTime": "prov:endedAtTime",
            "wasAssociatedWith": "prov:wasAssociatedWith",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "referenceData": "nsg:referenceData",
            "tags": "nsg:tags",
            "resourceUsage": "nsg:resourceUsage",
            "status": "schema:actionStatus",
            "providerId": "nsg:providerId"
        }
    ]
    fields = (
        Field("name", str, "name"),
        Field("description", str, "description"),
        Field("identifier", str, "identifier"),
        Field("model_instance", (ModelInstance, MEModel), "modelUsed"),
        Field("config", "brainsimulation.SimulationConfiguration", "configUsed", multiple=True),
        Field("timestamp", datetime,  "startedAtTime"),
        Field("result", "brainsimulation.SimulationOutput", "generated", multiple=True),
        Field("started_by", Person, "wasAssociatedWith"),
        Field("end_timestamp",  datetime, "endedAtTime"),
        Field("computing_environment", ComputingEnvironment, "envUsed", required=False),
        Field("status", str, "status"),
        # should probably restrict to the enum https://schema.org/ActionStatusType
        Field("resource_usage", float, "resourceUsage"),
        Field("tags", str,  "tags", multiple=True),
        Field("job_id", str, "providerId")
    )
    existence_query_fields = ("timestamp", "model_instance", "simulation_config")  #, "computing_environment")


class SimulationConfiguration(KGObject):
    """
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/simulationconfiguration/v0.1.0"
    type = ["prov:Entity", "nsg:Entity", "nsg:SimulationConfiguration"]
    context = {"schema": "http://schema.org/",
               "name": "schema:name",
               "description": "schema:description",
               "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"}
    fields = (
        Field("name", str, "name", required=True),
        Field("identifier", str, "identifier"),
        Field("description", str, "description"),
        Field("config_file", (Distribution, str), "distribution")
    )

    def __init__(self,
                 name,
                 config_file=None,
                 description=None,
                 identifier=None,
                 id=None, instance=None):

        super(SimulationConfiguration, self).__init__(
            name=name,
            config_file=config_file,
            description=description,
            identifier=identifier,
            id=id,
            instance=instance)
        self._file_to_upload = None
        if isinstance(config_file, str):
            if config_file.startswith("http"):
                self.config_file = [Distribution(location=config_file)]
            elif os.path.isfile(config_file):
                self._file_to_upload = config_file
                self.config_file = None
        elif config_file is not None:
            for rf in as_list(self.config_file):
                assert isinstance(rf, Distribution)

    def save(self, client):
        super(SimulationConfiguration, self).save(client)
        if self._file_to_upload:
            self.upload_attachment(self._file_to_upload, client)

    def upload_attachment(self, file_path, client):
        upload_attachment(self, file_path, client)

    def download(self, local_directory, client):
        for rf in as_list(self.config_file):
            rf.download(local_directory, client)


class SimulationOutput(KGObject):
    """
    """
    namespace = DEFAULT_NAMESPACE
    type = ["prov:Entity", "nsg:Entity", "nsg:SimulationResult"]
    _path = "/simulation/simulationresult/v0.1.0"
    context = {"schema": "http://schema.org/",
               "name": "schema:name",
               "identifier": "schema:identifier",
               "description": "schema:description",
               "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
               "variable": "nsg:variable",
               "target": "nsg:target",
               "brainRegion": "nsg:brainRegion",
               "species": "nsg:species",
               "celltype": "nsg:celltype",
               "dataType": "nsg:dataType",
               "prov": "http://www.w3.org/ns/prov#",
               "startedAtTime": "prov:startedAtTime",
               "wasGeneratedBy": "prov:wasGeneratedBy",
               "wasDerivedFrom": "prov:wasDerivedFrom"}
    fields = (Field("name", str, "name", required=True),
              Field("description", str, "description"),
              Field("identifier", str, "identifier"),
              Field("result_file", (Distribution, str), "distribution"),
              Field("generated_by", Simulation, "wasGeneratedBy"),
              Field("derived_from", KGObject, "wasDerivedFrom", multiple=True),  # SHOULD BE SET UP  BY THE ACTIVITY
              Field("target", str, "target"),
              Field("data_type", str, "dataType"),
              Field("timestamp", datetime,  "startedAtTime"),
              Field("brain_region", BrainRegion, "brainRegion"),
              Field("species", Species, "species"),
              Field("celltype", CellType, "celltype"))

    def __init__(self,
                 name,
                 identifier=None,
                 result_file=None,
                 generated_by=None,
                 derived_from=None,
                 data_type = None,
                 variable=None,
                 target=None,
                 description=None,
                 timestamp=None,
                 brain_region=None, species=None, celltype=None,
                 id=None, instance=None):

        super(SimulationOutput, self).__init__(
            name=name,
            identifier=identifier,
            result_file=result_file,
            generated_by=generated_by,
            derived_from=derived_from,
            data_type=data_type,
            variable=variable,
            target=target,
            description=description,
            timestamp=timestamp,
            brain_region=brain_region,
            species=species,
            celltype=celltype,
            id=id,
            instance=instance)
        self._file_to_upload = None
        if isinstance(result_file, str):
            if result_file.startswith("http"):
                self.result_file = Distribution(location=result_file)
            elif os.path.isfile(result_file):
                self._file_to_upload = result_file
                self.result_file = None
        elif result_file is not None:
            for rf in as_list(self.result_file):
                assert isinstance(rf, Distribution)

    def save(self, client):
        super(SimulationOutput, self).save(client)
        if self._file_to_upload:
            self.upload_attachment(self._file_to_upload, client)

    def upload_attachment(self, file_path, client):
        upload_attachment(self, file_path, client)

    def download(self, local_directory, client):
        for rf in as_list(self.result_file):
            rf.download(local_directory, client)


def list_kg_classes():
    """List all KG classes defined in this module"""
    return [obj for name, obj in inspect.getmembers(sys.modules[__name__])
            if inspect.isclass(obj) and issubclass(obj, KGObject) and obj.__module__ == __name__]


def use_namespace(namespace):
    """Set the namespace for all classes in this module."""
    for cls in list_kg_classes():
        cls.namespace = namespace


class LivePaper(KGObject):
    """
    JSON data for generating live papers.
    """
    namespace = DEFAULT_NAMESPACE
    _path = "/simulation/livepaper/v0.0.1"
    type = ["prov:Entity", "nsg:LivePaper"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "name": "schema:name",
            "description": "schema:description",
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/",
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "http://schema.org/",
            "dateCreated": "schema:dateCreated",
            "dataObject": "schema:livePaperDataObject"
        }
    ]
    fields = (
        Field("name", str, "name", required=True),
        Field("description", str, "description", required=False),
        Field("date_created", (date, datetime), "dateCreated", required=True),
        Field("data_object", str, "dataObject", required=True), # stringify JSON object
    )

    @property
    def data(self):
        return json.loads(self.dataObject)

    @data.setter
    def data(self, dataObject):
        self.dataObject = json.dumps(dataObject)