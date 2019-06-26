"""
brain simulation
"""

import logging
import datetime
from dateutil import parser as date_parser
from .base import KGObject, cache, KGProxy, build_kg_object, Distribution, as_list, KGQuery
from .commons import BrainRegion, CellType, Species, AbstractionLevel, ModelScope
from .core import Organization, Person, Age

logger = logging.getLogger("fairgraph")

NAMESPACE = "neuralactivity"
#NAMESPACE = "brainsimulation"


class HasAliasMixin(object):

    @classmethod
    def from_alias(cls, alias, client):
        context = {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"
        }
        query = {
            "path": "nsg:alias",
            "op": "eq",
            "value": alias
        }
        return KGQuery(cls, query, context).resolve(client)


class ModelProject(KGObject, HasAliasMixin):
    """docstring"""
    path = NAMESPACE + "/simulation/modelproject/v0.1.0"
    #path = NAMESPACE + "/simulation/modelproject/v0.1.1"
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
        "partOf": "nsg:partOf"
    }

    attribute_map = {
        "model_of": (ModelScope, context["modelOf"]),
        "brain_region": (BrainRegion, context["brainRegion"]),
        "species": (Species, context["species"]),
        "celltype": (CellType, context["celltype"]),
        "abstraction_level": (AbstractionLevel, context["abstractionLevel"]),
    }

    def __init__(self, name, owners, authors, description, date_created, private, collab_id, alias=None,
                 organization=None, pla_components=None, brain_region=None, species=None, celltype=None,
                 abstraction_level=None, model_of=None, old_uuid=None, parents=None, instances=None, images=None,
                 id=None, instance=None):
        self.name = name
        self.alias = alias
        self.brain_region = brain_region
        self.species = species
        self.celltype = celltype
        self.organization = organization
        self.abstraction_level = abstraction_level
        self.private = private
        self.authors = authors  # rename 'contributors', for consistency with MINDS?
        self.owners = owners
        self.description = description
        self.collab_id = collab_id
        self.PLA_components = pla_components
        self.date_created = date_created
        self.model_of = model_of
        self.old_uuid = old_uuid
        self.images = images
        self.parents = parents
        self.instances = instances
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.brain_region!r}, '
                '{self.celltype!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:ModelProject' in D["@type"]
        obj = cls(name=D["name"],
                  owners=None,
                  authors=[],
                  collab_id=D["collabID"], description=D["description"], private=D["private"],
                  date_created=D["dateCreated"],
                  organization=build_kg_object(Organization, D.get("organization")),
                  pla_components=D.get("PLAComponents", None),
                  alias=D.get("alias", None),
                  model_of=build_kg_object(ModelScope, D.get("modelOf")),
                  brain_region=build_kg_object(BrainRegion, D.get("brainRegion")),
                  species=build_kg_object(Species, D.get("species")),
                  celltype=build_kg_object(CellType, D.get("celltype")),
                  abstraction_level=build_kg_object(AbstractionLevel, D.get("abstractionLevel")),
                  old_uuid=D.get("oldUUID", None),
                  parents=build_kg_object(ModelProject, D.get("partOf")),
                  instances=build_kg_object(None, D.get("dcterms:hasPart")),
                  images=D.get("images"),
                  id=D["@id"], instance=instance)
        if isinstance(D["author"], str):  # temporary, this shouldn't happen once migration complete
            obj.authors = D["author"]
        else:
            obj.authors = build_kg_object(Person, D["author"])
        if "owner" in D:
            if isinstance(D["owner"], str):  # temporary, this shouldn't happen once migration complete
                raise Exception()
                obj.owner = D["owner"]
            else:
                obj.owners = build_kg_object(Person, D["owner"])
        return obj

    def _build_data(self, client):
        # if self.instance:
        #     data = self.instance.data
        #     # the following 4 lines are a temporary hack, due to dcterms being missing in the standard context
        #     if isinstance(data["@context"], list):
        #         data["@context"].append(self.get_context(client))
        #     else:
        #         data["@context"].update(self.get_context(client))
        # else:
        #     data = {
        #         "@context": self.get_context(client),
        #         "@type": self.type
        #     }
        data = {}
        if self.authors:
            if isinstance(self.authors, str):  # temporary, should convert into Person
                raise Exception()
                #data["author"] = self.authors
            else:
                data["author"] = [
                    {
                        "@type": person.type,
                        "@id": person.id
                    } for person in as_list(self.authors)
                ]
        if self.owners:
            owners = as_list(self.owners)
            for owner in owners:
                if owner.id is None:
                    owner.save(client)
            if len(owners) == 1:
                data["owner"] = {
                    "@type": owners[0].type,
                    "@id": owners[0].id
                }
            else:
                data["owner"] = [
                    {
                        "@type": owner.type,
                        "@id": owner.id
                    } for owner in owners
                ]
        data["name"] = self.name
        data["collabID"] = self.collab_id
        data["description"] = self.description
        data["private"] = self.private
        if type(self.date_created) is datetime.date or type(self.date_created) is datetime.datetime:
            data["dateCreated"] = self.date_created.isoformat()
        else:
            data["dateCreated"] = self.date_created
        if self.organization is not None:
            if isinstance(self.organization, list):
                data["organization"] = [
                    {
                        "@type": org.type,
                        "@id": org.id,
                    } for org in self.organization
                 ]
            else:
                if self.organization.id is None:
                    self.organization.save(client)
                data["organization"] = {
                    "@type": self.organization.type,
                    "@id": self.organization.id
                }
        if self.PLA_components is not None:
            data["PLAComponents"] = self.PLA_components
        if self.alias is not None:
            data["alias"] = self.alias
        if self.model_of is not None:
            data["modelOf"] = self.model_of.to_jsonld()
        if self.brain_region is not None:
            if isinstance(self.brain_region, list):
                data["brainRegion"] = [br.to_jsonld() for br in self.brain_region]
            else:
                data["brainRegion"] = self.brain_region.to_jsonld()
        if self.species is not None:
            if isinstance(self.species, list):
                data["species"] = [s.to_jsonld() for s in self.species]
            else:
                data["species"] = self.species.to_jsonld()
        if self.celltype is not None:
            if isinstance(self.celltype, list):
                data["celltype"] = [ct.to_jsonld() for ct in self.celltype]
            else:
                data["celltype"] = self.celltype.to_jsonld()
        if self.abstraction_level is not None:
            if isinstance(self.abstraction_level, list):
                data["abstractionLevel"] = [al.to_jsonld() for al in self.abstraction_level]
            else:
                data["abstractionLevel"] = self.abstraction_level.to_jsonld()
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        if self.parents:
            data["partOf"] = [{
                "@type": parent.type,
                "@id": parent.id
            } for parent in as_list(self.parents)]
        if self.instances is not None:
            data["dcterms:hasPart"] = [
                {
                    "@type": obj.type,
                    "@id": obj.id
                } for obj in as_list(self.instances)
            ]
        if self.images is not None:
            data["images"] = self.images
        return data

    @classmethod
    def list(cls, client, size=10000, **filters):
        """List all objects of this type in the Knowledge Graph"""
        context = {
           'nsg': 'https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/'
        }
        filter_queries = []
        for name, value in filters.items():
            if name in cls.attribute_map:
                concept_class, concept_uri = cls.attribute_map[name]
                filter_queries.append({
                    'path': concept_uri,
                    'op': 'eq',
                    'value': concept_class(value).iri
                })
            else:
                raise Exception("The only supported filters are by {supported_filters}"
                                "You specified {name}".format(supported_filters=", ".join(cls.attribute_map), name=name))
        if len(filter_queries) == 0:
            return client.list(cls, size=size)
        elif len(filter_queries) == 1:
            filter_query = filter_queries[0]
        else:
            filter_query = {
                "op": "and",
                "value": filter_queries
            }
        return KGQuery(cls, filter_query, context).resolve(client, size=size)

    def authors_str(self, client):
        return ", ".join("{obj.given_name} {obj.family_name}".format(obj=obj.resolve(client)) for obj in self.authors)

    #def sub_projects(self):


class ModelInstance(KGObject):
    """docstring"""
    #path = NAMESPACE + "/simulation/modelinstance/v0.1.2"
    path = NAMESPACE + "/simulation/modelinstance/v0.1.1"
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
        {"oldUUID": "nsg:providerId"}
    ]
    # fields:
    #  - fields of ModelInstance + eModel, morphology, mainModelScript, isPartOf (an MEModelRelease)

    def __init__(self, name, brain_region, species, model_of,
                 main_script, release, version, timestamp,
                 part_of=None, description=None, parameters=None,
                 old_uuid=None, id=None, instance=None):
        self.name = name
        self.description = description
        self.brain_region = brain_region
        self.species = species
        self.model_of = model_of
        self.main_script = main_script
        self.release = release
        self.version = version
        self.timestamp = timestamp
        self.part_of = part_of
        self.parameters = parameters
        self.old_uuid = old_uuid
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.brain_region!r}, '
                '{self.model_of!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:ModelInstance' in D["@type"]
        obj = cls(name=D["name"],
                  model_of=build_kg_object(None, D.get("modelOf")),
                  #model_of = D.get("modelOf", None),
                  brain_region=build_kg_object(BrainRegion, D.get("brainRegion")),
                  species=build_kg_object(Species, D.get("species")),
                  main_script=build_kg_object(ModelScript, D["mainModelScript"]),
                  release=D.get("release"),  # to fix once we define MEModelRelease class
                  version=D.get("version"),
                  timestamp=date_parser.parse(D.get("generatedAtTime"))
                            if "generatedAtTime" in D else None,
                  #part_of=build_kg_object(ModelRelease, D.get("isPartOf")),
                  description=D.get("description"),
                  parameters=D.get("nsg:parameters"),
                  old_uuid=D.get("oldUUID"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.model_of:
            data["modelOf"] = self.model_of.to_jsonld()
        if self.brain_region:
            data["brainRegion"] = self.brain_region.to_jsonld()
        if self.species:
            data["species"] = self.species.to_jsonld()
        if self.description:
            data["description"] = self.description
        if self.main_script:
            data["mainModelScript"] = {
                "@id": self.main_script.id,
                "@type": self.main_script.type
            }
        if self.version:
            data["version"] = self.version
        if self.timestamp:
            data["generatedAtTime"] = self.timestamp.isoformat()
        if self.part_of:
            data["isPartOf"] = {
                "@id": self.part_of.id,
                "@type": self.part_of.type
            }
        if self.release:
            data["release"] = self.release
        if self.parameters:
            data["nsg:parameters"] = self.parameters
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        return data

    @property
    def project(self):
        query = {
            "path": "dcterms:hasPart",
            "op": "eq",
            "value": self.id
        }
        context = {
            "dcterms": "http://purl.org/dc/terms/"
        }
        return KGQuery(ModelProject, query, context)


class MEModel(ModelInstance):
    """docstring"""
    path = NAMESPACE + "/simulation/memodel/v0.1.2"  # latest is 0.1.4, but all the data is currently under 0.1.2
    type = ["prov:Entity", "nsg:MEModel", "nsg:ModelInstance"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {"oldUUID": "nsg:providerId"}
    ]
    # fields:
    #  - fields of ModelInstance + eModel, morphology, mainModelScript, isPartOf (an MEModelRelease)

    def __init__(self, name, brain_region, species, model_of, e_model,
                 morphology, main_script, release, version, timestamp, project,
                 part_of=None, description=None, parameters=None,
                 old_uuid=None, id=None, instance=None):
        self.name = name
        self.description = description
        self.brain_region = brain_region
        self.species = species
        self.model_of = model_of
        self.e_model = e_model
        self.morphology = morphology
        self.main_script = main_script
        self.release = release
        self.version = version
        self.timestamp = timestamp
        #self.project = project  # conflict with project property in parent class. To fix.
        self.part_of = part_of
        self.parameters = parameters
        self.old_uuid = old_uuid
        self.id = id
        self.instance = instance

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:MEModel' in D["@type"]
        obj = cls(name=D["name"],
                  model_of=build_kg_object(None, D.get("modelOf")),
                  #model_of = D.get("modelOf", None),
                  brain_region=build_kg_object(BrainRegion, D.get("brainRegion")),
                  species=build_kg_object(Species, D.get("species")),
                  e_model=build_kg_object(EModel, D["eModel"]),
                  morphology=build_kg_object(Morphology, D["morphology"]),
                  main_script=build_kg_object(ModelScript, D["mainModelScript"]),
                  release=D.get("release"),  # to fix once we define MEModelRelease class
                  version=D.get("version"),
                  timestamp=date_parser.parse(D.get("generatedAtTime"))
                            if "generatedAtTime" in D else None,
                  project=build_kg_object(ModelProject, D.get("isPartOf")),
                  #part_of=build_kg_object(ModelRelease, D.get("isPartOf")),
                  description=D.get("description"),
                  parameters=D.get("nsg:parameters"),
                  old_uuid=D.get("oldUUID"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.model_of:
            data["modelOf"] = self.model_of.to_jsonld()
        if self.brain_region:
            data["brainRegion"] = self.brain_region.to_jsonld()
        if self.species:
            data["species"] = self.species.to_jsonld()
        if self.description:
            data["description"] = self.description
        data["eModel"] = {
            "@id": self.e_model.id,
            "@type": self.e_model.type
        }
        data["morphology"] = {
            "@id": self.morphology.id,
            "@type": self.morphology.type
        }
        if self.main_script:
            data["mainModelScript"] = {
                "@id": self.main_script.id,
                "@type": self.main_script.type
            }
        if self.version:
            data["version"] = self.version
        if self.timestamp:
            data["generatedAtTime"] = self.timestamp.isoformat()
        if self.part_of:
            data["isPartOf"] = {
                "@id": self.part_of.id,
                "@type": self.part_of.type
            }
        # if self.project:
        #     data["project"] = {
        #         "@id": self.project.id,
        #         "@type": self.project.type
        #     }
        if self.release:
            data["release"] = self.release
        if self.parameters:
            data["nsg:parameters"] = self.parameters
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        return data


class Morphology(KGObject):
    path = NAMESPACE + "/simulation/morphology/v0.1.1"
    type = ["prov:Entity", "nsg:Morphology"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0"
    ]

    #name, distribution
    def __init__(self, name, cell_type=None, morphology_file=None, distribution=None, id=None, instance=None):
        self.name = name
        self.cell_type = cell_type
        self.distribution = distribution
        if morphology_file:
            if distribution:
                raise ValueError("Cannot provide both morphology_file and distribution")
            self.morphology_file = morphology_file
        self.id = id
        self.instance = instance

    @property
    def morphology_file(self):
        if isinstance(self.distribution, list):
            return [d.location for d in self.distribution]
        else:
            return self.distribution.location

    @morphology_file.setter
    def morphology_file(self, value):
        if isinstance(value, list):
            self.distribution = [Distribution(location=mf) for mf in value]
        else:
            self.distribution = Distribution(location=value)

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:Morphology' in D["@type"]
        obj = cls(name=D["name"],
                  cell_type=D.get("modelOf", None),
                  distribution=build_kg_object(Distribution, D.get("distribution")),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.cell_type:
            data["modelOf"] = self.cell_type.to_jsonld()
        if isinstance(self.distribution, list):
            data["distribution"] = [item.to_jsonld(client) for item in self.distribution]
        elif self.distribution is not None:
            data["distribution"] = self.distribution.to_jsonld(client)
        return data


class ModelScript(KGObject):
    path = NAMESPACE + "/simulation/emodelscript/v0.1.0"
    type = ["prov:Entity", "nsg:EModelScript"]  # generalize to other sub-types of script
    context =  [  # todo: root should be set by client to nexus or nexus-int or whatever as required
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0",
        {
            "license": "schema:license"
        }
    ]

    def __init__(self, name, code_location=None, code_format=None, license=None,
                 distribution=None, id=None, instance=None):
        self.name = name
        self.distribution = distribution
        self.code_format = code_format
        self.license = license
        self.id = id
        self.instance = instance
        if code_location and distribution:
            raise ValueError("Cannot provide both code_location and distribution")
        if code_location:
            self.distribution = Distribution(location=code_location)
        if distribution is not None:
            assert isinstance(self.distribution, Distribution)

    @property
    def code_location(self):
        if self.distribution:
            return self.distribution.location
        else:
            return None

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:EModelScript' in D["@type"]  # generalise
        obj = cls(name=D["name"],
                  distribution=build_kg_object(Distribution, D.get("distribution")),
                  license=D.get("license"),
                  code_format=D.get("code_format"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if isinstance(self.distribution, list):
            data["distribution"] = [item.to_jsonld(client) for item in self.distribution]
        elif self.distribution is not None:
            data["distribution"] = self.distribution.to_jsonld(client)
        data["license"] = self.license
        data["code_format"] = self.code_format
        return data


class EModel(ModelInstance):
    path = NAMESPACE + "/simulation/emodel/v0.1.1"
    type = ["prov:Entity", "nsg:EModel"]
    context = [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0"
    ]


    # model_script, name, species, subCellularMechanism
    def __init__(self, name, brain_region, species, model_of,
                 main_script, release, id=None, instance=None):
        self.name = name
        self.brain_region = brain_region
        self.species = species
        self.model_of = model_of
        self.main_script = main_script
        self.release = release
        self.id = id
        self.instance = instance

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:EModel' in D["@type"]
        obj = cls(name=D["name"],
                  model_of=build_kg_object(D.get("modelOf", None)),
                  #model_of=D.get("modelOf", None),
                  brain_region=build_kg_object(BrainRegion, D.get("brainRegion")),
                  species=build_kg_object(Species, D.get("species")),
                  main_script=build_kg_object(ModelScript, D["modelScript"]),
                  release=D.get("release"),  # to fix once we define MEModelRelease class
                  id=D["@id"], instance=instance)
        return obj


    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.model_of:
            data["modelOf"] = {
                "@type": self.model_of.type,
                "@id": self.model_of.id
            }
        if self.brain_region:
            data["brainRegion"] = self.brain_region.to_jsonld()
        if self.species:
            data["species"] = self.species.to_jsonld()
        if self.main_script:
            data["modelScript"] = {
                "@id": self.main_script.id,
                "@type": self.main_script.type
            }
        if self.release:
            data["release"] = self.release
        return data


class AnalysisResult(KGObject):
    path = NAMESPACE + "/simulation/analysisresult/v1.0.0"
    type = ["prov:Entity", "nsg:Entity", "nsg:AnalysisResult"]
    context =  [
        "{{base}}/contexts/neurosciencegraph/core/data/v0.3.1",
        "{{base}}/contexts/nexus/core/resource/v0.3.0"
    ]

    def __init__(self, name, distribution=None, timestamp=None, id=None, instance=None):
        self.name = name
        self.distribution = distribution
        self.timestamp = timestamp
        self.id = id
        self.instance = instance
        if distribution is not None:
            assert isinstance(self.distribution, Distribution)

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:AnalysisResult' in D["@type"]
        obj = cls(name=D["name"],
                  distribution=build_kg_object(Distribution, D.get("distribution")),
                  timestamp=date_parser.parse(D.get("generatedAtTime"))
                            if "generatedAtTime" in D else None,
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        """docstring"""
        data = {}
        data["name"] = self.name
        if self.timestamp:
            data["generatedAtTime"] = self.timestamp.isoformat()
        if isinstance(self.distribution, list):
            data["distribution"] = [item.to_jsonld(client) for item in self.distribution]
        elif self.distribution is not None:
            data["distribution"] = self.distribution.to_jsonld(client)
        return data


class ValidationTestDefinition(KGObject, HasAliasMixin):
    """docstring"""
    path = NAMESPACE + "/simulation/validationtestdefinition/v0.1.0"
    #path = NAMESPACE + "/simulation/validationtestdefinition/v0.1.2"
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

    def __init__(self, name, authors, description, date_created, alias=None,
                 brain_region=None, species=None, celltype=None, test_type=None,
                 age=None, reference_data=None, data_type=None, recording_modality=None,
                 score_type=None, status=None, old_uuid=None,
                 id=None, instance=None):
        self.name = name
        self.alias = alias
        self.brain_region = brain_region
        self.species = species
        self.celltype = celltype
        self.authors = authors  # rename 'contributors', for consistency with MINDS?
        self.description = description
        self.date_created = date_created
        self.test_type = test_type
        self.age = age
        self.reference_data = reference_data
        self.data_type = data_type
        self.recording_modality = recording_modality
        self.score_type = score_type
        self.status = status
        self.old_uuid = old_uuid
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.brain_region!r}, '
                '{self.celltype!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:ValidationTestDefinition' in D["@type"]
        obj = cls(name=D["name"],
                  authors=build_kg_object(Person, D["author"]),
                  description=D.get("description", ""),
                  date_created=D["dateCreated"],
                  alias=D.get("alias", None),
                  test_type=D.get("testType"),
                  brain_region=build_kg_object(BrainRegion, D.get("brainRegion")),
                  species=build_kg_object(Species, D.get("species")),
                  celltype=build_kg_object(CellType, D.get("celltype")),
                  age=Age.from_jsonld(D.get("age")),
                  reference_data=build_kg_object(None, D.get("referenceData")),
                  data_type=D.get("dataType"),
                  recording_modality=D.get("recordingModality"),
                  score_type=D.get("scoreType"),
                  status=D.get("status"),
                  old_uuid=D.get("oldUUID"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        data = {}
        if self.authors:
            for author in as_list(self.authors):
                if not author.id:
                    author.save(client)
            data["author"] = [
                {
                    "@type": person.type,
                    "@id": person.id
                } for person in as_list(self.authors)
            ]
        data["name"] = self.name
        data["description"] = self.description
        if type(self.date_created) is datetime.date or type(self.date_created) is datetime.datetime:
            data["dateCreated"] = self.date_created.isoformat()
        else:
            data["dateCreated"] = self.date_created
        if self.alias is not None:
            data["alias"] = self.alias
        if self.test_type is not None:
            data["testType"] = self.test_type
        if self.brain_region is not None:
            if isinstance(self.brain_region, list):
                data["brainRegion"] = [br.to_jsonld() for br in self.brain_region]
            else:
                data["brainRegion"] = self.brain_region.to_jsonld()
        if self.species is not None:
            if isinstance(self.species, list):
                data["species"] = [s.to_jsonld() for s in self.species]
            else:
                data["species"] = self.species.to_jsonld()
        if self.celltype is not None:
            if isinstance(self.celltype, list):
                data["celltype"] = [ct.to_jsonld() for ct in self.celltype]
            else:
                data["celltype"] = self.celltype.to_jsonld()
        if self.age is not None:
            data["age"] = self.age.to_jsonld()
        if self.reference_data is not None:
            data["referenceData"] = [{
                "@type": item.type,
                "@id": item.id
            } for item in as_list(self.reference_data)]
        # todo: if we're auto-saving authors, should do the same for reference data
        if self.data_type is not None:
            data["dataType"] = self.data_type
        if self.recording_modality is not None:
            data["recordingModality"] = self.recording_modality
        if self.status is not None:
            data["status"] = self.status
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        return data

    @property
    def scripts(self):
        query = {
            "path": "nsg:implements",
            "op": "eq",
            "value": self.id
        }
        context = {
            "nsg": "https://bbp-nexus.epfl.ch/vocabs/bbp/neurosciencegraph/core/v0.1.0/"
        }
        return KGQuery(ValidationScript, query, context)


class ValidationScript(KGObject):  # or ValidationImplementation
    """docstring"""
    path = NAMESPACE + "/simulation/validationscript/v0.1.0"
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

    def __init__(self, name, date_created,
                 repository=None, version=None,
                 description=None, parameters=None,
                 test_class=None, test_definition=None,
                 old_uuid=None, id=None, instance=None):
        self.name = name
        self.description = description
        self.date_created = date_created
        self.repository = repository
        self.version = version
        self.parameters = parameters
        self.test_class = test_class
        self.test_definition = test_definition
        self.old_uuid = old_uuid
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.repository!r}, '
                '{self.version!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:ModelValidationScript' in D["@type"]
        obj = cls(name=D["name"],
                  description=D.get("description", ""),
                  date_created=D["dateCreated"],
                  repository=D.get("repository")["@id"] if "repository" in D else None,
                  version=D.get("version"),
                  parameters=D.get("parameters"),
                  test_class=D.get("path"),
                  test_definition=build_kg_object(ValidationTestDefinition, D.get("implements")),
                  old_uuid=D.get("oldUUID"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        data = {}
        data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if isinstance(self.date_created, (datetime.date, datetime.datetime)):
            data["dateCreated"] = self.date_created.isoformat()
        else:
            raise ValueError("date_created must be a date or datetime object")
        if self.repository is not None:
            data["repository"] = {"@id": self.repository}
        if self.version is not None:
            data["version"] = self.version
        if self.parameters is not None:
            data["parameters"] = self.parameters
        if self.test_class is not None:
            data["path"] = self.test_class
        if self.test_definition is not None:
            data["implements"] = {
                "@type": self.test_definition.type,
                "@id": self.test_definition.id
            }
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        return data


class ValidationResult(KGObject):
    """docstring"""
    path = NAMESPACE + "/simulation/validationresult/v0.1.0"
    #path = NAMESPACE + "/simulation/validationresult/v0.1.1"
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
            "oldUUID": "nsg:providerId"
        }
    ]

    def __init__(self, name, generated_by=None, description=None,
                 score=None, normalized_score=None, passed=None,
                 timestamp=None, additional_data=None, old_uuid=None,
                 collab_id=None, id=None, instance=None):
        self.name = name
        self.generated_by = generated_by
        self.description = description
        self.score = score
        self.normalized_score = normalized_score
        self.passed = passed
        self.timestamp = timestamp
        self.additional_data = additional_data
        self.old_uuid = old_uuid
        self.collab_id = collab_id
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r}, {self.generated_by!r}, '
                '{self.score!r}, {self.id})'.format(self=self))

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client, use_cache=True):
        D = instance.data
        assert 'nsg:ValidationResult' in D["@type"]
        obj = cls(name=D["name"],
                  generated_by=build_kg_object(ValidationActivity, D.get("wasGeneratedBy")),
                  description=D.get("description", ""),
                  timestamp=D["dateCreated"],
                  score=D.get("score"),
                  normalized_score=D.get("normalizedScore"),
                  passed=D.get("passedValidation"),
                  additional_data=build_kg_object(None, D.get("hadMember")),
                  old_uuid=D.get("oldUUID"),
                  id=D["@id"], instance=instance)
        return obj

    def _build_data(self, client):
        data = {}
        data["name"] = self.name
        if self.description is not None:
            data["description"] = self.description
        if isinstance(self.timestamp, (datetime.date, datetime.datetime)):
            data["dateCreated"] = self.timestamp.isoformat()
        else:
            raise ValueError("timestamp must be a date or datetime object")
        if self.score is not None:
            data["score"] = self.score
        if self.normalized_score is not None:
            data["normalizedScore"] = self.normalized_score
        if self.passed is not None:
            data["passedValidation"] = self.passed
        if self.generated_by is not None:
            data["wasGeneratedBy"] = {
                "@type": self.generated_by.type,
                "@id": self.generated_by.id
            }
        if self.additional_data is not None:
            data["hadMember"] = [{
                "@type": obj.type,
                "@id": obj.id
            } for obj in as_list(self.additional_data)]
        if self.old_uuid:
            data["oldUUID"] = self.old_uuid
        return data


class ValidationActivity(KGObject):
    """docstring"""
    path = NAMESPACE + "/simulation/modelvalidation/v0.2.0"
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
            "startedAtTime": "prov:startedAtTime",
            "wasAssociatedWith": "prov:wasAssociatedWith",
            "referenceData": "nsg:referenceData"
        }
    ]

    def __init__(self, model_instance, test_script, reference_data, timestamp,
                 result=None, started_by=None, id=None, instance=None):
        self.model_instance = model_instance
        self.test_script = test_script
        self.reference_data = reference_data
        self.timestamp = timestamp
        self.result = result
        self.started_by = started_by
        self.id = id
        self.instance = instance


    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.model_instance!r}, '
                '{self.test_script!r} {self.reference_data!r}, '
                '{self.id})'.format(self=self))

    @property
    def _existence_query(self):
        # to fix: need an _and_ on model_instance, test_script, reference_data and timestamp
        return {
            "path": "prov:startedAtTime",
            "op": "eq",
            "value": self.timestamp.isoformat()
        }

    @classmethod
    @cache
    def from_kg_instance(cls, instance, client):
        D = instance.data
        assert 'nsg:ModelValidation' in D["@type"]
        model_instance = [item for item in D.get("used") if "nsg:ModelInstance" in item["@type"]][0]
        reference_data = [item for item in D.get("used") if "nsg:Collection" in item["@type"]][0]
        test_script = [item for item in D.get("used") if "nsg:ModelValidationScript" in item["@type"]][0]
        obj = cls(model_instance=build_kg_object(None, model_instance),
                  test_script=build_kg_object(ValidationScript, test_script),
                  reference_data=build_kg_object(None, reference_data),
                  timestamp=D.get("startedAtTime", None),
                  result=build_kg_object(ValidationResult, D.get("result")),
                  started_by=build_kg_object(Person, D.get("wasAssociatedWith")),
                  id=D["@id"],
                  instance=instance)
        return obj

    def _build_data(self, client):
        data = {}
        if isinstance(self.timestamp, (datetime.date, datetime.datetime)):
            data["startedAtTime"] = self.timestamp.isoformat()
        else:
            raise ValueError("timestamp must be a date or datetime object")
        data["used"] = [
            {"@id": self.model_instance.id, "@type": self.model_instance.type},
            {"@id": self.test_script.id, "@type": self.test_script.type},
            {"@id": self.reference_data.id, "@type": self.reference_data.type}
        ]
        if self.started_by is not None:
            data["wasAssociatedWith"] = [{
                "@type": agent.type,
                "@id": agent.id
            } for agent in self.started_by]
        if self.result is not None:
            data["generated"] = {
                "@type": self.result.type,
                "@id": self.result.id
            }
        return data
