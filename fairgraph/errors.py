"""
Definition of specific Exceptions.
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


class ResourceExistsError(Exception):
    """Raised when trying to create a resource that already exists in the Knowledge Graph"""

    pass


class AuthenticationError(Exception):
    """Raised when there is a problem with authentication"""

    pass


class AuthorizationError(Exception):
    """Raised when there is a problem with authorization"""

    pass


class ResolutionFailure(Exception):
    """Raised when unable to resolve a link in the Knowledge Graph"""

    pass


class CannotBuildExistenceQuery(Exception):
    """Raised when it is not possible to build an existence query"""

    pass
