=============
Release notes
=============


Version 0.13.2
==============

Fixed some bugs in the machinery for supporting the openMINDS v3 to v4 migration.
This version has been tested with both unmigrated (v3) and migrated (v4) deployments of the KG.


Version 0.13.1
==============

Fixed a bug where checking if an object exists was resetting any properties that had been changed to None locally.


Version 0.13.0
==============

For this version we have extensively rewritten fairgraph,
to build directly on the `openMINDS Python library`_.
This

- ensures (almost) perfect compatibility between the openMINDS API and the fairgraph API,
  so people can start developing locally with openMINDS-Python, then just change to
  importing "fairgraph.openminds" instead of "openminds.v4" when they wish to upload
  metadata to the Knowledge Graph.
- adds functionality for working with local JSON-LD files in fairgraph.
- provides the openMINDS instances libraries as class attributes, e.g., ``Species.mus_musculus``
- adds the :class:`Collection`, which has the functionality of the equivalent class in openMINDS-Python,
  but in addition has support for uploading an entire metadata collection to the KG in a single call.

The documentation has been refreshed and extended.

This version of fairgraph provides the openMINDS v4 schemas.

There is one breaking change, the keyword argument "scope" has been renamed to "release_status".


Version 0.12.2
==============

This version includes various small changes and bug fixes.

- Improvements to :meth:`client.user_info()` implementation, to give better error messages in case of failure.
- Use numbers.Real in place of float in fields where openMINDS specifies type "number".
- More informative error message for unserializable values.
- Optimization of the :meth:`exists()` method, to improve performance by using a simpler query.
- Allow restricting :meth:`exists()` to specific spaces.
- Don't allow creating IRI objects with an empty string.

Version 0.12.1
==============

This version includes various small changes and bug fixes.

- Reverse properties/fields, introduced in version 0.11, are now contained in the attribute :attr:`reverse_properties`,
  which makes it easier to operate only on intrinsic, "forward" properties or only on reverse properties.
- The :attr:`type_` attribute is now a string (as in openMINDS Python), rather than a single-element list containing that string (as in the KG).
- The :class:`KGClient` now allows interactive authentication via a web-browser ("device flow"),
  if the client cannot find an authorization token.
  To disable this (for example for non-interactive use), create the client with ``allow_interactive=False``.
- Added methods :meth:`space_info()` and :meth:`clean_space()` to :class:`KGClient`, to make it easier to clean up private and collab KG spaces used for testing and development.
- Added method :meth:`move_all_to_space()` method to :class:`KGClient`, primarily intended for use by KG curators.
- Added the option to ignore duplicates in :meth:`node.exists()` calls (by default, if multiple nodes match the existence query an Exception will be raised)
- Updated the :mod:`openminds` module to include the latest changes in the openMINDS schemas.
- Partially fixed a `bug <https://github.com/HumanBrainProject/fairgraph/issues/92>`_ in which resolving certain reverse links is broken.

Version 0.12.0
==============

The main change in this release is the harmonization of terminology between fairgraph and the openMINDS Python library.
In particular, Field/fields has been changed to Property/properties, but there are also various other changes.
The previous names should still work, and should emit a deprecation warning.
The previous names will be removed in a future release.

In addition, the openminds module builder has been rewritten using the new openMINDS build pipeline.
This should not have resulted in any substantive changes to the released fairgraph package.

Version 0.11.0
==============

"Reverse" fields
----------------

fairgraph now includes "reverse" fields,
i.e. fields that connect to objects that aren't defined directly in the schema for a given type A,
but are defined in other types, B, C that link to objects of type A.
To take an example, :class:`Model` has a field :attr:`versions`,
which links to objects of type :class:`ModelVersion`.
Now we've added to :class:`ModelVersion` a "reverse" field :attr:`is_version_of`,
which links back to the :class:`Model`.

These reverse links can be resolved, and can be used for queries.
For example, if you are starting from a :class:`ModelVersion`,
and wish to find its associated :class:`Model`, previously you had to perform a query:

.. code-block:: python

    >>> models = omcore.Model.list(client, versions=model_version)
    >>> model = models[0]

Now, you can just resolve the reverse field:

.. code-block:: python

    >>> model = model_version.is_version_of.resolve(client)

The original method also still works, and could be more efficient,
depending on how many objects of each type there are.
If performance is an issue, it is best to profile both approaches.

Perhaps more usefully, you can now ask fairgraph to resolve the :class:`Model` at the moment
of obtaining the :class:`ModelVersion`, e.g.

.. code-block:: python

    >>> model_version = omcore.ModelVersion.from_id(
    ...     "5c52380c-7bd9-4fe6-8d72-ff340250b238",
    ...     client,
    ...     follow_links={"is_version_of": {}}
    ... )
    >>> type(model_version.is_version_of)
    <class 'fairgraph.openminds.core.products.model.Model'>
    >>> model_version.is_version_of.uuid
    'be001074-7eab-4c7e-9bde-9e5987b085d2'

and you can also make queries across these reverse links, e.g.

.. code-block:: python

    >>> model_versions = omcore.ModelVersion.list(
    ...     client,
    ...     is_version_of="be001074-7eab-4c7e-9bde-9e5987b085d2"  # id of a Model
    ... )
    >>> model_versions[0].uuid
    '5c52380c-7bd9-4fe6-8d72-ff340250b238'


.. note:: reverse links that pass via :class:`EmbeddedMetadata` instances are not yet supported.
          For example: :class:`SoftwareVersion` has a field :attr:`copyright`, which contains
          embedded metadata of type :class:`Copyright` (which does not have its own ID).
          :class:`Copyright` has a field :attr:`holders` which links to :class:`Person`, among others.
          At present, it is not possible to access the :class:`SoftwareVersion` from a :class:`Person`
          by way of a reverse field, since the link is not direct. (You can still make a forward query, though).
          Such indirect reverse fields will be implemented in a future version of fairgraph.


Other changes
-------------

- made the ``follow_links`` argument to :meth:`resolve()` behave the same way as for :meth:`list()`, :meth:`from_id()`, etc.,
  i.e. it expects a structure of nested dicts to specify explicitly which links to follow,
  rather than an integer meaning "follow all links for this number of levels".
- added :func:`set_error_handling()` as a module-level function, so you can control the behaviour of all classes in a module (e.g. ``fairgraph.openminds.core``) in a single line.


Version 0.10.0
==============

New/modified functionality
--------------------------

- more flexible "strict_mode" - replace [True, False] with Enum["error", "warning", "log" none"], rename to "error_handling", and  make ErrorHandling.log the default
- support filters that cross links in the graph
- implement more fine-grained control of specifying links to follow when creating queries
- add "follow_links" argument to `from_uri()`, `from_uuid`, `from_id`, `from_alias` and `by_name`
- remove "resolved" keyword argument and replace with "follow_links"
- improve "queries" module to expose more of the available features of the API
- allow `KGObject.from_id()` to work with cls=KGObject, i.e. when we have an @id but don't know its type
- add an `__init__()` method with explicit field names to all KGObject sub-classes, to catch incorrect keyword arguments
- rename "type" class attribute to "type\_" to avoid clashing with "type" as an openMINDS property name
- regenerate fairgraph.openminds based on latest openMINDS v3-dev
- remove mention of "v3" from module and variable names
- remove code relating to KG v2

Code/documentation quality
--------------------------

- update documentation - added developers' guide and code-of-conduct
- add codemeta.json
- code cleanup and refactoring
- add docstrings to most classes and methods that were missing them
- formatted codebase with black
- started adding type annotations
- deserialization of EmbeddedMetadata uses the same machinery as KGObject
- simplify internal data handling (in particular detecting updated fields).
- remove unused code
- switch to using expanded keys (URIs) in KGObject.data, to reduce the risk of confusion, since the KG always returns data with expanded keys.
- make `expand_uri` consistent with `compact_uri` in how it handles single uris vs lists of uris
- remove dependency on pyld
- by default, don't use stored queries, use the latest generated ones
- more unit tests

Version 0.9.0
=============

- implement the "match" argument of the `by_name()` method
- change `configure_space()` to take the space name, not the collab id, as its argument
- fix DatasetVersion.download() for unreleased data repositories
- better handling of the scenario when self.exists() gives the wrong answer, so we get an error on creating a new instance
- distinguish authorization and authentication errors, and allow being more forgiving with authorization errors
- fix some bugs when using fairgraph without curator privileges
- add "allow_update" attribute to KGObject (True by default), to support preventing attempted updates when needed
- more informative error messages
- better handling of the situation where fields with `multiple=False` receive multiple items
- when calculating which fields need to be updated, handle expanded and compacted paths
- better documentation of controlled terms, including adding a list of possible values and ontology links to docstrings
- switch to building project with pyproject.toml
- update openMINDS schemas

Version 0.8.2
=============

- more informative error message when failing to generate cache key
- add KGClient method to move instances between spaces
- allow `client.query(..., scope="any",...)` to work with custom queries (ones not generated by fairgraph)
- add `scope="any"`
- update openMINDS schemas, including adding "chemicals" extension
- add "instance_id" option to kgclient query() method

Version 0.8.1
=============

- recursive save now handles EmbeddedMetadata objects that _contain_ KGObjects (e.g. QuantitativeValue→UnitOfMeasurement, Affiliation→Organization)
- `space` no longer defaults to the class default
- make it clear that `data` and `space` are required for `create_new_instance()`
- fix release()/unrelease() methods, and add support for recursive releasing (i.e. following tree of children)

Version 0.8.0
=============

- update to work with new ebrains-kg-core package release (from PyPI)
- add `configure_space(collab_id, types)` method to KGClient
- updates following recent openMINDS schema changes
- avoid confusing error messages when importing fairgraph if kg-core-python not installed

Version 0.7.1
=============

- run tests with Github Actions
- fix a few bugs

Version 0.7.0
=============

- add `download()` methods
- support use of KGProxy objects as filter values
- updates to reflect recent changes in openMINDS
- more flexibility in delete() method
- store the scope from which an object was queried
- add `from_alias()`
- if unable to store queries to the preferred space, use "myspace"
- prevent writing to "controlled" space
- assorted bug fixes
- cleaner separation between KGObject and KGClient functionality
- handle lists of filter values
- add a "follow_links" argument to the `resolve()` methods, to avoid having to manually resolve links.
- order fields in openMINDS classes alphabetically, except for certain priority fields that act as unique names
- refactor queries to allow dynamically generated queries based on filter settings, not only previously-stored queries
- move fairgraph openMINDS generator from openMINDS_generator to fairgraph repository
- change default strict mode to False
- make v3 the default
- add support for typeFilter in queries, and use this to re-enable support for cases where different allowed classes have different fields, such as QuantitativeValue and QuantitativeValueRange for age, weight
- make pyxus and openid_http_client optional dependencies, so people using only KGv3 can install fairgraph without them
- add documentation of openMINDS classes

Version 0.6.0
=============

- support for openMINDS and KG v3
- improved handling of spaces when saving
- handle serialization of KGProxy objects
- added "replace" option to KGObject.save(), and implemented client.delete_instance() and client.replace_instance()
- add CI testing with Python 3.9
- handle expiring tokens better, since kg_core_python doesn't consider 401 and 403 responses as errors
- add queryable logging of activity when saving, to help debug problems with KG updating
- when saving recursively, non-top-level objects that already exist in a space are updated in that space, and existing controlled terms are not updated.
- raise a NameError if unrecognized keyword arguments are based to a KGObject constructor, helps avoid misspellings passing unnoticed.
- add caching of queries, to avoid repeated network requests
- fix inconsistency in signatures of "resolve()" methods
- explictly use "latest" scope when getting data while saving
- support new KG authentication method
- many new v2 schemas, including live papers, computational provenance, optophysiology
- update openminds module with latest schemas
- add utility methods Person.me() and File.from_local_file()
- add "from_index" argument to KGQuery.resolve()
- add "count()" method to KGQuery
- add the option to load SPDX licence data from a local file rather than downloading from Github
- remove Python 2 code
- drop testing for Python 2.7 and 3.5, add testing for 3.8.
- can now filter on datetime fields.
- fix for when query values contain non-ascii characters
- when updating an object, also update the cached version
- more robust download method for Dataset


.. _`openMINDS Python library`: https://pypi.org/project/openMINDS