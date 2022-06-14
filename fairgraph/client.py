"""
define client
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


import os
import json
import logging
from urllib.parse import urlparse, quote_plus
from time import sleep

from requests.exceptions import HTTPError
try:
    from openid_http_client.auth_client.access_token_client import AccessTokenClient
    from openid_http_client.auth_client.simple_refresh_token_client import SimpleRefreshTokenClient
    from openid_http_client.auth_client.client_credentials_client import ClientCredentialsClient
    from openid_http_client.http_client import HttpClient
    from pyxus.client import NexusClient
    from pyxus.resources.entity import Instance
    have_pyxus = True
except ImportError:
    have_pyxus = False

try:
    from jupyter_collab_storage import oauth_token_handler
except ImportError:
    oauth_token_handler = None


from .errors import AuthenticationError


CURL_LOGGER = logging.getLogger("curl")
CURL_LOGGER.setLevel(logging.WARNING)
logger = logging.getLogger("fairgraph")


SCOPE_MAP = {
    "released": "RELEASED",
    "latest": "INFERRED",
}


class KGClient(object):
    """docstring"""

    def __init__(self, token=None,
                 nexus_endpoint="https://nexus.humanbrainproject.org/v0",
                 kg_query_endpoint="https://kg.humanbrainproject.eu/query",
                 release_endpoint="https://kg.humanbrainproject.eu/api/releases",
                 idm_endpoint="https://iam.ebrains.eu/auth/realms/hbp/protocol/openid-connect",
                 oidc_host="https://iam.ebrains.eu/auth/realms/hbp",
                 client_id=None,
                 client_secret=None,
                 refresh_token=None):

        if not have_pyxus:
            raise ImportError("Support for KG version 2 requires the pyxus package.")

        if client_id and client_secret:
            if refresh_token:
                auth_client = SimpleRefreshTokenClient(oidc_host, client_secret,
                                                       client_id, refresh_token)
            else:
                auth_client = ClientCredentialsClient(oidc_host, client_secret, client_id)
        else:
            if token is None:
                if oauth_token_handler:
                    token = oauth_token_handler.get_token()
                else:
                    try:
                        token = os.environ["KG_AUTH_TOKEN"]
                    except KeyError:
                        raise AuthenticationError("No token provided.")
            auth_client = AccessTokenClient(token)

        ep = urlparse(nexus_endpoint)
        self.nexus_endpoint = nexus_endpoint
        self._nexus_client = NexusClient(scheme=ep.scheme, host=ep.netloc, prefix=ep.path[1:],
                                         alternative_namespace=nexus_endpoint,
                                         auth_client=auth_client)
        self._kg_query_client = HttpClient(kg_query_endpoint, "", auth_client=auth_client)
        self._release_client = HttpClient(release_endpoint, "", auth_client=auth_client, raw=True)
        self._idm_client = HttpClient(idm_endpoint, "", auth_client=auth_client)
        self._instance_repo = self._nexus_client.instances
        self.cache = {}  # todo: use combined uri and rev as cache keys

    def list(self, cls, from_index=0, size=100, deprecated=False, api="query", scope="released",
             resolved=False, filter=None, context=None):
        """docstring"""
        if api == "nexus":
            organization, domain, schema, version = cls.path.split("/")
            subpath = "/{}/{}/{}/{}".format(organization, domain, schema, version)
            instances = self.query_nexus(subpath, filter, context, from_index, size, deprecated)
        elif api == "query":
            if hasattr(cls, "query_id") and cls.query_id is not None:
                if resolved:
                    query_id = cls.query_id_resolved
                else:
                    query_id = cls.query_id
                instances = self.query_kgquery(cls.path, query_id, filter, from_index, size, scope)
                return [cls.from_kg_instance(instance, self, resolved=resolved)
                        for instance in instances]
            else:
                raise NotImplementedError("Coming soon. For now, please use api='nexus'")
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")
        return [cls.from_kg_instance(instance, self, resolved=resolved)
                for instance in instances]

    def count(self, cls, api="query", scope="released"):
        """docstring"""
        if api == "nexus":
            url = "{}/data/{}/?size=1&deprecated=False".format(self.nexus_endpoint, cls.path)
            response = self._nexus_client._http_client.get(url)
        elif api == "query":
            if scope not in SCOPE_MAP:
                raise ValueError("'scope' must be either '{}'".format("' or '".join(list(SCOPE_MAP))))
            url = "{}/{}/instances?size=1&databaseScope={}".format(cls.path, cls.query_id, SCOPE_MAP[scope])
            response = self._kg_query_client.get(url)
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")
        return response["total"]

    def _raw_query_nexus(self, path, filter, context, from_index=0, size=100, deprecated=False):
        if filter:
            filter = quote_plus(json.dumps(filter))
        if context:
            context = quote_plus(json.dumps(context))
        tries = 0
        while tries < 5:
            try:
                query = self._nexus_client.instances.list(
                    subpath=path,
                    filter_query=filter,
                    context=context,
                    from_index=from_index,
                    size=size,
                    deprecated=deprecated,
                    resolved=True)
            except HTTPError as err:
                if err.response.status_code == 503:
                    tries += 1
                    if tries >= 5:
                        raise
                    logger.warning("503 error. Retrying ({} of 5)".format(tries))
                    sleep(5)
                else:
                    raise
            else:
                tries = 9999  # continue
        return query

    def query_nexus(self, path, filter, context, from_index=0, size=100, deprecated=False):
        # Nexus API
        logger.debug("Making Nexus query {} with filter {}".format(path, filter))
        instances = []
        query = self._raw_query_nexus(
            path=path,
            filter=filter,
            context=context,
            from_index=from_index,
            size=size,
            deprecated=deprecated)
        # todo: add support for "sort" field
        instances.extend(query.results)
        next = query.get_next_link()
        while len(instances) < size and next:
            query = self._nexus_client.instances.list_by_full_path(next)
            instances.extend(query.results)
            next = query.get_next_link()

        for instance in instances:
            self.cache[instance.data["@id"]] = instance
            instance.data["fg:api"] = "nexus"
        return instances

    def count_nexus(self, path, filter, context, deprecated=False):
        # Nexus API
        logger.debug("Making Nexus count query {} with filter {}".format(path, filter))
        query = self._raw_query_nexus(
            path=path,
            filter=filter,
            context=context,
            from_index=0,
            size=1,
            deprecated=deprecated)
        return query.total

    def query_kgquery(self, path, query_id, filter, from_index=0, size=100, scope="released"):
        template = "{}/{}/instances?start={{}}&size={}&databaseScope={}".format(
            path, query_id, size, SCOPE_MAP[scope])
        if filter:
            for key, value in filter.items():
                if hasattr(value, "iri"):
                    filter[key] = value.iri
            template += "&" + "&".join("{}={}".format(k, quote_plus(v.encode("utf-8"))) for k, v in filter.items())
        if scope not in SCOPE_MAP:
            raise ValueError("'scope' must be either '{}'".format("' or '".join(list(SCOPE_MAP))))
        start = from_index
        #url = quote_plus(template.format(start).encode("utf-8"))
        url = template.format(start)
        try:
            response = self._kg_query_client.get(url)
        except HTTPError as err:
            if err.response.status_code == 403:
                response = None
            else:
                raise
        if response and "results" in response:
            instances = [
                Instance(path, data, Instance.path)
                for data in response["results"]
            ]
            start += response["size"]
            while start < min(response["total"], size):
                #url = quote_plus(template.format(start).encode("utf-8"))
                url = template.format(start)
                response = self._kg_query_client.get(url)
                instances.extend([
                    Instance(path, data, Instance.path)
                    for data in response["results"]
                ])
                start += response["size"]
        else:
            instances = []

        for instance in instances:
            self.cache[instance.data["@id"]] = instance
            instance.data["fg:api"] = "query"
        return instances

    def instance_from_full_uri(self, uri, cls=None, use_cache=True, deprecated=False, api="query",
                               scope="released", resolved=False):
        # 'deprecated=True' means 'returns an instance even if that instance is deprecated'
        # should perhaps be called 'show_deprecated' or 'include_deprecated'
        logger.debug("Retrieving instance from {}, api='{}' use_cache={}".format(uri, api, use_cache))
        if scope == "released" and not self.is_released(uri):
            return None

        if use_cache and uri in self.cache:
            logger.debug("Retrieving instance {} from cache".format(uri))
            instance = self.cache[uri]
        elif api == "nexus":
            instance = Instance(Instance.extract_id_from_url(uri, self._instance_repo.path),
                                data=self._instance_repo._http_client.get(uri),
                                root_path=Instance.path)
            if instance and instance.data and "@id" in instance.data:
                if deprecated is False and instance.data["nxv:deprecated"]:
                    instance = None
                    logger.debug("Not returning deprecated instance")
                else:
                    self.cache[instance.data["@id"]] = instance
                    logger.debug("Retrieved instance from KG Nexus" + str(instance.data))
            else:
                instance = None
        elif api == "query":
            if cls and hasattr(cls, "query_id") and cls.query_id is not None:
                if resolved:
                    query_id = cls.query_id_resolved
                else:
                    query_id = cls.query_id
                response = self._kg_query_client.get(
                    "{}/{}/instances?databaseScope={}&id={}".format(cls.path,
                                                                    query_id,
                                                                    SCOPE_MAP[scope],
                                                                    uri))
                if response and len(response["results"]) > 0:
                    instance = Instance(cls.path, response["results"][0], Instance.path)
                    self.cache[instance.data["@id"]] = instance
                    logger.debug("Retrieved instance from KG Query" + str(instance.data))
                else:
                    logger.warning("Instance not found at {} using KG Query API".format(uri))
                    instance = None
            else:
                raise NotImplementedError("No query id available: cls={}".format(str(cls)))
        else:
            raise ValueError("'api' must be either 'nexus' or 'query'")
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
        instance.data.pop("fg:api", None)
        instance = self._nexus_client.instances.update(instance)
        return instance

    def delete_instance(self, instance):
        self._nexus_client.instances.delete(instance)
        logger.debug("Deleting instance {}".format(instance.id))
        if instance.data["@id"] in self.cache:
            logger.debug("Removing {} from cache".format(instance.data["@id"]))
            self.cache.pop(instance.data["@id"])

    def by_name(self, cls, name, match="equals", all=False,
                api="query", scope="released", resolved=False):
        """Retrieve an object based on the value of schema:name"""
        # todo: allow non-exact searches
        if api not in ("query", "nexus"):
            raise ValueError("'api' must be either 'nexus' or 'query'")
        valid_match_methods = {
            #"query": ("starts_with", "ends_with", "contains", "equals", "regex"),
            "query": ("contains", "equals"),
            "nexus": ("equals")
        }
        if match not in valid_match_methods[api]:
            raise ValueError("'match' must be one of {}".format(valid_match_methods[api]))

        if api == "nexus":
            op = {"equals": "eq", "contains": "in"}[match]
            context = {"schema": "http://schema.org/"}
            query_filter = {
                "path": "schema:name",
                "op": op,
                "value": name
            }
            instances = self.query_nexus(cls.path, query_filter, context)
        else:
            assert api == "query"
            if hasattr(cls, "query_id") and cls.query_id is not None:
                if resolved:
                    query_id = cls.query_id_resolved
                else:
                    query_id = cls.query_id
                response = self._kg_query_client.get(
                    "{}/{}{}/instances?databaseScope={}&name={}".format(
                        cls.path,
                        query_id,
                        match == "contains" and "_name_contains" or "",  # workaround
                        SCOPE_MAP[scope],
                        name))
                instances = [Instance(cls.path, result, Instance.path)
                             for result in response["results"]]
            else:
                raise NotImplementedError("Coming soon. For now, please use api='nexus'")
        if instances:
            if all:
                return [cls.from_kg_instance(inst, self, resolved=resolved)
                        for inst in instances]
            else:  # return only the first result
                return cls.from_kg_instance(instances[0], self, resolved=resolved)
        else:
            return None

    def store_query(self, path, query_definition):
        self._kg_query_client.raw = True  # endpoint returns plain text, not JSON
        response = self._kg_query_client.put(path, data=query_definition)
        self._kg_query_client.raw = False

    def retrieve_query(self, path):
        return self._kg_query_client.get(path)

    def is_released(self, uri):
        """Release status of the node"""
        path = Instance.extract_id_from_url(uri, self._instance_repo.path)
        response = self._release_client.get(path)
        return response.json()["status"] == "RELEASED"

    def release(self, uri):
        """Release the node with the given uri"""
        path = Instance.extract_id_from_url(uri, self._instance_repo.path)
        response = self._release_client.put(path)
        if response.status_code not in (200, 201):
            raise Exception("Can't release node with id {}".format(uri))

    def unrelease(self, uri):
        """Unrelease the node with the given uri"""
        path = Instance.extract_id_from_url(uri, self._instance_repo.path)
        response = self._release_client.delete(path)
        if response.status_code not in (200, 204):
            raise Exception("Can't unrelease node with id {}".format(uri))

    def user_info(self):
        return self._idm_client.get("userinfo")
