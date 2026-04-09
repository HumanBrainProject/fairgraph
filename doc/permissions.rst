==================
Access permissions
==================

Before accessing the Human Brain Project/EBRAINS Knowledge Graph through fairgraph,
you must read and accept the `Terms of Use`_, and then e-mail support@ebrains.eu
to request access.

Public and private spaces, released and unreleased nodes
========================================================

Each metadata node is stored in the KG in a "space".
Each space has its own access permissions.
Some spaces are public, others private.

The KG also has the concept of released and un-released metadata nodes.
Released nodes in public spaces can be viewed by anyone through the `KG Search UI`_, without an account.

For programmatic access, for example through **fairgraph**, an EBRAINS account is needed to access metadata.

Anyone with an EBRAINS account can access released nodes in public spaces.
Access to unreleased nodes in public spaces is restricted to curators.

To see a list of spaces you can access, run::

    >>> from fairgraph import KGClient
    >>> client = KGClient()

    >>> client.spaces(names_only=True)
    ['collab-my-project',
     'collab-another-project',
     'common',
     'computation',
     'controlled',
     'dataset',
     'files',
     'in-depth',
     'kg-search',
     'livepapers',
     'metadatamodel',
     'model',
     'myspace',
     'review',
     'software',
     'spatial',
     'tutorial',
     'webservice']

To see list of spaces for which you have write access:

    >>> client.spaces(names_only=True, permissions=["WRITE"])
    ['collab-my-project',
     'collab-another-project',
     'myspace']

For a full list of available permission names, run::

    from fairgraph.client import AVAILABLE_PERMISSIONS
    print(AVAILABLE_PERMISSIONS)


Working with private spaces
---------------------------

Everyone with an EBRAINS account can create metadata nodes in a KG private space named "myspace".
Only the user who created the node can access it.

To collaborate with others, users can create a workspace (called a "collab") in the `EBRAINS Collaboratory`_,
choose who can access that workspace, and then create a private KG space for that workspace.


Before you can use a private space, it needs to be configured,
by specifying which metadata types you plan to store in it.
This is done with the :meth:`KGClient.configure_space()` method::

    from fairgraph.openminds.core import Dataset, DatasetVersion, Software, SoftwareVersion, Person

    types = [Dataset, DatasetVersion, Software, SoftwareVersion, Person]
    space_name = "collab-my-project"
    client.configure_space(space_name, types)

Now we can save a node to this space::

    >>> person = Person(given_name="Oliver", family_name="Hardy")
    >>> person.save(client, space="collab-my-project")

To see a list of how many instances you have stored in the space::

    >>> client.space_info("collab-my-project", release_status="in progress")
    {fairgraph.openminds.core.products.dataset.Dataset: 0,
     fairgraph.openminds.core.product.dataset_version.DatasetVersion: 0,
     fairgraph.openminds.core.actors.person.Person: 1,
     fairgraph.openminds.core.product.software.Software: 0,
     fairgraph.openminds.core.product.software_version.SoftwareVersion: 0}

If you want to remove *all* nodes from a private space, you can run:

    >>> client.clean_space("collab-my-project")

.. warning:: Be *very* careful when doing this; it is really only intended for use when developing
             a new script that writes to the space, so that you can clean up mistakes
             before re-running the script.


Data Protection
===============

fairgraph is a client library that communicates with the EBRAINS Knowledge Graph
API on behalf of the user. It does not store, log, or process personal data
independently. Any metadata transmitted to or retrieved from the Knowledge Graph
— including researcher names, affiliations, and contact details embedded in
research products — is subject to the `EBRAINS Privacy Policy`_ and the `Terms of Use`_.

Authentication tokens passed to :class:`~fairgraph.KGClient` are used solely
to authenticate requests to the EBRAINS API and are never written to disk or
transmitted to any third party by fairgraph.

For questions about GDPR compliance of the EBRAINS infrastructure, contact the
EBRAINS support team via the `EBRAINS helpdesk <https://ebrains.eu/support>`_.


.. _`Terms of Use`: https://kg.ebrains.eu/search-terms-of-use.html
.. _`KG Search UI`: https://search.kg.ebrains.eu
.. _`EBRAINS Collaboratory`: https://wiki.ebrains.eus
.. _`EBRAINS Privacy Policy`: https://ebrains.eu/privacy-policy
