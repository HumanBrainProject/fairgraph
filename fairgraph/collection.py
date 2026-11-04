"""
This module provides the Collection class, an extension to the openMINDS Collection
that knows how to upload metadata to the KG.
"""

# Copyright 2018-2026 CNRS and fairgraph authors and/or their employers

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from importlib import import_module
import logging
import os
import random
from time import sleep
from uuid import uuid4
from warnings import warn

from openminds import Collection as OMCollection
from .utility import ActivityLog
from .errors import AuthenticationError

logger = logging.getLogger("fairgraph")


def _is_retryable(err):
    """Check if an error is transient and worth retrying."""
    err_str = str(err)
    return any(code in err_str for code in ("500", "502", "503", "504")) or isinstance(
        err, (ConnectionError, TimeoutError)
    )


class Collection(OMCollection):
    """
    A collection of metadata nodes that can be saved to
    and loaded from disk, and uploaded to the KG.

    Args
    ----

    *nodes (LinkedMetadata):
        Nodes to store in the collection when creating it.
        Child nodes that are referenced from the explicitly
        listed nodes will also be added. This includes instances from the
        built-in openMINDS instance library (controlled terms, licences, ...),
        which are written out in full when the collection is saved to disk,
        but are not uploaded by `upload()`, since they already exist in the KG.
    """

    def load(self, *paths):
        import_module("fairgraph.openminds")
        super().load(*paths, version="v4")

    def upload(
        self,
        client,
        default_space=None,
        space_map=None,
        verbosity=0,
        max_retries=5,
        upload_log_path=".kg_upload_log.txt",
        existence_match="equals",
    ):
        """
        Save the nodes in the collection to the Knowledge Graph.

        Nodes are saved one at a time, in an order such that linked nodes are saved before
        the nodes that link to them. Instances from the openMINDS instance library are not uploaded,
        since they already exist in the KG.

        Each node is saved with `KGObject.save()`, with `recursive=False` and `ignore_duplicates=True`,
        so a node with no id that matches an existing instance (see `KGObject.exists()`) is not created
        again. Note that the existence check searches all the spaces the user can read, and that a node
        that matches an instance in another space is updated in that space, not in the target space.

        Args:
            client: KGClient object that handles the communication with the KG.
            default_space (str, optional): The KG space to save nodes in, if not given by `space_map`.
                If not given, each node's class's default space is used.
            space_map (dict, optional): A mapping from classes to the KG spaces to save their instances in.
            verbosity (int, optional): 0 for no output (default), 1 for a progress bar (needs `tqdm`),
                2 to print each node as it is saved.
            max_retries (int, optional): How many times to retry saving a node after a transient error
                (a server error or a lost connection) or an authentication error, before giving up.
                After an authentication error, `client.refresh()` is called before retrying. Defaults to 5.
            upload_log_path (str, optional): The path of a file recording the KG id given to each node,
                so that an interrupted upload can be resumed: nodes recorded in it are not saved again.
                The file is not deleted afterwards, and is keyed on the nodes' local ids, so delete it
                before uploading a different collection, or uploading this one again from scratch.
                Defaults to ".kg_upload_log.txt", in the current directory.
            existence_match (str, optional): How string properties are compared when looking for an existing
                instance that matches a node: "equals" (the default), "contains" or "normalized".
                With "normalized", for example, a person called "Emilie du Chatelet" matches an existing
                "Émilie du Châtelet". See `KGObject.exists()`. Since nodes are saved with `ignore_duplicates=True`,
                if several instances match equally well, the first one found is used.

        Returns:
            An `ActivityLog`, recording what was done with each node.
        """
        nodes_to_save = [
            node
            for node in self.sort_nodes_for_upload()
            if not node.id.startswith("https://openminds.om-i.org/instances")
        ]
        activity_log = ActivityLog()

        # Resume support: load ID mappings from previous upload attempts
        id_mapping = {}
        if os.path.exists(upload_log_path):
            with open(upload_log_path) as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("\t")
                    if len(parts) == 2:
                        id_mapping[parts[0]] = parts[1]
                    elif len(parts) == 1:
                        # old format: local ID only, no KG ID stored
                        id_mapping[parts[0]] = None

        # Restore KG IDs for already-uploaded nodes so that
        # cross-references from later nodes resolve correctly
        skip_local_ids = set(id_mapping.keys())
        for node in nodes_to_save:
            if node.id in id_mapping:
                kg_id = id_mapping[node.id]
                if kg_id:
                    node.id = kg_id

        if verbosity == 1:
            try:
                tqdm = import_module("tqdm")
            except ImportError:
                warn("Unable to show progress bar, please install tqdm")
            else:
                nodes_to_save = tqdm.tqdm(nodes_to_save)

        for i, node in enumerate(nodes_to_save):
            if node.id in skip_local_ids or (id_mapping and node.id in id_mapping.values()):
                continue

            if verbosity == 2:
                print(f"[{100*i//len(nodes_to_save)}%] Saving {node.__class__.__name__} {node.id}")
            if space_map:
                target_space = space_map.get(node.__class__, default_space)
            else:
                target_space = default_space
            original_node_id = node.id

            for attempt in range(max_retries + 1):
                try:
                    node.save(
                        client,
                        space=target_space,
                        recursive=False,
                        ignore_duplicates=True,
                        activity_log=activity_log,
                        existence_match=existence_match,
                    )
                    with open(upload_log_path, "a") as fp:
                        fp.write(f"{original_node_id}\t{node.id}\n")
                    break
                except AuthenticationError as err:
                    if attempt < max_retries:
                        logger.warning(
                            "Authentication error, refreshing client (attempt %d/%d)", attempt + 1, max_retries
                        )
                        client.refresh()
                    else:
                        raise
                except Exception as err:
                    if _is_retryable(err) and attempt < max_retries:
                        wait = (2**attempt) * 5 + random.uniform(0, 2)
                        logger.warning(
                            "Retryable error saving %s %s (attempt %d/%d), waiting %.1fs: %s",
                            node.__class__.__name__,
                            original_node_id,
                            attempt + 1,
                            max_retries,
                            wait,
                            err,
                        )
                        sleep(wait)
                    else:
                        raise

        return activity_log
