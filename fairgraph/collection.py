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
        listed nodes will also be added.
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
    ):
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
                    )
                    with open(upload_log_path, "a") as fp:
                        fp.write(f"{original_node_id}\t{node.id}\n")
                    break
                except AuthenticationError as err:
                    if attempt < max_retries:
                        logger.warning("Authentication error, refreshing client (attempt %d/%d)", attempt + 1, max_retries)
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
