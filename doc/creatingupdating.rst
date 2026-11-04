====================================
Creating and updating metadata nodes
====================================

To create a new metadata node, create an instance of the appropriate Python class,
then use the :meth:`save()` method, e.g.::

    from fairgraph.openminds.core import SoftwareVersion

    sv = SoftwareVersion(
        name="numpy",
        alias="numpy",
        version_identifier="1.14.9"
    )
    sv.save(client, space="myspace")

To update a node, edit the attributes of the corresponding Python object, then :meth:`save()` again::

    from fairgraph import IRI

    sv.homepage = IRI("https://numpy.org")
    sv.save(client)

(Note that for updating existing objects you don't need to specify the space.)

.. note:: Before saving, **fairgraph** removes leading and trailing whitespace
          from properties that contain text (including those of embedded nodes).
          In single-line properties, such as names, each run of whitespace within the text,
          including line breaks, is also replaced by a single space.

How does fairgraph distinguish between creating a new node and modifying an existing one?
=========================================================================================

If a previously-created node has been retrieved from the Knowledge Graph, it will have a unique ID,
and therefore calling :meth:`save()` will update the node with this ID.

If a new Python object is created with the same or similar metadata, **fairgraph** queries for
a node with matching metadata for a *subset* of the properties.
If you want to know which properties are included in the match, examine the :attr:`existence_query_properties`
attribute, e.g.::

    >>> SoftwareVersion.existence_query_properties
    ('short_name', 'version_identifier')

String properties must match exactly (ignoring case).
If you want a value in the Knowledge Graph to match when it merely *contains* the local value,
pass ``existence_match="contains"`` to :meth:`save()` or :meth:`exists()`. 
Use this with care: the object you save will overwrite any that is found::

    >>> dataset.save(client, space="myspace", existence_match="contains")

Names are often written in different ways, for example with or without accents. To find a match
that differs from the local value only in case, accents and other diacritical marks,
or whitespace, pass ``existence_match="normalized"``::

    >>> person = Person(given_name="Emilie", family_name="du Chatelet")
    >>> person.save(client, space="common", existence_match="normalized")  # finds "Émilie du Châtelet"

If several nodes match, but only one of them matches exactly (ignoring case), that one is used;
otherwise an exception is raised, unless you pass ``ignore_duplicates=True``.
When a match is found, the object takes the spelling stored in the Knowledge Graph,
so saving does not overwrite it.

With ``existence_match="normalized"``, :class:`Person` and :class:`Organization` objects that have
an ORCID or a ROR ID, respectively, in :attr:`digital_identifiers` are first looked for by that identifier,
and by name only if no node has it. A node found by its identifier is updated with the local names
if they differ.

When looking for a :class:`Person` by name with ``existence_match="normalized"``, the given names may
also differ by middle names that appear in only one of them, and by initials in place of names,
so "James Maxwell", "James C. Maxwell" and "J. Clerk Maxwell" all find an existing "James Clerk Maxwell".
The first given names must correspond, however: "Clerk Maxwell" does not. Family names must still match
as described above. If several nodes match, one whose given names match exactly (ignoring case) is preferred,
then one whose given names differ only in case, accents or whitespace. As before, the object takes the
names stored in the Knowledge Graph, so saving "James Maxwell" does not remove the middle name of an existing
"James Clerk Maxwell".


Saving child nodes
==================

By default, **fairgraph** will recursively save all child objects of the object that is being directly saved.
For example, if saving a :class:`Dataset` it will also save all the :class:`Person` objects in the :attr:`authors` property.

To turn off this recursive behaviour (for example, because you know the child objects have not been modified,
or because you want more fine-grained control over what gets saved), run::

    >>> obj.save(client, space="myspace", recursive=False)


Permissions
===========

If you get an error message when trying to create or update a node, it may be because you do not
have the necessary permissions. See :doc:`permissions` for more information.
