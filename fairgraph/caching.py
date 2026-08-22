"""
This module contains global caches for Knowledge Graph data and queries,
to avoid making unnecessary API calls.
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

from collections import defaultdict
from typing import Dict, Any, Tuple


def generate_cache_key(qd: Dict[str, str]) -> Tuple:
    """From a query dict, generate an object suitable as a key for caching"""
    if not isinstance(qd, dict):
        raise TypeError("generate_cache_key expects a query dict. You provided '{}'".format(qd))
    cache_key = []
    for key in sorted(qd):
        value = qd[key]
        if isinstance(value, (list, tuple)):
            sub_key = []
            for sub_value in value:
                if isinstance(sub_value, dict):
                    sub_key.append(generate_cache_key(sub_value))
                else:
                    sub_key.append(str(value))
            cache_key.append(tuple(sub_key))
        elif isinstance(value, dict):
            cache_key.append((key, str(value)))
        elif value.__class__.__name__ == "IRI":  # a bit hacky
            cache_key.append((key, str(value)))
        else:
            if not isinstance(value, (str, int, float)):
                errmsg = "Expected a string, integer or float for key '{}', not a {}"
                raise TypeError(errmsg.format(key, type(value)))
            cache_key.append((key, value))
    return tuple(cache_key)


object_cache: Dict[str, Any] = {}  # for caching based on object ids
save_cache: Dict[type, Dict[Tuple, str]] = defaultdict(dict)  # for caching based on queries
