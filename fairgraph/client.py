"""
This module defines the KGClient class, which provides a thin interface
on top of the kg-core-python package, for communicating with the
EBRAINS KG core API.
"""

# Copyright 2018-2024 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from copy import deepcopy
import os
import logging
from typing import Any, Dict, Iterable, List, Optional, Union, TYPE_CHECKING
from uuid import uuid4, UUID

try:
    from kg_core.kg import kg
    from kg_core.request import Stage, Pagination, ExtendedResponseConfiguration, ReleaseTreeScope
    from kg_core.response import ResultPage, JsonLdDocument, SpaceInformation, Error

    have_kg_core = True
except ImportError:
    have_kg_core = False

from openminds.registry import lookup_type

from .errors import AuthenticationError, AuthorizationError, ResourceExistsError
from .utility import (
    adapt_namespaces_for_query,
    adapt_namespaces_3to4,
    adapt_namespaces_4to3,
    adapt_type_4to3,
    handle_scope_keyword,
)
from .base import OPENMINDS_VERSION

if TYPE_CHECKING:
    from .kgobject import KGObject

try:
    import clb_nb_utils.oauth as clb_oauth  # type: ignore
except ImportError:
    clb_oauth = None


logger = logging.getLogger("fairgraph")


if have_kg_core:
    STAGE_MAP = {
        "released": Stage.RELEASED,
        "latest": Stage.IN_PROGRESS,
        "in progress": Stage.IN_PROGRESS,
    }
    default_response_configuration = ExtendedResponseConfiguration(return_embedded=True)


AVAILABLE_PERMISSIONS = [
    "CREATE",
    "READ",
    "DELETE",
    "RELEASE",
    "INVITE_FOR_REVIEW",
    "INVITE_FOR_SUGGESTION",
    "SUGGEST",
    "UNRELEASE",
    "READ_RELEASED",
    "RELEASE_STATUS",
    "WRITE",
]


class KGClient(object):
    """
    A client for accessing the EBRAINS Knowledge Graph (KG) API.

    It can be used to retrieve, add, update, and delete KG nodes.

    Attributes:
        cache (dict): A dictionary used for caching JSON-LD documents.
        accepted_terms_of_use (bool): A boolean indicating whether the user has accepted the terms of use.

    Args:
        token (str, optional): An EBRAINS authentication token for accessing the KG API.
        host (str, optional): The hostname of the KG API. Use "core.kg-ppd.ebrains.eu" for testing
                              and "core.kg.ebrains.eu" to work with the production KG.
        client_id (str, optional): For use together with client_secret in place of the token if you have a service account.
        client_secret (str, optional): The client secret to use for authentication. Required if client_id is provided.
        allow_interactive (bool, default True): if true, allow authentication via web browser

    Raises:
        ImportError: If the kg_core package is not installed.
        AuthenticationError: If neither a token nor client ID/secret are provided.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        host: str = "core.kg-ppd.ebrains.eu",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        allow_interactive: bool = True,
    ):
        if not have_kg_core:
            raise ImportError("Please install the ebrains-kg-core package")
        if client_id and client_secret:
            self._kg_client_builder = kg(host).with_credentials(client_id, client_secret)
        elif token:
            self._kg_client_builder = kg(host).with_token(token)
        elif clb_oauth:
            self._kg_client_builder = kg(host).with_token(clb_oauth.get_token())  # running in EBRAINS Jupyter Lab
        else:
            try:
                self._kg_client_builder = kg(host).with_token(os.environ["KG_AUTH_TOKEN"])
            except KeyError:
                if allow_interactive:
                    iam_config_url = "https://iam.ebrains.eu/auth/realms/hbp/.well-known/openid-configuration"
                    self._kg_client_builder = kg(host).with_device_flow(
                        client_id="kg-core-python", open_id_configuration_url=iam_config_url
                    )
                else:
                    raise AuthenticationError("Need to provide either token or client id/secret.")
        self._kg_client = self._kg_client_builder.build()
        self.__kg_admin_client = None
        self.host = host
        self._user_info = None
        self.cache: Dict[str, JsonLdDocument] = {}
        self._query_cache: Dict[str, str] = {}
        self.accepted_terms_of_use = False
        self._migrated = None
        if allow_interactive:
            self.user_info()

    @property
    def _kg_admin_client(self):
        if self.__kg_admin_client is None:
            self.__kg_admin_client = self._kg_client_builder.build_admin()
        return self.__kg_admin_client

    @property
    def token(self) -> Optional[str]:
        return self._kg_client.instances._kg_config.token_handler._fetch_token()

    def _check_response(
        self,
        response: ResultPage[JsonLdDocument],
        ignore_not_found: bool = False,
        error_context: str = "",
        expected_instance_id: Optional[str] = None,
    ) -> ResultPage[JsonLdDocument]:
        if expected_instance_id and not response.error:
            if response.total > 1:
                # if an instance_id is specified, we expect there to be only one result
                # if there are more, it seems to mean that the instance_id does not exist
                response.error = Error(
                    code=404,
                    message=(
                        f"Received multiple results when specifying instance_id {expected_instance_id}"
                        "This indicates the instance does not exist."
                    ),
                )
                response.data = []
                response.size = response.total = 0
            else:
                if response.size == 1:
                    if str(expected_instance_id) not in response.data[0]["@id"]:
                        raise Exception("mismatched instance_id")
        if response.error:
            # todo: handle "ignore_not_found"
            if response.error.code == 403:
                raise AuthorizationError(f"{response} {error_context}")
            elif response.error.code == 401:
                raise AuthenticationError(f"{response} {error_context}")
            elif response.error.code == 404 and ignore_not_found:
                return response
            elif response.error.code == 409:
                raise ResourceExistsError(f"{response} {error_context}")
            else:
                raise Exception(f"Error: {response.error} {error_context}")
        else:
            if self.migrated is False:
                adapt_namespaces_3to4(response.data)
            return response

    @property
    def migrated(self):
        # This is a temporary work-around for use during the transitional period
        # from openMINDS v3 to v4 (change of namespace)
        if self._migrated is None:
            self._migrated = True  # to stop the call to _check_response() in instance_from_full_uri from recurring

            # This is the released controlled term for "left handedness", which should be accessible to everyone
            result = self.instance_from_full_uri(
                "https://kg.ebrains.eu/api/instances/92631f2e-fc6e-4122-8015-a0731c67f66c", release_status="released"
            )
            _type = result["@type"]
            if isinstance(_type, list):
                _type = _type[0]
            if "om-i.org" in _type:
                self._migrated = True
            else:
                self._migrated = False
        return self._migrated

    def query(
        self,
        query: Dict[str, Any],
        filter: Optional[Dict[str, str]] = None,
        instance_id: Optional[str] = None,
        from_index: int = 0,
        size: int = 100,
        release_status: str = "released",
        scope: Optional[str] = None,
        id_key: str = "@id",
        use_stored_query: bool = False,
        restrict_to_spaces: Optional[List[str]] = None,
    ) -> ResultPage[JsonLdDocument]:
        """
        Execute a Knowledge Graph (KG) query with the given filters and query definition.

        Args:
            query (Dict[str, Any]): A dictionary containing the query definition in JSON-LD.
            filter (Dict[str, str]): A dictionary of filters to apply to the query. Each key represents the prop name to filter on,
                and the value represents the value(s) to filter on.
            instance_id (Optional[URI]): The URI of a specific KG instance to retrieve.
            from_index (int): The index of the first result to return (0-based).
            size (int): The maximum number of results to return.
            release_status (str): The scope of the query. Valid values are "released", "in progress", or "any". Default is "released".
            id_key (str): The key that identifies the ID of a JSON-LD document. Default is "@id".
            use_stored_query (bool): Whether to use a stored query with the given query_id instead of a dynamic query. Default is False.

        Returns:
            A ResultPage object containing a list of JSON-LD instances that satisfy the query,
            along with metadata about the query results such as total number of instances, and pagination information.
        """
        release_status = handle_scope_keyword(scope, release_status)
        query_id = query.get("@id", None)

        if use_stored_query:

            def _query(release_status, from_index, size):
                response = self._kg_client.queries.execute_query_by_id(
                    query_id=self.uuid_from_uri(query_id),
                    additional_request_params=filter or {},
                    stage=STAGE_MAP[release_status],
                    pagination=Pagination(start=from_index, size=size),
                    instance_id=instance_id,
                    restrict_to_spaces=restrict_to_spaces,
                )
                error_context = f"_query(release_status={release_status} query_id={query_id} filter={filter} instance_id={instance_id} size={size} from_index={from_index})"
                return self._check_response(
                    response, error_context=error_context, expected_instance_id=instance_id, ignore_not_found=True
                )

        else:
            if self.migrated is False:
                query = adapt_namespaces_for_query(query)

            def _query(release_status, from_index, size):
                response = self._kg_client.queries.test_query(
                    query,
                    additional_request_params=filter or {},
                    stage=STAGE_MAP[release_status],
                    pagination=Pagination(start=from_index, size=size),
                    instance_id=instance_id,
                    restrict_to_spaces=restrict_to_spaces,
                )
                error_context = f"_query(release_status={release_status} query_id={query_id} filter={filter} instance_id={instance_id} size={size} from_index={from_index})"
                return self._check_response(
                    response, error_context=error_context, expected_instance_id=instance_id, ignore_not_found=True
                )

        if release_status == "any":
            # the following implementation is simple but very inefficient
            # because we retrieve _all_ instances and then apply the limits
            # from_index and size.
            # todo: make this more efficient, but be sure to clearly
            #       explain the algorithm
            instances = {}
            # first we get the released instances
            response = _query("released", 0, 100000)
            for instance in response.data:
                instances[instance[id_key]] = instance
            # now we get the "in progress" instances, and overwrite
            # any existing released instances which have the same id
            response = _query("in progress", 0, 100000)
            for instance in response.data:
                instances[instance[id_key]] = instance
            response.data = list(instances.values())[from_index : from_index + size]
            response.size = len(response.data)
            response.total = len(instances)
        else:
            response = _query(release_status, from_index, size)
        return response

    def list(
        self,
        target_type: str,
        space: Optional[str] = None,
        from_index: int = 0,
        size: int = 100,
        release_status: str = "released",
        scope: Optional[str] = None,
    ) -> ResultPage[JsonLdDocument]:
        """
        List KG instances of a given type.

        Args:
            target_type: The URI if the instance type to list.
            space: If specified, restricts the search to the given space.
            from_index: The index of the first result to include in the response.
            size: The maximum number of results to include in the response.
            release_status: The scope of instances to include in the response. Valid values are
                   'released', 'in progress', 'any'. If 'any' is specified, all accessible instances
                   are included in the response, but this may be slow where there are large numbers of instances.

        Returns:
            A ResultPage object containing the list of JSON-LD instances,
            along with metadata about the query results such as total number of instances, and pagination information.
        """
        release_status = handle_scope_keyword(scope, release_status)

        if self.migrated is False:
            target_type = adapt_type_4to3(target_type)

        def _list(release_status, from_index, size):
            response = self._kg_client.instances.list(
                stage=STAGE_MAP[release_status],
                target_type=target_type,
                space=space,
                response_configuration=default_response_configuration,
                pagination=Pagination(start=from_index, size=size),
            )
            error_context = f"_list(release_status={release_status} space={space} target_type={target_type} size={size} from_index={from_index})"
            return self._check_response(response, error_context=error_context)

        if release_status == "any":
            # see comments in query() about this implementation
            instances = {}
            # first we get the released instances
            response = _list("released", 0, 100000)
            for instance in response.data:
                instances[instance["@id"]] = instance
            # now we get the "in progress" instances, and overwrite
            # any existing released instances which have the same id
            response = _list("in progress", 0, 100000)
            for instance in response.data:
                instances[instance["@id"]] = instance
            response.data = list(instances.values())[from_index : from_index + size]
            response.size = len(response.data)
            response.total = len(instances)
            return response
        else:
            return _list(release_status, from_index, size)

    def instance_from_full_uri(
        self,
        uri: str,
        use_cache: bool = True,
        release_status: str = "released",
        scope: Optional[str] = None,
        require_full_data: bool = True,
    ) -> JsonLdDocument:
        """
        Return a specific KG instance identified by its URI.

        Args:
            uri: The global identifier of the instance
            use_cache: whether to use cached data if they exist. Defaults to True.
            release_status: The release_status of instances to include in the response.
                   Valid values are 'released', 'in progress', 'any'.
            require_full_data: Whether to only return instances for which the user has full read access.
        """
        release_status = handle_scope_keyword(scope, release_status)
        logger.debug("Retrieving instance from {}, api='core' use_cache={}".format(uri, use_cache))
        data: JsonLdDocument
        if use_cache and uri in self.cache:
            logger.debug("Retrieving instance {} from cache".format(uri))
            data = self.cache[uri]
        else:

            def _get_instance(release_status):
                error_context = f"_get_instance(release_status={release_status} uri={uri})"
                # Normal KG URIs start with https://kg.ebrains.eu/api/instances/ with a UUID
                # but for openMINDS controlled terms we may have the openMINDS URI
                # of the form https://openminds.ebrains.eu/instances/ageCategory/juvenile (v3)
                # or https://openminds.om-i.org/instances/ageCategory/juvenile (v4)
                # We use different query methods for these different cases.
                kg_namespace = self._kg_client.instances._kg_config.id_namespace
                if uri.startswith(kg_namespace):
                    response = self._kg_client.instances.get_by_id(
                        stage=STAGE_MAP[release_status],
                        instance_id=self.uuid_from_uri(uri),
                        extended_response_configuration=default_response_configuration,
                    )
                    response = self._check_response(response, error_context=error_context, ignore_not_found=True)
                    if response.error:
                        assert response.error.code == 404  # all other errors should have been trapped by the check
                        data = None
                    else:
                        data = response.data
                elif uri.startswith("https://openminds.om-i.org/instances") or uri.startswith(
                    "https://openminds.ebrains.eu/instances"
                ):
                    payload = [uri]
                    if self.migrated:
                        if uri.startswith("https://openminds.ebrains.eu"):
                            payload = [uri.replace("ebrains.eu", "om-i.org")]
                    else:
                        if uri.startswith("https://openminds.om-i.org"):
                            payload = [uri.replace("om-i.org", "ebrains.eu")]
                    response = self._kg_client.instances.get_by_identifiers(
                        stage=STAGE_MAP[release_status],
                        payload=payload,
                        extended_response_configuration=default_response_configuration,
                    )
                    # todo: handle errors
                    data = response.data[payload[0]].data
                else:
                    raise Exception(f"This client cannot retrieve instances from {uri}")

                # in some circumstances, the KG returns "minimal" metadata,
                # e.g. with just the id and fullName properties
                # this means the user does not have full access, so we count this as no data
                if require_full_data and data and "http://schema.org/identifier" not in data:
                    data = None
                return data

            if release_status == "any":
                data_ip = _get_instance("in progress")
                data_rel = _get_instance("released")
                data = data_rel or data_ip
                if data_ip is not None:
                    data.update(data_ip)
            else:
                data = _get_instance(release_status)

            if data:
                self.cache[uri] = data
        return data

    def create_new_instance(
        self, data: JsonLdDocument, space: str, instance_id: Optional[str] = None
    ) -> JsonLdDocument:
        """
        Create a new KG instance using the data provided.

        Args:
            data (dict): a JSON-LD document that should be added to the KG as a new instance.
            space (str): the space in which the instance should be stored.
            instance_id (UUID, optional): a UUID that should be used as the basis for the
                instance's persistent identifier. If not specified, the KG will generate an ID.
        """
        if "'@id': None" in str(data):
            raise ValueError("payload contains undefined ids")
        if instance_id:
            UUID(instance_id)
        if self.migrated is False:
            data = deepcopy(data)
            adapt_namespaces_4to3(data)
        if instance_id:
            response = self._kg_client.instances.create_new_with_id(
                space=space,
                payload=data,
                instance_id=instance_id,
                extended_response_configuration=default_response_configuration,
            )
        else:
            response = self._kg_client.instances.create_new(
                space=space,
                payload=data,
                extended_response_configuration=default_response_configuration,
            )
        error_context = f"create_new_instance(data={data}, space={space}, instance_id={instance_id})"
        return self._check_response(response, error_context=error_context).data

    def update_instance(self, instance_id: str, data: JsonLdDocument) -> JsonLdDocument:
        """
        Update an existing KG instance using the data provided.

        Args:
            instance_id (UUID): the instance's persistent identifier.
            data (dict): a JSON-LD document that modifies some or all of the data of the existing instance.
        """
        UUID(instance_id)
        if self.migrated is False:
            data = deepcopy(data)
            adapt_namespaces_4to3(data)
        response = self._kg_client.instances.contribute_to_partial_replacement(
            instance_id=instance_id,
            payload=data,
            extended_response_configuration=default_response_configuration,
        )
        error_context = f"update_instance(data={data}, instance_id={instance_id})"
        return self._check_response(response, error_context=error_context).data

    def replace_instance(self, instance_id: str, data: JsonLdDocument) -> JsonLdDocument:
        """
        Replace an existing KG instance using the data provided.

        Args:
            instance_id (UUID): the instance's persistent identifier.
            data (dict): a JSON-LD document that will replace the existing instance.
        """
        UUID(instance_id)
        if self.migrated is False:
            data = deepcopy(data)
            adapt_namespaces_4to3(data)
        response = self._kg_client.instances.contribute_to_full_replacement(
            instance_id=instance_id,
            payload=data,
            extended_response_configuration=default_response_configuration,
        )
        error_context = f"replace_instance(data={data}, instance_id={instance_id})"
        return self._check_response(response, error_context=error_context).data

    def delete_instance(self, instance_id: str, ignore_not_found: bool = True, ignore_errors: bool = True):
        """
        Delete a KG instance.
        """
        UUID(instance_id)
        response = self._kg_client.instances.delete(instance_id)
        # response is None if no errors
        if response:  # error
            if not ignore_errors:
                raise Exception(response.message)
        return response

    def uri_from_uuid(self, uuid: str) -> str:
        """Return an instance's URI given its UUID."""
        namespace = self._kg_client.instances._kg_config.id_namespace
        return f"{namespace}{uuid}"

    def uuid_from_uri(self, uri: str) -> UUID:
        """Return an instance's UUID given its URI."""
        namespace = self._kg_client.instances._kg_config.id_namespace
        assert uri.startswith(namespace)
        return UUID(uri[len(namespace) :])

    def store_query(self, query_label: str, query_definition: Dict[str, Any], space: str):
        """
        Store a query definition in the KG.

        Args:
            query_label (str): a label that can be used to identify and retrieve the query definition.
            query_definition (dict): a JSON-LD document defining a KG query.
            space (str): the space in which the query definition should be stored.
        """
        existing_query = self.retrieve_query(query_label)
        if existing_query:
            query_id = self.uuid_from_uri(existing_query["@id"])
        else:
            query_id = uuid4()

        try:
            response = self._check_response(
                self._kg_client.queries.save_query(
                    query_id=query_id, payload=query_definition, space=space or "myspace"
                )
            )
        except AuthorizationError:
            response = self._check_response(
                self._kg_client.queries.save_query(query_id=query_id, payload=query_definition, space="myspace")
            )

        query_definition["@id"] = self.uri_from_uuid(query_id)

    def retrieve_query(self, query_label: str) -> Dict[str, Any]:
        """
        Retrieve a stored query definition from the KG.

        Args:
            query_label (str): the label of the query definition to be retrieved.
        """
        if query_label not in self._query_cache:
            response = self._check_response(self._kg_client.queries.list_per_root_type(search=query_label))
            if response.total == 0:
                return None
            elif response.total > 1:
                # check for exact match to query_label
                found_match = False
                kgvq = "https://core.kg.ebrains.eu/vocab/query"
                for result in response.data:
                    if result[f"{kgvq}/meta"][f"{kgvq}/name"] == query_label:
                        query_definition = result
                        found_match = True
                        break
                if not found_match:
                    return None
            else:
                query_definition = response.data[0]
            self._query_cache[query_label] = query_definition
        return self._query_cache[query_label]

    def user_info(self) -> Dict[str, Any]:
        """
        Returns information about the current user.

        This information is that associated with the authorization token used.
        """
        if self._user_info is None:
            response = self._kg_client.users.my_info()
            if response.data:
                self._user_info = response.data
            elif response.error.code == 401:
                raise AuthenticationError()
            elif response.error.code == 403:
                raise AuthorizationError()
            else:
                raise Exception(response.error)
        return self._user_info

    def spaces(
        self, permissions: Optional[Iterable[str] | bool] = None, names_only: bool = False
    ) -> Union[List[str], List[SpaceInformation]]:
        f"""
        Return a list of the Knowledge Graph spaces the user can access.

        Args:
            permissions (Optional[Iterable[str]]): Return only spaces for which the user has specific permissions.
                The available permissions are as follows: {AVAILABLE_PERMISSIONS}
            names_only (bool): Whether to return detailed information about each space (default) or only the space names.

        Returns:
            Union[List[str], List[SpaceInformation]]: either a list of SpaceInformation objects (default) or a list of names.

        Raises:
            ValueError: If an invalid permission string is included in permissions.

        """
        if permissions and isinstance(permissions, Iterable):
            for permission in permissions:
                if permission.upper() not in AVAILABLE_PERMISSIONS:
                    raise ValueError(f"Invalid permission '{permission}'")
        response = self._check_response(
            self._kg_client.spaces.list(permissions=bool(permissions), pagination=Pagination(start=0, size=50))
        )
        accessible_spaces = list(response.items())  # makes additional requests if multiple pages of results
        if permissions and isinstance(permissions, Iterable):
            filtered_spaces = []
            for space in accessible_spaces:
                for permission in permissions:
                    if permission.upper() in space.permissions:
                        if names_only:
                            filtered_spaces.append(space.name)
                        else:
                            filtered_spaces.append(space)
            return filtered_spaces
        else:
            if names_only:
                return [space.name for space in accessible_spaces]
            else:
                return accessible_spaces

    @property
    def _private_space(self) -> str:
        # temporary workaround
        return f"private-{self.user_info().identifiers[0]}"

    def configure_space(self, space_name: Optional[str] = None, types: Optional[List[KGObject]] = None) -> str:
        """
        Creates and configures a Knowledge Graph (KG) space with the specified name and types.

        Args:
            space_name (str, required (optional only if you run inside a collab)): The name of the KG space to create and configure.
                If not provided, the method will try to obtain the collab ID from the environment
                variables and use it to generate a default space name in the format "collab-collab_id".
                If you are not launching this from inside an EBRAINS collab, you should provide a space name.
            types (list of Type, required): An array containing the Type classes that should be included
                in this space.

        Returns:
            str: The name of the configured KG space.

        Example usage:
            types = [Dataset, DatasetVersion, Software, SoftwareVersion]
            space_name = "collab-MyCollab"
            kg_client = KGClient()
            kg_client.configure_space(space_name, types)
        """
        if space_name is None:
            collab_id = os.environ.get("LAB_COLLAB_ID")
            if collab_id is None:
                raise ValueError(
                    "If you are not launching this from inside an EBRAINS collab, you should provide a space name with the following format: collab-collab_id."
                )
            else:
                space_name = f"collab-{collab_id}"
        result = self._kg_admin_client.create_space_definition(space=space_name)
        if result:  # error
            err_msg = f"Unable to configure KG space for space '{space_name}': {result}"
            if not space_name.startswith("collab-"):
                err_msg += (
                    f". If you are trying to configure a collab space, ensure the space name starts with 'collab-'"
                )
            raise Exception(err_msg)
        for cls in types:
            if self.migrated:
                target_type = cls.type_
            else:
                target_type = adapt_type_4to3(cls.type_)
            result = self._kg_admin_client.assign_type_to_space(space=space_name, target_type=target_type)
            if result:  # error
                raise Exception(f"Unable to assign {cls.__name__} to space {space_name}: {result}")
        return space_name

    def move_to_space(self, uri: str, destination_space: str):
        """
        Move a KG instance from one space to another.

        This is not recursive, i.e. child instances much be moved individually.
        """
        # todo: add recursion
        response = self._kg_client.instances.move(instance_id=self.uuid_from_uri(uri), space=destination_space)
        if response.error:
            raise Exception(response.error)

    def space_info(
        self,
        space_name: str,
        release_status: str = "released",
        scope: Optional[str] = None,
        ignore_errors: bool = False,
    ):
        """
        Return information about the types and number of instances in a space.

        The return format is a dictionary whose keys are classes and the values are the
        number of instances of each class in the given spaces.
        """
        release_status = handle_scope_keyword(scope, release_status)
        # todo: if not self.migrated, adapt type before lookup
        result = self._kg_client.types.list(space=space_name, stage=STAGE_MAP[release_status])
        if result.error:
            raise Exception(result.error)
        response = {}
        for item in result.data:
            if self.migrated:
                type_iri = item.identifier
            else:
                type_ = {"@type": item.identifier}
                adapt_namespaces_3to4(type_)
                type_iri = type_["@type"]
            try:
                cls = lookup_type(type_iri, OPENMINDS_VERSION)
            except (KeyError, ValueError) as err:
                ignore_list = [
                    "https://core.kg.ebrains.eu/vocab/type/Bookmark",
                    "https://core.kg.ebrains.eu/vocab/meta/type/Query",
                    "https://openminds.om-i.org/types/Query",
                    "https://openminds.ebrains.eu/core/URL",
                    "https://openminds.om-i.org/types/URL"
                ]
                if ignore_errors or any(ignore in str(err) for ignore in ignore_list):
                    pass
                else:
                    raise
            else:
                response[cls] = item.occurrences
        return response

    def clean_space(self, space_name):
        """Delete all instances from a given space."""
        # todo: check for released instances, they must be unreleased
        #       before deletion.
        space_info = self.space_info(space_name, release_status="in progress", ignore_errors=True)
        if sum(space_info.values()) > 0:
            print(f"The space '{space_name}' contains the following instances:\n")
            for cls, count in space_info.items():
                if count > 0:
                    print(cls.__name__, count)
            response = input("\nAre you sure you want to delete them? ")
            if response not in ("y", "Y", "yes", "YES"):
                return
            error_messages = []
            for cls, count in space_info.items():
                if count > 0 and hasattr(cls, "list"):  # exclude embedded metadata instances
                    print(f"Deleting {cls.__name__} instances", end=" ")
                    response = self.list(cls.type_, release_status="in progress", space=space_name, size=count)
                    assert response.total <= count
                    for instance in response.data:
                        assert instance["https://core.kg.ebrains.eu/vocab/meta/space"] == space_name
                        error = self.delete_instance(self.uuid_from_uri(instance["@id"]), ignore_not_found=False)
                        if error:
                            print("x", end="")
                            error_messages.append(error)
                        else:
                            print(".", end="")
                    print()
            if error_messages:
                print(error_messages)
        else:
            print(f"The space '{space_name}' is already clean")

    def move_all_to_space(self, source_space: str, destination_space: str):
        """
        Move all the KG instances in one space to another.
        """
        assert source_space != destination_space
        space_info = self.space_info(source_space, release_status="in progress")
        if sum(space_info.values()) > 0:
            print(f"The space '{source_space}' contains the following instances:\n")
            for cls, count in space_info.items():
                if count > 0:
                    print(cls.__name__, count)
            response = input(f"\nAre you sure you want to move them to space '{destination_space}'? ")
            if response not in ("y", "Y", "yes", "YES"):
                return
            for cls, count in space_info.items():
                if count > 0 and hasattr(cls, "list"):  # exclude embedded metadata instances
                    print(f"Moving {cls.__name__} instances", end="")
                    instances = cls.list(self, release_status="in progress", space=source_space)
                    assert len(instances) <= count
                    for instance in instances:
                        assert instance.space == source_space
                        print(".", end="")
                        self.move_to_space(instance.id, destination_space)
                    print()
        else:
            print(f"The space '{source_space}' is empty, nothing to move.")

    def is_released(self, uri: str, with_children: bool = False) -> bool:
        """
        Release status of a KG instance identified by its URI.

        Args:
            uri (URI): persistent identifier of the instance.
            with_children (bool): whether to check if all the children of the instance
                                  have also been released.

        Returns:
            True if the instance and (optionally) all its children have been released.
            Otherwise False.
        """
        if with_children:
            release_tree_scope = ReleaseTreeScope.CHILDREN_ONLY
        else:
            release_tree_scope = ReleaseTreeScope.TOP_INSTANCE_ONLY
        response = self._kg_client.instances.get_release_status(
            instance_id=self.uuid_from_uri(uri), release_tree_scope=release_tree_scope
        )
        if response.data in ("RELEASED", "HAS_CHANGED"):
            return True
        elif response.data == "UNRELEASED":
            return False
        else:
            raise AuthorizationError("You are not able to access the release status")

    def release(self, uri: str):
        """Release the instance with the given uri"""
        response = self._kg_client.instances.release(self.uuid_from_uri(uri))
        if response:
            raise Exception(f"Can't release instance with id {uri}. Error message: {response}")

    def unrelease(self, uri: str):
        """Unrelease the instance with the given uri"""
        response = self._kg_client.instances.unrelease(self.uuid_from_uri(uri))
        if response:
            raise Exception(f"Can't unrelease instance with id {uri}. Error message: {response}")
