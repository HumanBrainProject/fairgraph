"""
define client
"""

import json
import logging
try:
    from urllib.parse import urlparse, quote_plus
except ImportError:  # Python 2
    from urlparse import urlparse
    from urllib import quote_plus
from openid_http_client.auth_client.access_token_client import AccessTokenClient
from pyxus.client import NexusClient
from pyxus.resources.entity import Instance
from .core import Organization
from .electrophysiology import PatchClampExperiment


CURL_LOGGER = logging.getLogger("curl")
CURL_LOGGER.setLevel(logging.WARNING)
logger = logging.getLogger("fairgraph")


class KGClient(object):
    """docstring"""

    def __init__(self, token, nexus_endpoint="https://nexus.humanbrainproject.org/v0"):
        ep = urlparse(nexus_endpoint)
        self.nexus_endpoint = nexus_endpoint
        self._nexus_client = NexusClient(scheme=ep.scheme, host=ep.netloc, prefix=ep.path[1:],
                                         alternative_namespace=nexus_endpoint,
                                         auth_client=AccessTokenClient(token))
        self._instance_repo = self._nexus_client.instances
        self.cache = {}  # todo: use combined uri and rev as cache keys


    def list(self, cls, from_index=0, size=100, deprecated=False):
        """docstring"""
        instances = []
        query = self._nexus_client.instances.list_by_schema(*cls.path.split("/"),
                                                            from_index=from_index,
                                                            size=size,
                                                            deprecated=deprecated,
                                                            resolved=True)
        # todo: add support for "sort" field
        instances.extend(query.results)
        next = query.get_next_link()
        while len(instances) < size and next:
            query = self._nexus_client.instances.list_by_full_path(next)
            instances.extend(query.results)
            next = query.get_next_link()

        for instance in instances:
            self.cache[instance.data["@id"]] = instance
        return [cls.from_kg_instance(instance, self) # todo: lazy resolution
                for instance in instances]

    def filter_query(self, path, filter, context, from_index=0, size=100, deprecated=False):
        instances = []
        query = self._nexus_client.instances.list(
            subpath=path,
            filter_query=quote_plus(json.dumps(filter)),
            context=quote_plus(json.dumps(context)),
            from_index=from_index,
            size=size,
            deprecated=deprecated,
            resolved=True)
        # todo: add support for "sort" field
        instances.extend(query.results)
        next = query.get_next_link()
        while len(instances) < size and next:
            query = self._nexus_client.instances.list_by_full_path(next)
            instances.extend(query.results)
            next = query.get_next_link()

        for instance in instances:
            self.cache[instance.data["@id"]] = instance
        return instances

    def instance_from_full_uri(self, uri, use_cache=True, deprecated=False):
        # 'deprecated=True' means 'returns an instance even if that instance is deprecated'
        # should perhaps be called 'show_deprecated' or 'include_deprecated'
        if use_cache and uri in self.cache:
            logger.debug("Retrieving instance from cache")
            instance = self.cache[uri]
        else:
            instance = Instance(Instance.extract_id_from_url(uri, self._instance_repo.path),
                                data=self._instance_repo._http_client.get(uri),
                                root_path=Instance.path)
            self.cache[instance.data["@id"]] = instance
            logger.debug("Retrieved instance from KG " + str(instance.data))
        if instance and deprecated is False and instance.data["nxv:deprecated"]:
            return None
        else:
            return instance

    def instance_from_uuid(self, path, uuid, deprecated=False):
        # todo: caching
        instance = self._instance_repo.read_by_full_id(path + "/" + uuid)
        if instance and deprecated is False and instance.data["nxv:deprecated"]:
            return None
        else:
            return instance

    def create_new_instance(self, path, data):
        instance = Instance(path, data, Instance.path)
        entity = self._nexus_client.instances.create(instance)
        entity.data.update(data)
        return entity

    def update_instance(self, instance):
        instance.data.pop("links", None)
        instance.data.pop("nxv:rev", None)
        instance.data.pop("nxv:deprecated", None)
        instance = self._nexus_client.instances.update(instance)
        return instance

    def delete_instance(self, instance):
        self._nexus_client.instances.delete(instance)
        if instance.id in self.cache:
            self.cache.pop(instance.id)

    def by_name(self, cls, name):
        """Retrieve an object based on the value of schema:name"""
        context = {"schema": "http://schema.org/"}
        query_filter = {
            "path": "schema:name",
            "op": "eq",
            "value": name
        }
        response = self.filter_query(cls.path, query_filter, context)
        if response:
            return cls.from_kg_instance(response[0], self)
        else:
            return None
