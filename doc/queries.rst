============================
Querying the Knowledge Graph
============================

Setting up a connection
=======================

Communication between **fairgraph** metadata objects and the Knowledge Graph (KG) web service is through
a client object, for which an access token associated with an EBRAINS account is needed.
To obtain an EBRAINS account, please see https://ebrains.eu/register.

The default way to connect to the KG is::

    from fairgraph import KGClient
    client = KGClient()

This will connect to the "PPD" KG environment, which should be used for testing and experimentation.
When you need to connect to the production KG, specify the host, as follows::

    client = KGClient(host="core.kg.ebrains.eu")

If you are working in an EBRAINS Lab Jupyter notebook, you are already authenticated,
and so the client will find your access token automatically.

If working outside the EBRAINS environment, the client will
print the URL of a log-in page.
You should open this URL in a web-browser, log in to your EBRAINS account,
then close the tab and return to your Python prompt or your notebook.

For more advanced users, you can alternatively obtain a token from another application
(for example from the `KG Editor`_, or by using ``clb_oauth.get_token()`` in the EBRAINS Lab)
and provide it directly::

   client = KGClient(token="<token>")

If you save the token as an environment variable named `KG_AUTH_TOKEN`,
e.g., at a shell prompt::

   export KG_AUTH_TOKEN=eyJhbGci...nPq

then the client will take the token from the environment.

Finally, if you are developing an application that is using **fairgraph** to access the KG,
you can request a service account from EBRAINS Support::

    client = KGClient(client_id="my_client_id", client_secret="<secret value>")


Listing the available metadata types
====================================

Each type of metadata node in the Knowledge Graph is represented by a Python class.
These classes are organized into modules according to the openMINDS_ schemas.
The examples below use the openMINDS v4 classes, which are the ones you get by default;
equivalent v5 classes are available in ``fairgraph.openminds.v5``.
For a full list of modules in each version, see :doc:`modules`.

To get a list of classes in a given module, import the module and then run
:func:`list_kg_classes()`, e.g.::

    >>> import fairgraph.openminds.core as omcore

    >>> omcore.list_kg_classes()
    [fairgraph.openminds.core.research.behavioral_protocol.BehavioralProtocol,
    fairgraph.openminds.core.actors.contact_information.ContactInformation,
    fairgraph.openminds.core.data.content_type.ContentType,
    fairgraph.openminds.core.miscellaneous.doi.DOI,
    fairgraph.openminds.core.products.dataset.Dataset,
    fairgraph.openminds.core.products.dataset_version.DatasetVersion,
    fairgraph.openminds.core.data.file.File,
    fairgraph.openminds.core.data.file_bundle.FileBundle,
    fairgraph.openminds.core.data.file_repository.FileRepository,
    fairgraph.openminds.core.data.file_repository_structure.FileRepositoryStructure,
    fairgraph.openminds.core.miscellaneous.funding.Funding,
    fairgraph.openminds.core.miscellaneous.gridid.GRIDID,
    fairgraph.openminds.core.miscellaneous.isbn.ISBN,
    fairgraph.openminds.core.data.license.License,
    fairgraph.openminds.core.products.meta_data_model.MetaDataModel,
    fairgraph.openminds.core.products.meta_data_model_version.MetaDataModelVersion,
    fairgraph.openminds.core.products.model.Model,
    fairgraph.openminds.core.products.model_version.ModelVersion,
    fairgraph.openminds.core.miscellaneous.orcid.ORCID,
    fairgraph.openminds.core.actors.organization.Organization,
    fairgraph.openminds.core.actors.person.Person,
    fairgraph.openminds.core.products.project.Project,
    fairgraph.openminds.core.research.protocol.Protocol,
    fairgraph.openminds.core.research.protocol_execution.ProtocolExecution,
    fairgraph.openminds.core.miscellaneous.rorid.RORID,
    fairgraph.openminds.core.miscellaneous.swhid.SWHID,
    fairgraph.openminds.core.data.service_link.ServiceLink,
    fairgraph.openminds.core.products.software.Software,
    fairgraph.openminds.core.products.software_version.SoftwareVersion,
    fairgraph.openminds.core.research.stimulation.Stimulation,
    fairgraph.openminds.core.research.subject.Subject,
    fairgraph.openminds.core.research.subject_group.SubjectGroup,
    fairgraph.openminds.core.research.subject_group_state.SubjectGroupState,
    fairgraph.openminds.core.research.subject_state.SubjectState,
    fairgraph.openminds.core.research.tissue_sample.TissueSample,
    fairgraph.openminds.core.research.tissue_sample_collection.TissueSampleCollection,
    fairgraph.openminds.core.research.tissue_sample_collection_state.TissueSampleCollectionState,
    fairgraph.openminds.core.research.tissue_sample_state.TissueSampleState,
    fairgraph.openminds.core.miscellaneous.web_resource.WebResource]


Listing all metadata nodes of a given type
==========================================

To obtain a list of all the metadata nodes of a given type, import the associated class and use
the :meth:`list()` method, passing the `client` object you created previously,
e.g., to get a list of software or open access document licences::

    from fairgraph.openminds.core import License

    licenses = License.list(client)

By default, this gives you the first 100 results.
You can change the number of results retrieved and the starting point, e.g.::

    licenses = License.list(client, from_index=15, size=10)

This returns 10 nodes starting with the 15th. To see how many nodes there are in total::

    License.count(client)

.. note:: if you consistently retrieve an empty list, it is probably because you do not
          yet have the necessary permissions. See :doc:`permissions` for more information.

Result ordering
---------------

The order in which ``list()`` returns results is only meaningful when the metadata is retrieved
through the query API (i.e. when a filter or ``follow_links`` is used, or when ``api="query"``
is passed explicitly). In that case fairgraph asks the Knowledge Graph to sort the results by a
single property, in **ascending** order and **case-insensitively** (so, e.g., ``AAL1_brain`` is
placed between ``AAL1_AMYG`` and ``AAL1_CAU``, which is not the order plain Python ``sorted()``
would produce).

The Knowledge Graph API allows sorting on exactly one property, at the root level. fairgraph
chooses that property from the class's name-like properties in a fixed priority order:
``name``, then ``full_name``, ``short_name``, ``family_name``, ``abbreviation``, then
``lookup_label``. It picks the first of these that the class actually has, so, for example,
``Dataset`` is sorted by ``full_name`` and ``Person`` by ``family_name``. ``synonyms`` is never
used as a sort key (it is list-valued), and classes with none of these properties are returned in
whatever order the Knowledge Graph supplies.

A few classes override this default because a different property keeps related results together.
In particular, ``ParcellationEntity`` and ``ParcellationEntityVersion`` are sorted by
``lookup_label`` so that terms from the same atlas stay grouped.

Results retrieved through the core API (the default for a plain, unfiltered ``list()``) are
returned in an unspecified order.

.. note:: This ordering of *results* is unrelated to the internal ``ensure_order`` option on a
          query property, which only preserves the order of instances within a list-valued
          property, not the ordering of the results returned.


Filtering/searching
===================

To obtain only metadata nodes that have certain properties, you can filter the list of nodes.
For example, to see only datasets whose name contain the phrase 'patch-clamp'::

    from fairgraph.openminds.core import Dataset, Organization

    datasets = Dataset.list(client, full_name="patch-clamp")

.. warning:: the filtering system is currently primitive, and unaware of hierarchies, e.g.
             filtering by "hippocampus" **will not** return cells with the brain region set to
             "hippocampus CA1". This is on our list of things to fix soon!
             To see a list of possible search terms, use the :meth:`property_names` attribute,
             e.g., ``DatasetVersion.property_names``
             or consult the inline help (``help(omcore.DatasetVersion)``).

A plain string matches any property value that *contains* it.
To require the whole value to match, pass an :class:`Equals` instead::

    from fairgraph import Equals

    datasets = Dataset.list(client, short_name=Equals("FOO"))

This finds datasets whose short name is "FOO", but not those named "FOO-BAR".
Case is ignored, but whitespace is not, so "FOO " would not match.
For a case-sensitive search on a property such as ``name``, see :meth:`by_name` below.
Only a single value is supported.

For a more flexible search, pass a :class:`Regex` instead of a plain string::

    from fairgraph import Regex

    datasets = Dataset.list(client, full_name=Regex("^Whole cell patch-clamp"))

The KG applies the pattern as a *search*: a pattern with no anchors matches anywhere in the property value, 
so ``Regex("patch-clamp")`` finds the same datasets as the plain string ``"patch-clamp"``. 
The ``^`` in the example above is what restricts the match to names that *begin* with the phrase; 
``$`` likewise anchors to the end.

.. note:: matching is always case-insensitive, whatever the pattern says: 
          ``Regex("^whole cell")`` and ``Regex("^Whole cell")`` return the same datasets. 
          To match case exactly, filter the results in Python.

fairgraph checks that the pattern compiles before sending it, 
so a typo raises :exc:`ValueError` rather than quietly matching nothing::

    >>> Dataset.list(client, full_name=Regex("^Whole cell (patch-clamp"))
    ValueError: Invalid regular expression '^Whole cell (patch-clamp': missing ), unterminated subpattern at position 12

.. warning:: the check uses Python's :mod:`re` module, 
             and the KG's regular expression engine is not the same as in Python,
             so if you use advanced Python-specific features it is possible for fairgraph to accept the Regex
             but for the KG to return nothing.

To search across multiple links in the graph, join property names with "__".
For example, to find all datasets whose authors are affiliated with the Karolinska Institute::

    karolinska = Organization.by_name("Karolinska", client)
    datasets = Dataset.list(client, authors__affiliations__member_of=Karolinska)


Retrieving a specific node based on its name or id
==================================================

If you know the name or unique id of a node in the KnowledgeGraph, you can retrieve it directly::

    dataset_of_interest = DatasetVersion.by_name("Whole cell patch-clamp recordings of cerebellar Golgi cells", client)
    dataset_of_interest = DatasetVersion.from_id("17196b79-04db-4ea4-bb69-d20aab6f1d62", client)

:meth:`by_name` searches the properties "name", "lookup_label", "family_name", "full_name",
"short_name", "abbreviation" and "synonyms", if the class has them. 
By default the search is for an exact, case-sensitive match, but this can be relaxed::

    licence = License.by_name("cc-by-nc-4.0", client, case_sensitive=False)
    region = ParcellationEntity.by_name("raphe nuclei", client, ignore_accents=True)
    cells = CellType.by_name("interneuron", client, match="contains", all=True)

If you provide the ``client`` argument, fairgraph searches the Knowledge Graph;
if you don't provide it, the built-in openMINDS instance library is searched instead,
and the objects found have semantic IRIs rather than UUID-based ids::

    >>> Species.by_name("Mus musculus").id
    'https://openminds.om-i.org/instances/species/musMusculus'
    >>> Species.by_name("Mus musculus", client).id
    'https://kg.ebrains.eu/api/instances/d9875ebd-260e-4337-a637-b62fed4aa91d'

Only classes that have an instance library (controlled terms, licences, content types, ...)
can be found without a client; for any other class, ``None`` is returned.


Viewing metadata and connections
================================

Once you have retrieved a node of interest, the associated metadata are available as attributes of the
Python object, e.g.::

    >>> dataset_of_interest.id
    'https://kg.ebrains.eu/api/instances/17196b79-04db-4ea4-bb69-d20aab6f1d62'

    >>> dataset_of_interest.uuid
    '17196b79-04db-4ea4-bb69-d20aab6f1d62'

    >>> dataset_of_interest.description[:100] + "..."
    'The Golgi cells, together with granule cells and mossy fibers, form a neuronal microcircuit regulati...'

Connections between graph nodes are also available as attributes::

    >>> dataset_of_interest.license
    KGProxy([License], '6ebce971-7f99-4fbc-9621-eeae47a70d85')

By default, for performance reasons, connections are not followed, and instead you will see either
a :class:`KGQuery` or :class:`KGProxy` object. In both these cases, follow the connection using the
:meth:`resolve()` method, e.g.::

    >>> license = dataset_of_interest.license.resolve(client)

    >>> license.full_name
    'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International'


It is rather cumbersome to have to follow all these connections manually.
You can ask **fairgraph** to resolve the connections for you, using the :attr:`follow_links` argument, e.g.::

    dataset_of_interest.resolve(
        client,
        follow_links={
            "license": {},
            "is_version_of": {
                "authors": {}
            }
        }
    )

Following a link is often much faster than filtering on it, and the difference can be dramatic
for types with very many instances in the Knowledge Graph. To get the files in a repository,
prefer traversing the link from the dataset version::

    dataset_version = DatasetVersion.from_id(
        dataset_version_id, client, follow_links={"repository": {"files": {}}}
    )
    files = dataset_version.repository.files

rather than filtering all files by their repository::

    files = File.list(client, file_repository=repository)   # slow

Both give the same answer, but the second builds a query over every File in the Knowledge Graph,
and there are a great many of them. For a dataset version with a few thousand files, the first
form returns in seconds where the second can take minutes.


Error handling
==============

If you don't provide all of the metadata attributes and data types expected,
**fairgraph** will warn you.

If you wish to be certain that all required attributes have been provided,
you can turn on strict checking for a given node type as follows::

    DatasetVersion.set_error_handling("error")

This will then raise an Exception if an attribute is missing or of the wrong data type.

If you wish to turn off all warnings for a given node type::

    DatasetVersion.set_error_handling(None)

You can also turn warnings on and off at the level of individual modules, or for all modules.
For example, the following turns warnings off for all modules, then sets the "core" module
to send warning messages to the Python logging system::

    import fairgraph
    fairgraph.set_error_handling(None)
    fairgraph.openminds.core.set_error_handling("log")


.. _`KG Editor`: https://editor.kg.ebrains.eu
.. _openMINDS: https://openminds.docs.om-i.org
