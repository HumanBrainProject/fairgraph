=============
Release notes
=============


Version 0.17.0
==============

Matching names when saving
--------------------------

- :meth:`~fairgraph.KGObject.exists` and :meth:`~fairgraph.KGObject.save` accept
  ``existence_match="normalized"``, with which strings in the existence query match stored values that differ
  only in case, accents and other diacritical marks, or whitespace, so that "Emilie du Chatelet" finds an existing
  "Émilie du Châtelet" rather than creating a duplicate. If several instances match, one that matches
  exactly (ignoring case) is preferred. In this mode, :class:`~fairgraph.openminds.core.Person` and
  :class:`~fairgraph.openminds.core.Organization` are first looked for by ORCID or ROR ID, respectively.
  A :class:`~fairgraph.openminds.core.Person` is then looked for by name allowing for middle names and initials,
  so "James Maxwell" and "J. Clerk Maxwell" both find an existing "James Clerk Maxwell".
  The default, ``existence_match="equals"``, is unchanged
  (`#184 <https://github.com/HumanBrainProject/fairgraph/issues/184>`_).

- :meth:`Collection.upload() <fairgraph.Collection.upload>` accepts ``existence_match``,
  which it passes on to :meth:`~fairgraph.KGObject.save` for each node.

Bug fixes
---------

- If the KG drops the connection while :meth:`~fairgraph.KGObject.exists` or :meth:`~fairgraph.KGObject.save`
  is checking whether an object already exists, they once again treat the object as not found, with a warning,
  rather than raising an exception. Since 0.16, the client raises :exc:`~fairgraph.errors.KGConnectionError`
  for lost connections, which this check did not catch.

- For the same reason, :meth:`Collection.upload() <fairgraph.Collection.upload>` once again retries saving a node
  after a lost connection or a timeout, instead of stopping at the first one.


Version 0.16.0
==============

This release requires Python 3.10 or later, as Python 3.9 has reached end of life.
fairgraph is now tested with Python 3.10 to 3.15.

Upgrading from 0.15
-------------------

Most code works unchanged, but check the following:

- :meth:`~fairgraph.KGObject.save` and :meth:`~fairgraph.KGObject.exists` now match
  the strings in an existence query *exactly*, rather than matching any stored value that *contains* the local value, 
  and ``save()`` now normalizes whitespace in text. Pipelines that re-save objects may therefore create new nodes 
  where they previously updated existing ones. See `Saving and existence queries`_.
- :meth:`Collection.load() <fairgraph.Collection.load>` now raises :exc:`NameError` by default
  for keys that are not properties of the class, matching the behaviour of openMINDS-Python. 
  See `Reading JSON-LD documents`_.
- The module-level caches in ``fairgraph.caching``, and the deprecated ``fields`` attributes and module, have been
  removed. See `Caching and release status`_ and `Removed and deprecated names`_.


Saving and existence queries
----------------------------

- The existence query that :meth:`~fairgraph.KGObject.exists` and
  :meth:`~fairgraph.KGObject.save` use to decide whether an object is already in the KG
  now matches string properties exactly, ignoring case, where it previously matched any value that
  merely *contained* the local one. Saving a :class:`~fairgraph.openminds.core.Dataset` with the short name "Foo" therefore
  no longer finds, and overwrites, an existing one called "Foo-Bar"; likewise, a
  :class:`~fairgraph.openminds.core.DatasetVersion` with the version identifier "1.0" no longer matches "1.0.1"
  (`#149 <https://github.com/HumanBrainProject/fairgraph/issues/149>`_).

  To restore the previous behaviour for a call, pass ``existence_match="contains"`` to
  :meth:`~fairgraph.KGObject.exists` or :meth:`~fairgraph.KGObject.save`
  (the default is ``existence_match="equals"``). With ``recursive=True`` the setting applies to
  child objects as well.

- :meth:`~fairgraph.KGObject.save` now removes leading and trailing whitespace from text properties,
  and in single-line properties, such as names, replaces multiple spaces or tabs within the text
  with a single space. Whitespace within multi-line properties, such as descriptions,
  is left as it is. Text loaded from the Knowledge Graph is left as it is until saved, so saving a fetched
  object corrects any stored text that is not normalized in this way.

- When an existence query matches a stored instance whose value differs from the local one (for example,
  because of using ``existence_match="contains"``) the object's attribute is now set to the
  stored value. Previously, the local value was kept and treated as a modification, so ``save()`` wrote the search
  term over the stored name (`#170 <https://github.com/HumanBrainProject/fairgraph/issues/170>`_).

- Objects whose existence query includes a property holding a list, such as ``Chapter.authors`` or
  ``LearningResource.about``, can now be found in the KG: every item in the local list must be present in the
  stored one, in any order. Previously, such objects could not be checked, so each ``save()`` created a new node.

- :meth:`~fairgraph.KGObject.exists`, and therefore :meth:`~fairgraph.KGObject.save` and
  :meth:`~fairgraph.Collection.upload`, no longer raises :exc:`TypeError` when a property used
  in the existence query holds an unresolved link (a :class:`~fairgraph.kgproxy.KGProxy`),
  as happens when a link is taken from a fetched object or read from a JSON-LD file.
  Such a link now gives the same existence query as the object it points to
  (`#145 <https://github.com/HumanBrainProject/fairgraph/issues/145>`_).


Filtering and sorting query results
-----------------------------------

- A filter on a text property can now say explicitly how its value is matched:
  with :class:`~fairgraph.queries.Equals`, the whole property value must match (the KG's "EQUALS" operator);
  with :class:`~fairgraph.queries.Contains`, the property value need only contain it ("CONTAINS");
  and with :class:`~fairgraph.queries.Regex`, added in 0.15.0, it must match a regular expression.
  A plain string means the same as :class:`~fairgraph.queries.Contains`, so existing code is unaffected.
  For example, ``Dataset.list(client, short_name=Equals("FOO"))``
  does not return a dataset called "FOO-BAR", while ``short_name="FOO"`` does.
  Matching ignores case in all three cases.

- A filter may now be given a list of values, and a result must match every value in the list, e.g.
  ``SoftwareVersion.list(client, developers__family_name=["Baggins", "Oakenshield"])``.
  The items may be plain strings, :class:`~fairgraph.queries.Contains`, :class:`~fairgraph.queries.Equals`
  or :class:`~fairgraph.queries.Regex` objects, or, for linked properties, objects or ids
  (`#150 <https://github.com/HumanBrainProject/fairgraph/issues/150>`_). See :doc:`queries`.

- Filters on several properties of the same linked node, e.g.
  ``developers__given_name="Bilbo", developers__family_name="Baggins"``, are now all applied.
  Previously, all but the last were silently ignored.

- Resolving or counting a reverse property, e.g. ``license.is_applied_to.resolve(client)``, no longer raises
  :exc:`ValueError` ("Invalid filter") when the linking property has different names in different classes
  (here ``license`` in :class:`~fairgraph.openminds.core.DatasetVersion` but ``licenses`` in :class:`~fairgraph.openminds.core.ModelVersion`),
  and now finds the nodes linking through any of the forward properties a reverse property stands for,
  where previously only the first was used
  (`#92 <https://github.com/HumanBrainProject/fairgraph/issues/92>`_).

- Queries generated by fairgraph now sort results by exactly one property, as the KG query API requires.
  Previously, classes with both ``name`` and ``lookup_label`` requested sorting by both, and the KG used
  whichever came first. The property is now given by each class's new ``sort_property`` attribute.
  As a result, :class:`~fairgraph.openminds.specimen_prep.SlicingDevice`, :class:`~fairgraph.openminds.ephys.Electrode`, 
  :class:`~fairgraph.openminds.ephys.ElectrodeArray` and :class:`~fairgraph.openminds.ephys.Pipette`
  are now sorted by ``name`` instead of ``lookup_label``, and :class:`~fairgraph.openminds.core.Person`, previously unsorted,
  is now sorted by ``family_name``. The ordering of results is now described in :doc:`queries`
  (`#129 <https://github.com/HumanBrainProject/fairgraph/issues/129>`_).


Caching and release status
--------------------------

All caching is now done by the :class:`~fairgraph.client.KGClient`, so nothing retrieved with one client,
e.g., with one user's token in a web service, is seen by another, and several cases in which the cache returned
stale or incorrect content have been fixed (`#80 <https://github.com/HumanBrainProject/fairgraph/issues/80>`_).

In particular, the cache now takes the release status into account: previously, an instance retrieved as "released" was returned
from the cache for a request for "in progress" content, and vice versa. Likewise, a document for which the user
lacks full access, retrieved by :meth:`~fairgraph.KGObject.exists` (e.g. while saving), is no longer
returned where full access is required. The cache is now also cleared for an instance when it is released,
unreleased or moved to another space.

Connection robustness
---------------------

- :class:`~fairgraph.client.KGClient` now applies a timeout to requests to the KG, so that a request
  which loses its connection (for example, when a laptop sleeps and resumes on a different network)
  fails after a while instead of hanging forever. The new ``request_timeout`` constructor argument
  overrides the default of 300s.

- Network failures now raise a new, clearer :exc:`~fairgraph.errors.KGConnectionError` rather than
  a lower-level exception.

- Read-only requests to the KG (e.g., :meth:`~fairgraph.KGObject.list`) are now retried
  automatically if they fail with a connection error. This helps with
  queries that are naturally slow (e.g., against types with very many instances, such as ``File``),
  where transient connection errors or timeouts are common but often succeed on a second attempt.
  The new ``max_retries`` (default 2) and ``retry_backoff`` (default 5s) constructor arguments to
  :class:`~fairgraph.client.KGClient` control this. Requests that modify the KG are never
  retried automatically, since doing so risks duplicating or corrupting data if the original request
  actually succeeded but its response was lost.


Files
-----

- ``File.download()`` now checks the downloaded file against the hash recorded in the Knowledge Graph
  (MD5, SHA1, or any other algorithm available in :mod:`hashlib`), and raises :exc:`ValueError` if it does
  not match. Pass ``check_hash=False`` to skip the check, e.g. for very large files.
  Files uploaded to the EBRAINS data store in several parts have an MD5 digest with a "-N" suffix,
  which is not a digest of the file: these cannot be checked, and a warning is emitted.

- ``File.from_local_file()`` now links to the content type and unit of measurement from the openMINDS
  instance library, rather than creating new, unsaved terms. 
  If the content type cannot be determined, ``format`` is left unset
  (`#177 <https://github.com/HumanBrainProject/fairgraph/issues/177>`_).


Reading JSON-LD documents
-------------------------

- :meth:`KGObject.from_jsonld() <fairgraph.KGObject.from_jsonld>` now respects
  ``ignore_unexpected_keys``, which it previously accepted but ignored. As in openMINDS Python, the default
  is to raise :exc:`NameError` if the document contains keys that are not properties of the class,
  including in linked nodes included in the document, so that mistakes in documents written by hand are caught.
  This also applies to ``load()`` and :meth:`Collection.load() <fairgraph.Collection.load>`.
  Documents from the Knowledge Graph always contain such keys (e.g., the space): fairgraph reads them with
  ``ignore_unexpected_keys=True``, and code that calls ``from_jsonld()`` on them directly must do the same.


Performance
-----------

- The openMINDS library instances (controlled terms, brain atlases, licences, content types, ...)
  are now converted to fairgraph objects the first time each class's instances are used
  (e.g. by accessing ``Species.mus_musculus``, or by calling ``Species.instances()``
  or ``Species.by_name("Mus musculus")``), rather than all of them being converted
  when fairgraph is imported. This reduces the time taken by ``import fairgraph``
  from several seconds to well under one second, and more than halves memory use
  (`#155 <https://github.com/HumanBrainProject/fairgraph/issues/155>`_).

- Property values are no longer validated when they are set on an object whose class has error handling
  set to ``None``, since any validation failures would be ignored anyway.
  Converting the openMINDS library instances to fairgraph objects
  is also about twice as fast as a result (`#155 <https://github.com/HumanBrainProject/fairgraph/issues/155>`_).
  Explicit validation, with :meth:`~openminds.base.LinkedMetadata.validate` or :attr:`is_valid`, is not affected.


Removed and deprecated names
----------------------------

- The remaining deprecated names from the renaming of "fields" to "properties" in version 0.12.0 have been removed:

  - the class attributes ``fields``, ``field_names``, ``required_field_names`` and ``existence_query_fields``;
    use ``properties`` (with ``reverse_properties``, or ``all_properties`` for both), ``property_names``,
    ``required_property_names`` and ``existence_query_properties`` instead.
  - the ``fairgraph.fields`` module. Use ``openminds.properties.Property`` in place of ``Field``.

- The deprecated aliases ``EmbeddedMetadata``, ``ContainsMetadata``, ``RepresentsSingleObject`` and ``Node``
  now emit a :exc:`DeprecationWarning`. All deprecated names will be removed in version 1.0;
  see :doc:`deprecations` (`#122 <https://github.com/HumanBrainProject/fairgraph/issues/122>`_).


Other changes
-------------

- :meth:`~fairgraph.KGClient.clean_space` now says, before asking for confirmation, how many of the
  instances are released and will therefore not be deleted, and afterwards lists the instances that were not
  deleted, with the reason, rather than printing a list of raw error objects.


Documentation
-------------

- New pages describe the deprecation policy and the deprecated names (:doc:`deprecations`), and, for developers,
  fairgraph's internal architecture (:doc:`architecture`) and how the project is maintained (:doc:`maintenance`).
- :doc:`queries` now describes how results are ordered, the three kinds of text filter, lists of filter values,
  how to work with controlled terms (under "Terminologies"), and the ways of authenticating, including when access
  tokens are renewed.
- Two tutorial notebooks, for data consumers and data providers, are in ``examples/notebooks``, and can be opened
  directly in the EBRAINS Lab (see the README there).


Version 0.15.0
==============

This release requires openMINDS 0.6.1 (``openminds>=0.6.1``).

openMINDS v5 support
--------------------

**fairgraph now supports openMINDS v5 alongside v4, on an experimental basis.**
Both sets of classes are available at the same time, and v4 remains the default, so existing
code continues to work unchanged::

    import fairgraph.openminds.core as omcore          # v4 (default)
    import fairgraph.openminds.v4.core as omcore4      # explicit v4
    import fairgraph.openminds.v5.core as omcore5      # explicit v5

v5 covers the same metadata domains as v4, plus a new **neuroimaging** domain
(:doc:`modules/openminds_v5_neuroimaging`) for MRI acquisitions and the devices used to make
them. A number of classes have been renamed — for example ``BrainAtlas`` is now
``AnatomicalAtlas``, and ``CommonCoordinateSpace`` is now ``CommonCoordinateFramework`` — and
others have been added. See :doc:`modules` for the full list.

A v4 class and its v5 counterpart share the same node type URI in the Knowledge Graph, so a
response cannot be assigned to a version by inspecting it. The client therefore has to be told
which version to deserialize into::

    from fairgraph import KGClient
    import fairgraph.openminds.v5.core as omcore

    client = KGClient(host=host_serving_v5_metadata, openminds_version="v5")
    people = omcore.Person.list(client)

``openminds_version`` accepts ``"v4"`` (the default) or ``"v5"``; anything else raises
:exc:`ValueError`. Use classes from the same version as the client you pass them to.

.. warning:: **v5 support is experimental in this release.**

             The migration of the EBRAINS Knowledge Graph to openMINDS v5 is still under way.
             The production and pre-production deployments serve v4; v5 metadata is so far only
             available from a development deployment with restricted access, whose contents are
             incomplete and liable to change. The v5 support in this release has therefore not
             yet been exercised against a fully populated KG.

             Until that changes, the v5 classes and the ``openminds_version`` argument may be
             altered in backwards-incompatible ways in any release, without the deprecation
             period that applies to the rest of the API. **openMINDS v4 support is unaffected**
             and continues to follow the normal compatibility rules.


Searching by name
-----------------

:func:`by_name()` is now at parity with the openMINDS method it overrides.
If no ``client`` argument is provided, the function calls the underlying openMINDS method,
searching within the builtin openMINDS instance library and returning objects with semantic IRIs. 
If a client is provided, the function searches the Knowledge Graph and returns objects with UUID-based ids.

Both paths now accept ``match="within"`` (the search string contains the name), ``case_sensitive``
(default ``True``, as in openMINDS) and ``ignore_accents`` (which also treats
special letters as their plain-letter equivalents, e.g., ``ß`` as ``ss``, ``œ`` as ``oe``). 

The Knowledge Graph search also now covers **all** the name-like properties a class has, 
rather than stopping at the first. It previously searched only one, which is why, for example,
``License.by_name("CC-BY-NC-4.0", client)`` found nothing: ``full_name`` was searched and
``short_name`` was not (`#131 <https://github.com/HumanBrainProject/fairgraph/issues/131>`_).


Regular-expression filters
--------------------------

Filters may now be given as a :class:`~fairgraph.queries.Regex` instead of a plain string, 
which selects the KG's "REGEX" operator in place of "CONTAINS"::

    from fairgraph import Regex

    people = Person.list(client, family_name=Regex("^M[uü]ller$"))

Note that searches are always case-insensitive.


Saving objects that already exist in another space
---------------------------------------------------

:meth:`~fairgraph.kgobject.KGObject.save` now looks for an existing matching instance in all
spaces, not just the one it is about to write to. Previously, a locally-constructed object whose
counterpart lived in a different space was not recognized, and a duplicate was created. This
happened most often with ``recursive=True``, where new child objects take on the parent's target
space (`#136 <https://github.com/HumanBrainProject/fairgraph/issues/136>`_).

If a match is found in the target space, it is used. If the only match is in another space, it
is updated in the space where it lives, with a warning, rather than being duplicated. Multiple
matches, none of them in the target space, raise an exception unless ``ignore_duplicates=True``.


Removals
--------

**The openMINDS v3 transitional machinery has been removed.**
The KG has been serving v4 metadata for some time, and the code that translated between the v3
and v4 namespaces is no longer needed. The following have been removed:

- ``KGClient.migrated``, the feature-detection probe that decided at run time whether the KG
  a client was connected to had been migrated to v4;
- the :mod:`fairgraph.utility` functions ``adapt_namespaces_3to4``, ``adapt_type_4to3``,
  ``adapt_namespaces_4to3``, ``adapt_namespaces_for_query`` and ``types_match``.

Code that called these directly will need updating; code that simply used the client is
unaffected.


Changes in behaviour
--------------------

Three changes come with the rework of :meth:`~fairgraph.kgobject.KGObject.by_name`:

- searching with a client on a class that has no name-like property at all (``DOI``, ``ORCID``, ``WebResource``, ...) 
  now raises :exc:`AttributeError`;
- an unrecognized ``match`` argument now raises :exc:`ValueError` instead of being silently treated as ``"contains"``;
- the no-client path no longer warns when several objects share a name, since openMINDS does not.
  The warning remains on the Knowledge Graph path.

Other changes:

- :meth:`~fairgraph.client.KGClient.space_info` no longer raises an error when a space contains
  types that have no fairgraph class, such as the KG's own internal types. These now appear in the
  result keyed by their type IRI (a string) rather than by a class. The ``ignore_errors``
  argument, which is no longer needed, has been removed
  (`#113 <https://github.com/HumanBrainProject/fairgraph/issues/113>`_).
- :meth:`~fairgraph.client.KGClient.query` now raises :exc:`ValueError` if a value in its
  ``filter`` argument contains "+" or "%". These values are sent to the KG as request parameters,
  which the KG does not decode correctly, so the query would otherwise silently return the wrong
  results. Filters given to :meth:`~fairgraph.kgobject.KGObject.list` and similar methods are not
  affected.


Bug fixes
---------

- Saving the same object twice in one session no longer erases the properties it does not carry. 
  (`#134 <https://github.com/HumanBrainProject/fairgraph/issues/134>`_).
- :meth:`~fairgraph.kgobject.KGObject.by_name()` no longer raises :exc:`TypeError` when called
  without a client and nothing matches; it returns ``None``.
  (`#130 <https://github.com/HumanBrainProject/fairgraph/issues/130>`_).
- :class:`~fairgraph.kgobject.KGObject` instances are now hashable, so they can be used in
  sets and as dictionary keys. Defining ``__eq__`` had made them unhashable; they now hash by
  identity, as the openMINDS classes do.
- :meth:`~fairgraph.kgobject.KGObject.from_id` now returns ``None`` for a non-existent id when
  called on the base :class:`~fairgraph.kgobject.KGObject` class (i.e., when the type is not known
  in advance), instead of raising :exc:`TypeError`
  (`#115 <https://github.com/HumanBrainProject/fairgraph/issues/115>`_).
- An instance created by :meth:`~fairgraph.kgobject.KGObject.save` is now recorded in the save
  cache. Since the KG is only eventually consistent, a newly-created instance may not yet appear in
  existence queries, so saving a second, equivalent object in the same session could previously
  create a duplicate (`#137 <https://github.com/HumanBrainProject/fairgraph/issues/137>`_).
- :meth:`~fairgraph.kgobject.KGObject.exists`, and therefore
  :meth:`~fairgraph.kgobject.KGObject.save`, no longer raises :exc:`TypeError` for new objects of
  classes whose existence query includes a date or datetime property, such as ``Book``
  (`#139 <https://github.com/HumanBrainProject/fairgraph/issues/139>`_).
- Filter values containing "+" can now be matched. fairgraph previously cut string filter values
  off at the first "+" (or raised :exc:`ValueError` if it came within the first three
  characters), to work around a KG bug. That bug only affects filter values sent as request
  parameters, which fairgraph no longer does, so values such as ``"C++"``, email addresses with a
  "+" suffix, or timestamps with a UTC offset are now searched for in full.
- Where ``exists()`` hit a connection error other than a dropped connection, it raised a
  :exc:`NameError`; the original error is now re-raised.
- Links to other KG instances can now be resolved when they are given as bare UUIDs rather than
  full URIs. Version 4 of Marmotgraph, the software behind the Knowledge Graph, gives links in this
  form; it is already used by the development deployment serving openMINDS v5 metadata.
  :class:`~fairgraph.client.KGClient` now expands them to full URIs, so that links can be resolved
  and compared with the ids of the instances they point to
  (`#144 <https://github.com/HumanBrainProject/fairgraph/pull/144>`_).


Documentation
-------------

The developer documentation in :doc:`contributing` has been expanded
(`#73 <https://github.com/HumanBrainProject/fairgraph/issues/73>`_). It now covers regenerating
the v4 and v5 classes together, the hand-written methods that are merged into generated classes,
running the tests with and without a KG token, and the versioning scheme. It also points to the
issue-tracker milestones as the project roadmap.


Version 0.14.0
==============

This release requires openMINDS 0.6.0 (``openminds>=0.6.0``) and inherits two changes in
behaviour from it.

**Links between library instances now give you objects, not dictionaries.**
The openMINDS instance libraries (available as class attributes, e.g. ``Species.mus_musculus``)
contain many cross-references: an atlas region points to its versions, a parent region to its
children, and so on. Until now those references came back as plain ``{"@id": ...}``
dictionaries, so there was nothing useful you could do with them without a separate lookup.
They are now the actual objects:

.. code-block:: python

    >>> from fairgraph.openminds.sands import ParcellationEntity
    >>> region = ParcellationEntity.aal1_acin

    # up to 0.13.6, region.has_versions[0] was a plain dict:
    {'@id': 'https://openminds.om-i.org/instances/parcellationEntityVersion/AAL1_SPM12-v4_ACIN'}

    # from 0.14.0 it is a ParcellationEntityVersion, which you can use directly:
    >>> region.has_versions[0].version_identifier
    'SPM12, v4'
    >>> region.has_versions[0].name
    'anterior cingulate and paracingulate gyri'

If your code worked around the old behaviour by reading the ``"@id"`` key out of these
dictionaries, it will need updating. References that point outside the instance libraries are
still :class:`~fairgraph.kgproxy.KGProxy` objects, resolved with
:meth:`~fairgraph.kgproxy.KGProxy.resolve` as before.

**Invalid IRIs are now reported at validation time, not on creation.**
``IRI("not a url")`` used to raise :exc:`ValueError` immediately. It now succeeds, and the
problem is reported when the containing object is validated, together with any other
validation failures, and following whatever error handling you have configured
(see :func:`fairgraph.set_error_handling`):

.. code-block:: python

    >>> repo = FileRepository(name="my repository", iri=IRI("not a url"), hosted_by=organization)
    defaultdict(<class 'list'>, {'value': ['Invalid IRI']})
    >>> repo.validate()
    {'value': ['Invalid IRI']}

Code that relied on catching :exc:`ValueError` around IRI creation should check the
validation result instead.

**Other changes in this release:**

- ``import fairgraph`` works again with openMINDS 0.6.0. Preparing the instance libraries used
  to walk the links between instances, which the newly-connected atlas instances turned into an
  endless loop (a ``RecursionError``, or exhausted memory); it no longer does
  (`#116 <https://github.com/HumanBrainProject/fairgraph/pull/116>`_).
- Fixed an out-of-date data-proxy URL that made ``download()`` fail for some datasets, models
  and atlases (:class:`~fairgraph.openminds.core.DatasetVersion`,
  :class:`~fairgraph.openminds.core.ModelVersion`,
  :class:`~fairgraph.openminds.sands.BrainAtlasVersion`,
  :class:`~fairgraph.openminds.sands.CommonCoordinateSpaceVersion`).
- :func:`fairgraph.openminds.set_error_handling` now sets error handling for every openMINDS
  submodule in a single call.


Version 0.13.6
==============

Bug fixes in this release:

- Fixed a ``KeyError`` when calling :meth:`~fairgraph.client.KGClient.query`
  with both ``instance_id`` and a custom ``id_key`` on queries using a custom
  ``responseVocab``
  (`#107 <https://github.com/HumanBrainProject/fairgraph/issues/107>`_).


Version 0.13.5
==============

Bug fixes in this release:

- Fixed a bug where :meth:`~fairgraph.kgobject.KGObject.save` could silently
  no-op after re-fetching an object via :meth:`~fairgraph.kgobject.KGObject.from_id`,
  because :attr:`KGClient.cache` was not invalidated by writes
  (`#110 <https://github.com/HumanBrainProject/fairgraph/issues/110>`_).
- Fixed the repository IRI used by the dataset version ``download()`` method
  (`#109 <https://github.com/HumanBrainProject/fairgraph/pull/109>`_).


Version 0.13.4
==============

Bug fixes in this release:

- Fixed a ``TypeError`` when trying to filter by parts of an IRI.
- Fixed ``get_journal()`` when the journal is a :class:`~fairgraph.kgproxy.KGProxy` (issue + volume case).

Other changes:

- Added GDPR documentation.


Version 0.13.3
==============

Main changes in this release:

- Improved robustness of ``Collection.upload()`` (automatic retry on failure,
  token refresh, and correct resume behaviour).
- In the query-builder module (``fairgraph.queries``), added a new
  :class:`~fairgraph.queries.PathElement` class, which allows ``reverse`` and
  ``type_filter`` to be set independently on each step of a multi-element query path.
  Previously, ``reverse`` and ``type_filter`` applied only to the first element of the path.

Here is an example of using ``PathElement`` to find all files belonging to a particular dataset
by traversing a ``fileRepository`` link forward and a ``repository`` link in reverse,
filtered to ``DatasetVersion`` nodes:

.. code-block:: python

    from fairgraph.queries import Query, QueryProperty, Filter, PathElement

    query = Query(
        node_type="https://openminds.om-i.org/types/File",
        properties=[
            QueryProperty(
                [
                    "https://openminds.om-i.org/props/fileRepository",
                    PathElement(
                        "https://openminds.om-i.org/props/repository",
                        reverse=True,
                        type_filter="https://openminds.om-i.org/types/DatasetVersion",
                    ),
                    "@id",
                ],
                name="dataset",
                expect_single=True,
                filter=Filter("CONTAINS", value="<dataset-uuid>"),
            ),
            QueryProperty("https://openminds.om-i.org/props/name", name="name"),
        ],
    )
    response = client._kg_client.queries.test_query(
        payload=self.serialize(),
        stage=Stage.RELEASED,
        pagination=Pagination(start=0, size=5)
    )

Also fixed a bug where calling ``.exists()`` on a ``ModelVersion`` with a repository that had no ``@id`` raised an error.


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