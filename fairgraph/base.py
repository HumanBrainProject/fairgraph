"""

"""

import sys
from functools import wraps
from collections import defaultdict
import logging
from uuid import UUID
from six import with_metaclass
try:
    basestring
except NameError:
    basestring = str
from .errors import ResourceExistsError


logger = logging.getLogger("fairgraph")


registry = {
    'names': {},
    'types': {}
}

# todo: add namespaces to avoid name clashes, e.g. "Person" exists in several namespaces
def register_class(target_class):
    registry['names'][target_class.__name__] = target_class
    if hasattr(target_class, 'type'):
        if isinstance(target_class.type, basestring):
            registry['types'][target_class.type] = target_class
        else:
            registry['types'][tuple(target_class.type)] = target_class


def lookup(class_name):
    return registry['names'][class_name]


def lookup_type(class_type):
    return registry['types'][tuple(class_type)]


def generate_cache_key(qd):
    """From a query dict, generate an object suitable as a key for caching"""
    if not isinstance(qd, dict):
        raise TypeError("generate_cache_key expects a query dict. You provided '{}'".format(qd))
    cache_key = []
    for key in sorted(qd):
        value = qd[key]
        if isinstance(value, (list, tuple)):
            sub_key = []
            for sub_value in value:
                sub_key.append(generate_cache_key(sub_value))
            cache_key.append(tuple(sub_key))
        else:
            if not isinstance(value, (basestring, int, float)):
                raise TypeError("Expected a string, integer or float for key '{}', not a {}".format(key, type(value)))
            cache_key.append((key, value))
    return tuple(cache_key)


class Registry(type):
    """Metaclass for registering Knowledge Graph classes"""

    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


#class KGObject(object, metaclass=Registry):
class KGObject(with_metaclass(Registry, object)):
    """Base class for Knowledge Graph objects"""
    cache = {}
    save_cache = defaultdict(dict)

    def __init__(self, id=None, instance=None, **properties):
        for key, value in properties.items():
            if key not in self.property_names:
                raise TypeError("{self.__class__.__name__} got an unexpected keyword argument '{key}'".format(self=self, key=key))
            else:
                setattr(self, key, value)
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r} {self.id!r})'.format(self=self))

    @classmethod
    def from_kg_instance(self, instance, client, use_cache=True):
        raise NotImplementedError("To be implemented by child class")

    @classmethod
    def from_uri(cls, uri, client, use_cache=True, deprecated=False):
        return cls.from_kg_instance(client.instance_from_full_uri(uri,
                                                                  use_cache=use_cache,
                                                                  deprecated=deprecated),
                                    client,
                                    use_cache=use_cache)

    @classmethod
    def from_uuid(cls, uuid, client, deprecated=False):
        logger.info("Attempting to retrieve {} with uuid {}".format(cls.__name__, uuid))
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        val = UUID(uuid, version=4)  # check validity of uuid
        instance = client.instance_from_uuid(cls.path, uuid, deprecated=deprecated)
        if instance is None:
            return None
        else:
            return cls.from_kg_instance(instance, client)

    @property
    def uuid(self):
        return self.id.split("/")[-1]

    @classmethod
    def uri_from_uuid(cls, uuid, client):
        return "{}/data/{}/{}".format(client.nexus_endpoint, cls.path, uuid)

    @classmethod
    def list(cls, client, size=100, **filters):
        """List all objects of this type in the Knowledge Graph"""
        return client.list(cls, size=size)

    @property
    def _existence_query(self):
        # Note that this default implementation should in
        # many cases be over-ridden.
        # It assumes that "name" is unique within instances of a given type,
        # which may often not be the case.
        return {
            "path": "schema:name",
            "op": "eq",
            "value": self.name
        }

    def exists(self, client):
        """Check if this object already exists in the KnowledgeGraph"""
        if self.id:
            return True
        else:
            context = {"schema": "http://schema.org/",
                       "prov": "http://www.w3.org/ns/prov#"},
            query_filter = self._existence_query
            query_cache_key = generate_cache_key(query_filter)
            if query_cache_key in self.save_cache[self.__class__]:
                # Because the KnowledgeGraph is only eventually consistent, an instance
                # that has just been written to Nexus may not appear in the query.
                # Therefore we cache the query when creating an instance and
                # where exists() returns True
                self.id = self.save_cache[self.__class__][query_cache_key]
                return True
            else:
                response = client.filter_query(self.path, query_filter, context)
                if response:
                    self.id = response[0].data["@id"]
                    KGObject.save_cache[self.__class__][query_cache_key] = self.id
                return bool(response)

    def get_context(self, client):
        context_urls = set()
        if isinstance(self.context, dict):
            context_dict = self.context
        elif isinstance(self.context, (list, tuple)):
            context_dict = {}
            for item in self.context:
                if isinstance(item, dict):
                    context_dict.update(item)
                else:
                    assert isinstance(item, basestring)
                    if "{{base}}" in item:
                        context_urls.add(item.replace("{{base}}", client.nexus_endpoint))
                    else:
                        assert item.startswith("http")
                        context_urls.add(item)
        else:
            raise ValueError("Unexpected value for context")

        if self.instance:
            instance_context = self.instance.data["@context"]
            if isinstance(instance_context, dict):
                context_dict.update(instance_context)
            elif isinstance(instance_context, basestring):
                context_urls.add(instance_context)
            else:
                assert isinstance(instance_context, (list, tuple))
                for item in instance_context:
                    if isinstance(item, dict):
                        context_dict.update(item)
                    else:
                        assert isinstance(item, basestring) and item.startswith("http")
                        context_urls.add(item)

        context = list(context_urls) + [context_dict]
        if len(context) == 1:
            context = context[0]
        return context

    def _update_needed(self, data):
        for key, value in data.items():
            if key not in self.instance.data:
                return True
            elif self.instance.data[key] != value:
                return True
        return False

    def _build_data(self, client):
        raise NotImplementedError("to be implemented by child classes")

    def save(self, client):
        """docstring"""
        data = self._build_data(client)

        if self.id or self.exists(client):
            # note that calling self.exists() sets self.id if the object does exist
            if self.instance is None:
                # this can occur if updating a previously-saved object that has been constructed
                # (e.g. in a script), rather than retrieved from Nexus
                # since we don't know its current revision, we have to retrieve it
                self.instance = client.instance_from_full_uri(self.id, use_cache=False)

        if self.instance:
            if self._update_needed(data):
                logger.info("Updating {self!r}".format(self=self))
                self.instance.data.update(data)
                self.instance.data["@context"] = self.get_context(client)
                assert self.instance.data["@type"] == self.type
                self.instance = client.update_instance(self.instance)
            else:
                logger.info("Not updating {self!r}, unchanged".format(self=self))
        else:
            logger.info("Creating instance with data {}".format(data))
            data["@context"] = self.get_context(client)
            data["@type"] = self.type
            instance = client.create_new_instance(self.__class__.path, data)
            self.id = instance.data["@id"]
            self.instance = instance
            KGObject.cache[self.id] = self
            KGObject.save_cache[self.__class__][generate_cache_key(self._existence_query)] = self.id

    def delete(self, client):
        """Deprecate"""
        client.delete_instance(self.instance)

    @classmethod
    def by_name(cls, name, client):
        return client.by_name(cls, name)

    @property
    def rev(self):
        if self.instance:
            return self.instance.data.get("nxv:rev", None)
        else:
            return None

    def resolve(self, client):
        """To avoid having to check if a child attribute is a proxy or a real object,
        a real object resolves to itself.
        """
        return self


def cache(f):
    @wraps(f)
    def wrapper(cls, instance, client, use_cache=True):
        if use_cache and instance.data["@id"] in KGObject.cache:
            obj = KGObject.cache[instance.data["@id"]]
            #print(f"Found in cache: {obj.id}")
            return obj
        else:
            obj = f(cls, instance, client)
            KGObject.cache[obj.id] = obj
            #print(f"Added to cache: {obj.id}")
            return obj
    return wrapper


class OntologyTerm(object):
    """docstring"""

    def __init__(self, label, iri=None, strict=False):
        self.label = label
        self.iri = iri or self.iri_map.get(label)
        if strict:
            if self.iri is None:
                raise ValueError("No IRI found for label {}".format(label))

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.label!r}, {self.iri!r})')
        return ('{self.__class__.__name__}('
                '{self.label!r}, {self.iri!r})'.format(self=self))

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.label == other.label
                and self.iri == other.iri)

    def to_jsonld(self):
        return {'@id': self.iri,
                'label': self.label}

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        return cls(data["label"], data["@id"])


class KGProxy(object):
    """docstring"""

    def __init__(self, cls, uri):
        if isinstance(cls, basestring):
            self.cls = lookup(cls)
        else:
            self.cls = cls
        self.id = uri

    @property
    def type(self):
        return self.cls.type

    def resolve(self, client):
        """docstring"""
        if self.id in KGObject.cache:
            return KGObject.cache[self.id]
        else:
            obj = self.cls.from_uri(self.id, client)
            KGObject.cache[self.id] = obj
            return obj

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.cls!r}, {self.id!r})')
        return ('{self.__class__.__name__}('
                '{self.cls!r}, {self.id!r})'.format(self=self))

    @property
    def uuid(self):
        return self.id.split("/")[-1]

    def delete(self, client):
        """Delete the instance which this proxy represents"""
        obj = self.resolve(client)
        obj.delete(client)


class KGQuery(object):
    """docstring"""

    def __init__(self, cls, filter, context):
        if isinstance(cls, basestring):
            self.cls = lookup(cls)
        else:
            self.cls = cls
        self.filter = filter
        self.context = context

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.cls!r}, {self.filter!r})'.format(self=self))

    def resolve(self, client, size=10000):
        instances = client.filter_query(
            path=self.cls.path,
            filter=self.filter,
            context=self.context,
            size=size
        )
        objects = [self.cls.from_kg_instance(instance, client)
                   for instance in instances]
        for obj in objects:
            KGObject.cache[obj.id] = obj
        if len(instances) == 1:
            return objects[0]
        else:
            return objects


class Distribution(object):

    def __init__(self, location, size=None, digest=None, digest_method=None, content_type=None,
                 original_file_name=None):
        if not isinstance(location, basestring):
            # todo: add check that location is a URI
            raise ValueError("location must be a URI")
        self.location = location
        self.size = size
        self.digest = digest
        self.digest_method = digest_method
        self.content_type = content_type
        self.original_file_name = original_file_name

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "contentSize" in data:
            size = data["contentSize"]["value"]
            if data["contentSize"]["unit"] != "byte":
                raise NotImplementedError()
        else:
            size = None
        if "digest" in data:
            digest = data["digest"]["value"]
            digest_method = data["digest"]["algorithm"]
        else:
            digest = None
            digest_method = None
        return cls(data["downloadURL"], size, digest, digest_method, data.get("mediaType"),
                   data.get("originalFileName"))

    def to_jsonld(self, client):
        data = {
            "@context": "{{base}}/contexts/nexus/core/distribution/v0.1.0".replace("{{base}}", client.nexus_endpoint),
            "downloadURL": self.location
        }
        if self.size:
            data["contentSize"] = {
                "unit": "byte",
                "value": self.size
            }
        if self.digest:
            data["digest"]= {
                "algorithm": self.digest_method,  # e.g. "SHA-256"
                "value": self.digest
            },
        if self.content_type:
            data["mediaType"] = self.content_type
        if self.original_file_name:  # not sure if this is part of the schema, or just an annotation
            data["originalFileName"] = self.original_file_name
        return data


def build_kg_object(cls, data):
    """
    Build a KGObject, a KGProxy, or a list of such, based on the data provided.

    This takes care of the JSON-LD quirk that you get a list if there are multiple
    objects, but you get the object directly if there is only one.

    Returns `None` if data is None.
    """

    if data is None:
        return None

    if not isinstance(data, list):
        if not isinstance(data, dict):
            raise ValueError("data must be a list or dict")
        if "@list" in data:
            assert len(data) == 1
            data = data["@list"]
        else:
            data = [data]

    objects = []
    for item in data:
        if cls is None:
            # note that if cls is None, then the class can be different for each list item
            # therefore we need to use a new variable kg_cls inside the loop
            if "@type" in item:
                kg_cls = lookup_type(item["@type"])
            elif "label" in item:
                # we could possibly do a reverse lookup using iri_map of all the OntologyTerm
                # subclasses but for now just returning the base class
                kg_cls = OntologyTerm
            else:
                raise ValueError("Cannot determine type. Item was: {}".format(item))
        else:
            kg_cls = cls

        if issubclass(kg_cls, OntologyTerm):
            obj = kg_cls.from_jsonld(item)
        elif issubclass(kg_cls, KGObject):
            obj = KGProxy(kg_cls, item["@id"])
        elif kg_cls is Distribution:
            obj = kg_cls.from_jsonld(item)
        else:
            raise ValueError("cls must be a KGObject, OntologyTerm or Distribution")
        objects.append(obj)

    if len(objects) == 1:
        return objects[0]
    else:
        return objects


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
