=========================
Contributing to fairgraph
=========================


Contributions
=============

Contributions are welcome, and credit will always be given.

Report bugs
-----------

Report bugs through `GitHub <https://github.com/HumanBrainProject/fairgraph/issues>`__.

Please report relevant information and preferably code that demonstrates the problem.

Fix bugs or add new features
----------------------------

Look through the GitHub issues for bugs. Anything is open to whoever wants to implement it.
Changes should be proposed through pull requests.

Planned work is organised with `milestones`_ on the issue tracker: each milestone collects the
issues intended for a given release, so the milestone list serves as the project roadmap.
Issues labelled ``task`` are maintenance and code-quality work rather than user-facing changes.

Improve documentation
---------------------

fairgraph could always use better documentation, whether as part of the official docs,
in docstrings, or elsewhere (articles, tutorials, videos).

Submit feedback
---------------

The best way to send feedback is to `open an issue on GitHub <https://github.com/HumanBrainProject/fairgraph/issues/new>`__.

Code of conduct
---------------

We wish to foster an open and welcoming environment within the project.
As such we request that contributors abide by our code of conduct (see :file:`CODE_OF_CONDUCT.md` `(Link) <https://github.com/HumanBrainProject/fairgraph/blob/master/CODE_OF_CONDUCT.md>`_).


Developers' Guide
=================

Setting up a development environment
------------------------------------

We recommend developing in a Python virtual environment.

For example::

    $ python3 -m venv /path/to/venv
    $ source /path/to/venv/bin/activate


Getting the source code
-----------------------

We use the Git version control system. The best way to contribute is through
GitHub. You will first need a GitHub account, and you should then fork the
fairgraph `GitHub Repository`_
(see http://help.github.com/en/articles/fork-a-repo).

To get a local copy of the repository::

    $ cd /some/directory
    $ git clone git@github.com:<username>/fairgraph.git

Now you need to make sure that the ``fairgraph`` package is on your PYTHONPATH.
You can do this by installing with the *editable* option,
which avoids reinstalling when there are changes in the code::

    $ cd fairgraph
    $ pip install -e .

To install all dependencies needed for development::

    $ pip install -e .[dev]

or if using the zsh shell::

    $ pip install -e ".[dev]"

We strongly recommend always working in a branch other than "master", and keeping your
local master branch synchronized with the main, "upstream" repository::

    $ git remote add upstream git@github.com:HumanBrainProject/fairgraph.git
    $ git pull upstream master

    $ git checkout -b informative-branch-name

If the branch is for fixing a bug, we suggest including the word "bug" in the branch name,
or name it after a Github issue, e.g. "issue-42".
If the branch is for adding a new feature, make the branch name a short but informative
description of the feature, e.g. "improve-tests".

Building the openMINDS module
-----------------------------

The :mod:`fairgraph.openminds` module is built from the openMINDS schemas.
To obtain the latest schemas, clone the main openMINDS repository to somewhere
outside the fairgraph directory tree::

    $ git clone https://github.com/openMetadataInitiative/openMINDS.git /path/to/openMINDS

fairgraph provides classes for two schema versions, so both are generated together.
Within the main fairgraph folder::

    $ cd builder
    $ python update_openminds.py /path/to/openMINDS/schemas/v4.0 \
          --generate-all --v5-root /path/to/openMINDS/schemas/v5.0

This will delete and re-create the :file:`fairgraph/openminds/v4` and
:file:`fairgraph/openminds/v5` directories. A single version can be regenerated on its own with
``--version v4`` (or ``v5``) and no ``--generate-all``, but note that the two versions must stay
consistent with each other, so regenerating both is usually what you want.
The hand-written :file:`fairgraph/openminds/__init__.py`, which makes the v4 classes available
under their legacy :mod:`fairgraph.openminds.<domain>` paths, is not generated and is left alone.

After regenerating, review the diff before committing, to check that the changes introduced
look correct.

Reverse properties (links pointing *into* a class) get their names from the
``reverse_name_map`` dictionary at the top of :file:`builder/update_openminds.py`; if a new
schema introduces a property that has no entry there, generation fails with a :exc:`KeyError`
naming the class, and an entry needs to be added.

Each class's ``sort_property``, the property by which query results are sorted, is chosen by
``get_sort_property()`` in :file:`builder/update_openminds.py`: the first property in
``SORT_PROPERTY_PRIORITY`` that the class has, unless the class has an entry in ``custom_sort_properties``.

.. warning::

   Everything under :file:`fairgraph/openminds/v4` and :file:`fairgraph/openminds/v5` is
   generated, and any edit you make there by hand will be silently lost the next time the
   builder runs. To change the behaviour of a generated class, edit its *overlay* instead
   (see below).

Hand-written methods on generated classes
-----------------------------------------

Some generated classes need methods that cannot be derived from the schema, such as
:meth:`Person.me` or :meth:`DatasetVersion.download`. These live in
:file:`builder/additional_methods/`, one file per class, named after the class with a
:file:`.py.txt` suffix — for example :file:`builder/additional_methods/Person.py.txt`.

When the builder generates a class, it looks for a file matching that class name and, if
one exists, inserts its contents verbatim into the body of the generated class. The file
therefore contains method definitions only — no ``class`` statement — indented by four
spaces as they will appear in the class body::

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

So, to add or change a method on a generated class, edit (or create) the corresponding
file in :file:`builder/additional_methods/` and re-run :file:`update_openminds.py`.
Both the overlay and the regenerated file should be committed together.

Running the test suite
----------------------

Before you make any changes, run the test suite to make sure all the tests pass
on your system. In the top-level fairgraph directory, run::

    $ pytest

At the end, if you see "OK", then all the tests
passed (or were skipped because certain dependencies are not installed),
otherwise it will report on tests that failed or produced errors.

A large number of skipped tests is expected. Many tests run real queries, and are
skipped unless the environment variable :envvar:`KG_AUTH_TOKEN` contains a valid EBRAINS
authentication token. The remaining tests run offline against a mock client, so you can develop
and test most changes without any credentials.

To run the full suite, obtain a token and set it in your environment::

    $ export KG_AUTH_TOKEN=<your token>
    $ pytest

The tests run against the pre-production Knowledge Graph, never production. If you do not have an
EBRAINS account, anyone with an academic affiliation (which includes most students) can
sign up directly at https://ebrains.eu/sign-up.

To run tests from an individual file::

    $ pytest test/test_queries.py

Coding standards and style
--------------------------

All code should conform as much as possible to `PEP 8`_.
We use black_ to auto-format the code, with a line length of 119 characters.
Please run ``black`` before making a commit.

As a basic check of code quality, run::

    $ flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

Writing tests
-------------

You should try to write automated tests for any new code that you add. If you
have found a bug and want to fix it, first write a test that isolates the bug
(and that therefore fails with the existing codebase). Then apply your fix and
check that the test now passes.

To see how well the tests cover the code base, run::

    $ pytest --cov=fairgraph

Working on the documentation
----------------------------

All modules, classes, functions, and methods (including private and subclassed
builtin methods) should have docstrings.
Please see `PEP 257`_ for a description of docstring conventions.

The documentation is written in `reStructuredText`_, using the `Sphinx`_
documentation system.

To build the documentation::

    $ cd doc
    $ make html

Then open `_build/html/index.html` in your browser.

Committing your changes
-----------------------

Once you are happy with your changes, **run the test suite again to check
that you have not introduced any new bugs**. It is also recommended to check
your code with a code checking program, such as pyflakes or flake8.  Then
you can commit them to your local repository::

    $ git commit -m 'informative commit message'

If this is your first commit to the project, please add your name, ORCID if you have one, and
affiliation/employer to :file:`doc/authors.json`

You can then push your changes to your online repository on GitHub::

    $ git push origin informative-branch-name

(A reminder that we recommend working in a git branch other than "master").
Once you think your changes are ready to be included in the main fairgraph repository,
open a pull request on GitHub
(see https://help.github.com/en/articles/about-pull-requests).


Dealing with pull requests
--------------------------

Anyone is welcome to review a pull request, although only project maintainers are able to merge them.

- do the CI test pass?
- review the code - at least one person
- give feedback - be sure to thank the contributor, especially if it is a first time contribution!

Versioning
----------

fairgraph uses `semantic versioning`_: release numbers take the form ``MAJOR.MINOR.PATCH``.

Until version 1.0, the API should not be considered stable. As semantic versioning allows for
``0.y.z`` releases, incompatible changes may appear in any release; they are described in the
release notes, and where practical the previous behaviour keeps working for at least one release
while emitting a :exc:`DeprecationWarning`.

From version 1.0 onwards, the public API is a commitment:

* **major** releases may change the public API in incompatible ways;
* **minor** releases add functionality while remaining backwards compatible;
* **patch** releases contain only bug fixes.

Between releases, the ``master`` branch carries a development version: the version being worked
towards, with ``.dev0`` appended. For example, after 0.14.0 was released, ``master`` moved to ``0.15.0.dev0``.

Two files hold the version, and they must agree:

* :file:`pyproject.toml`, as ``project.version``
* :file:`fairgraph/__init__.py`, as ``__version__``

The documentation is not a third place to edit: :file:`doc/conf.py` reads the version from
:file:`pyproject.toml` when the docs are built.

:file:`codemeta.json` is deliberately **not** part of this set. It describes the most recent
*release* rather than the current state of ``master``, so it keeps the released version number
between releases. Its ``downloadUrl`` and ``identifier`` point at the release artefact on PyPI,
so giving it a development version would advertise a download that does not exist. It is
regenerated as part of the release commit, and its ``downloadUrl`` is filled in once the
release is on PyPI, as described below.

Making a release
----------------

Add a section in :file:`/doc/release_notes.rst` for the release.

First check that the version string (in :file:`pyproject.toml` and :file:`fairgraph/__init__.py`) is correct.

Regenerate :file:`codemeta.json` from the local project metadata (:file:`pyproject.toml` and
:file:`doc/authors.json`), and include it in the release commit::

    $ cd doc
    $ python build_codemeta.py

This updates all fields for the new version except ``downloadUrl``, which is set to ``null``
since the release is not yet on PyPI.

To build source and wheel packages::

    $ python -m build

Tag the release in the Git repository and push it::

    $ git tag <version>
    $ git push --tags origin
    $ git push --tags upstream

To upload the package to `PyPI`_ (the members of the `maintainers team`_ have the necessary permissions to do this)::

    $ twine upload dist/fairgraph-x.y.z.tar.gz dist/fairgraph.x.y.z-py3-none-any.whl

Once the release is on PyPI, fill in the ``downloadUrl`` in :file:`codemeta.json`, and commit.
This reads the URL of the source distribution from PyPI, so it can only be done after the upload
has completed. If the upload was made on a later day than the release commit, ``dateModified``
is also updated to the date of the upload::

    $ cd doc
    $ python build_codemeta.py --download-url

Finally, open the next development version: set the version strings in :file:`pyproject.toml`
and :file:`fairgraph/__init__.py` to the next release number with ``.dev0`` appended, and commit.

Governance
----------

fairgraph is maintained by Andrew Davison.
If the project begins to attract a larger number of regular contributors
we will transition to a more democratic governance model.
The copyright is held jointly by all contributors and/or their employers at the time of contribution,
as listed in :file:`doc/authors.rst`.
fairgraph is licenced under the Apache Software Licencse v2.0.


.. _`GitHub Repository`: https://github.com/HumanBrainProject/fairgraph/
.. _`PEP 8`: https://peps.python.org/pep-0008/
.. _`maintainers team`: https://github.com/orgs/HumanBrainProject/teams/fairgraph-maintainers
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://www.sphinx-doc.org/
.. _`PEP 257`: https://www.python.org/dev/peps/pep-0257/
.. _black: https://black.readthedocs.io
.. _PyPI: https://pypi.org
.. _milestones: https://github.com/HumanBrainProject/fairgraph/milestones
.. _`semantic versioning`: https://semver.org
