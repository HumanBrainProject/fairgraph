"""
Python client for the Human Brain Project Neural Activity Resource

Authors: Andrew Davison et al., CNRS, 2018-2019 (see authors.rst)


Copyright 2018-2019 CNRS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
from .client import KGClient

__version__ = "0.5.2.dev"

from . import (analysis, base, brainsimulation, client, commons, core, data, electrophysiology,
               errors, minds, optophysiology, software, uniminds, utility)
