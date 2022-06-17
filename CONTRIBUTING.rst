Contributor Guide
=========================================

.. contents:: Table of Contents
  :local:

.. _contributing_get-started:

Where to Start?
-----------------------------

All contributions, bug reports, bug fixes, documentation improvements,
enhancements, and ideas are welcome!

If you are new to open-source development or Dataverse Tests, we recommend going
through the `GitHub issues <https://github.com/gdcc/dataverse_tests/issues>`_,
to find issues that interest you. Once you've found an interesting issue, you can return here to
get your development environment setup.

When you start working on an issue, it’s a good idea to assign the issue
to yourself so that nobody else duplicates the work on it. GitHub restricts
assigning issues to maintainers of the project only. To let us know, please
add a comment to the issue so that everyone knows that you are working
on the issue.

If for whatever reason you
are not able to continue working with the issue, please try to unassign it so that
other people know it’s available again. You can periodically check the list of assigned issues,
since people may not be working in them anymore. If you want to work on one that
is assigned, feel free to kindly ask the current assignee if you can take it
(please allow at least a week of inactivity before considering work in the issue
discontinued).

This project and everyone participating in it is governed by the Dataverse Tests
`Code of Conduct <https://github.com/gdcc/dataverse_tests/blob/master/CODE_OF_CONDUCT.md>`_.
By participating, you are expected to uphold this code. Please report
unacceptable behaviour.

**Be respectful, supportive and nice to each other!**

.. _contributing_create-issues:

Bug reports, enhancement requests and other issues
----------------------------------------------------

Bug reports are an important part of making Dataverse Tests more stable. Having
a complete bug report will allow others to reproduce the bug and provide
insight into fixing the issue.

Trying the bug-producing code out on the ``master`` branch is often a
worthwhile exercise to confirm the bug still exists. It is also worth
searching existing bug reports and pull requests to see if the issue
has already been reported and/or fixed.

Other reasons to create an issue could be:

* suggesting new features
* sharing an idea
* giving feedback

Please check some things before creating an issue:

* Your issue may already be reported! Please search on the `issue tracker <https://github.com/gdcc/dataverse_tests/issues>`_ before creating one.
* Is this something you can **develop**? Send a pull request!

Once you have clicked `New issue <https://github.com/gdcc/dataverse_tests/issues>`_,
you have to choose one of the issue templates:

* Bug report (`template <https://github.com/gdcc/dataverse_tests/blob/master/.github/ISSUE_TEMPLATE/bug-template.md>`_)
* Feature request (`template <https://github.com/gdcc/dataverse_tests/blob/master/.github/ISSUE_TEMPLATE/feature-template.md>`_)
* Issue: all other issues, except bug reports and feature requests (`template  <https://github.com/gdcc/dataverse_tests/blob/master/.github/ISSUE_TEMPLATE/issue-template.md>`_)

After selecting the appropriate template, you will see some explanatory text. Follow it
step-by-step. After clicking `Submit new issue`, the issue will then show up
to the Dataverse Tests community and be open to comments/ideas from others.

Besides creating an issue, you also can contribute in many other ways by:

* sharing your knowledge in Issues and Pull Requests
* reviewing `pull requests <https://github.com/gdcc/dataverse_tests/pulls>`_
* talking about Dataverse Tests and sharing it with others


.. _contributing_working-with-code:

Working with the code
-----------------------------

Now that you have an issue you want to fix, an enhancement to add, or
documentation to improve, you need to learn how to work with GitHub
and the Dataverse Tests code base.


.. _contributing_working-with-code_version-control:

Version control, Git, and GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To the new user, working with Git is one of the more daunting aspects
of contributing to Dataverse Tests. It can very quickly become overwhelming, but
sticking to the guidelines below will help keep the process straightforward
and mostly trouble free. As always, if you are having difficulties please
feel free to ask for help.

The code is hosted on `GitHub <https://github.com/>`_. To contribute you will need
to sign up for a `free GitHub account <https://github.com/signup/free>`_.
We use `Git <https://git-scm.com/>`_ for version control to allow many people to
work together on the project.

A great resource for learning Git: the `GitHub help pages <https://help.github.com/>`_

There are many ways to work with git and Github. Our workflow is inspired by the
`GitHub flow <https://guides.github.com/introduction/flow/>`_ and
`Git flow <https://nvie.com/posts/a-successful-git-branching-model/>`_ approaches.


.. _contributing_working-with-code_git:

Getting started with Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`GitHub has instructions <https://help.github.com/set-up-git-redirect>`_ for
installing git, setting up your SSH key, and configuring git. All these steps
need to be completed before you can work seamlessly between your local
repository and GitHub.


.. _contributing_working-with-code_forking:

Forking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need your own fork to work on the code. Go to the
`Dataverse Tests project page <https://github.com/gdcc/dataverse_tests/>`_ and hit
the Fork button. You will want to clone your fork to your machine:

.. code-block:: shell

  git clone https://github.com/YOUR_USER_NAME/dataverse_tests.git
  cd dataverse_tests
  git remote add upstream https://github.com/gdcc/dataverse_tests.git

This creates the directory `dataverse_tests` and connects your repository
to the upstream (main project) Dataverse Tests repository.


.. _contributing_working-with-code_development-environment:

Creating a development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To test out code changes, you’ll need to build Dataverse Tests from source,
which requires a Python environment.

**Install pipenv**

See the `pipenv documentation <https://github.com/pypa/pipenv>_` for more information.

**Creating a Python environment**

Install requirements with pipenv.

.. code-block:: shell

  pipenv install --dev


.. _contributing_working-with-code_create-branch:

Creating a branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You want your ``develop`` branch to reflect only release-ready code,
so create a feature branch for making your changes. Use a
descriptive branch name and replace `BRANCH_NAME` with it, e. g.

.. code-block:: shell

  git checkout develop
  git checkout -b BRANCH_NAME

This changes your working directory to the `BRANCH_NAME` branch.
Keep any changes in this branch specific to one bug or feature so it is
clear what the branch brings to Dataverse Tests. You can have many
branches and switch between them using the git checkout command.

When creating this branch, make sure your ``develop`` branch is up to date
with the latest upstream ``develop`` version. To update your local ``develop``
branch, you can do:

.. code-block:: shell

  git checkout develop
  git pull upstream develop --ff-only

When you want to update the feature branch with changes in ``develop`` after
you created the branch, check the section on
:ref:`updating a PR <contributing_changes_update-pull-request>`.


.. _contributing_code:

Contributing to the code base
-----------------------------

Writing good code is not just about what you write. It is also about
how you write it. During testing, several tools will be run to check
your code for stylistic errors. Thus, good style is suggested for
submitting code to Dataverse Tests.

You can open a Pull Request at any point during the development process:
when you have little or no code but want to share some screenshots or
general ideas, when you're stuck and need help or advice, or when you're
ready for someone to review your work.


.. _contributing_code_tests:

Add tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Create new test**

* ``test_`` as filename prefix.
  * descriptive test name, e. g. ``test_oaipmh.json``
* Class name:
  * ``Test`` as prefix
  * Name should be descriptive for the type of tests clustered inside the Class, e. g. ``TestAccess``
* Method name:
  * ``test_```as prefix
  * descriptive name, which should tell what the test is doing by reading it (e. g. ``test_pid_url_not_logged_in``)
* Markers: see in ``setup.cfg``
* ``users``: list of user dicts loaded from ``user/DATAVERSE_INSTALLATION.json``
* ``input-expected``: input data and expected results loaded from the configs JSON.

**Add missing Dataverse versions**

* Check out ``configs/default/`` for existing Dataverse version configuration. Copy and adapt them as a starting point.
  * ``xpaths.json``: Dataverse version specific xpaths used in the tests.
  * ``form-data_create-dataverse.json``: xpaths for the create dataverse form.
  * ``terms-of-use.html``: default html for terms of use
* Run tests on your Dataverse installation, which runs a Dataverse version which is still missing
* Add new marker

**Custom testing functions**

If you want to add a custom test function in ``src/dvtests/testing/conftest.py``
, use ``custom_`` as prefix for the function name.


.. _contributing_code_standards:

Code standards
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dataverse Tests follows the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
standard and uses `Black <https://black.readthedocs.io/en/stable/>`_,
`Flake8 <https://flake8.pycqa.org/en/latest/>`_ and
`pylint <https://www.pylint.org/>`_  to ensure a consistent code format
throughout the project.

**Imports**

In Python 3, absolute imports are recommended.

Import formatting: Imports should be alphabetically sorted within
the sections.


**String formatting**

Dataverse Tests uses f-strings formatting instead of ‘%’ and ‘.format()’
string formatters.

.. _contributing_code_pre-commit:

Pre-commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can run many of the styling checks manually. However, we encourage
you to use `pre-commit <https://pre-commit.com/>`_ hooks instead to
automatically run ``black`` when you make a git commit.

This can be done by installing ``pre-commit`` (which should
already be installed by Pipenv).

To activate it, only run:

.. code-block:: shell

  pre-commit install

from the root of the Dataverse Tests repository. Now styling
checks will be run each time you commit changes without your needing to
run each one manually. In addition, using pre-commit will also allow you
to more easily remain up-to-date with our code checks as they change.

To run black alone, use

.. code-block:: shell

  black src/dvtests/file_changed.py


.. _contributing_code_type-hints:

Type hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dataverse Tests strongly encourages the use of
`PEP 484 <https://www.python.org/dev/peps/pep-0484>`_
style type hints. New development should contain type hints!

**Validating type hints**

Dataverse Tests uses `mypy <http://mypy-lang.org/>`_ to statically analyze the code base and
type hints. After making any change you can ensure your type hints are correct by running

.. code-block:: shell

  mypy src/dvtests/file_changed.py


.. _contributing_changes:

Contributing your changes to Dataverse Tests
-----------------------------------------

.. _contributing_changes_commit:

Committing your code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before committing your changes, make clear:

- You are on the right branch
- All style and code checks for your change ran successful (mypy, pylint, flake8)
- Keep style fixes to a separate commit to make your pull request more readable

Once you’ve made changes, you can see them by typing:

.. code-block:: shell

  git status

If you have created a new file, it is not being tracked by git. Add it by typing:

.. code-block:: shell

  git add path/to/file-to-be-added.py

Doing ``git status`` again should give something like:

.. code-block:: shell

  # On branch BRANCH_NAME
  #
  #       modified:   relative/path/to/file-you-added.py
  #

Finally, commit your changes to your local repository with an explanatory message.

The following defines how a commit message should be structured. Please reference
the relevant GitHub issues in your commit message using #1234.

- a subject line with < 80 chars.
- One blank line.
- Optionally, a commit message body.

Dataverse Tests uses a
`commit message template <https://github.com/gdcc/dataverse_tests/blob/master/.github/.gitmessage.txt>`_
to pre-fill the commit message, once you create a commit. We recommend,
using it for your commit message.

Now, commit your changes in your local repository:

.. code-block:: shell

  git commit


.. _contributing_changes_push:

Pushing your changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you want your changes to appear publicly on your GitHub page,
push your forked feature branch’s commits:

.. code-block:: shell

  git push origin BRANCH_NAME

Here origin is the default name given to your remote repository on GitHub.
You can see the remote repositories:

.. code-block:: shell

  git remote -v

If you added the upstream repository as described above you will see something like:

.. code-block:: shell

  origin  git@github.com:YOUR_USER_NAME/dataverse_tests.git (fetch)
  origin  git@github.com:YOUR_USER_NAME/dataverse_tests.git (push)
  upstream        git://github.com/gdcc/dataverse_tests.git (fetch)
  upstream        git://github.com/gdcc/dataverse_tests.git (push)

Now your code is on GitHub, but it is not yet a part of the Dataverse Tests project.
For that to happen, a pull request needs to be submitted on GitHub.


.. _contributing_changes_review:

Review your code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you’re ready to ask for a code review, file a pull request.
Before you do, once again make sure that you have followed all the
guidelines outlined in this document regarding code style, tests and
documentation. You should also double check your branch changes against
the branch it was based on:

- Navigate to your repository on GitHub – ``https://github.com/YOUR_USER_NAME/dataverse_tests``
- Click on the ``Compare & create pull request`` button for your `BRANCH_NAME`
- Select the base and compare branches, if necessary. This will be ``develop`` and ``BRANCH_NAME``, respectively.


.. _contributing_changes_pull-request:

Finally, make the pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If everything looks good, you are ready to make a pull request. A
pull request is how code from a local repository becomes available
to the GitHub community and can be looked at and eventually merged
into the ``develop`` version. This pull request and its associated changes
will eventually be committed to the ``master`` branch and available in
the next release. To submit a pull request:

- Navigate to your repository on GitHub
- Click on the ``Pull Request`` button
- You can then click on ``Commits`` and ``Files Changed`` to make sure everything looks okay one last time
- Write a description of your changes in the ``Preview Discussion`` tab. A `pull request template <https://github.com/gdcc/dataverse_tests/blob/master/.github/PULL_REQUEST_TEMPLATE.md>`_ is used to pre-fill the description. Follow the explainationi in it.
- Click ``Send Pull Request``.

This request then goes to the repository maintainers, and they will review the code.

By using GitHub's @mention system in your Pull Request message, you can
ask for feedback from specific people or teams, whether they're down
the hall or ten time zones away.

Once you send a pull request, we can discuss its potential modifications and
even add more commits to it later on.

There's an excellent tutorial on how Pull Requests work in the
`GitHub Help Center <https://help.github.com/articles/using-pull-requests/>`_.


.. _contributing_changes_update-pull-request:

Updating your pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the review you get on your pull request, you will probably
need to make some changes to the code. In that case, you can make
them in your branch, add a new commit to that branch, push it to
GitHub, and the pull request will be automatically updated. Pushing
them to GitHub again is done by:

.. code-block:: shell

  git push origin BRANCH_NAME

This will automatically update your pull request with the latest code.

Another reason you might need to update your pull request is to solve
conflicts with changes that have been merged into the ``develop`` branch
since you opened your pull request.

To do this, you need to “merge upstream develop“ in your branch:

.. code-block:: shell

  git checkout BRANCH_NAME
  git fetch upstream
  git merge upstream/develop

If there are no conflicts (or they could be fixed automatically), a
file with a default commit message will open, and you can simply save
and quit this file.

If there are merge conflicts, you need to solve those conflicts. See
for example in
`the GitHub tutorial on merge conflicts <https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/>`_
for an explanation on how to do this. Once the conflicts are merged
and the files where the conflicts were solved are added, you can run
``git commit`` to save those fixes.

If you have uncommitted changes at the moment you want to update the
branch with ``develop``, you will need to ``stash`` them prior to updating
(see the `stash docs <https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning>`_).
This will effectively store your changes and they can be reapplied after updating.

After the feature branch has been update locally, you can now update your
pull request by pushing to the branch on GitHub:

.. code-block:: shell

  git push origin BRANCH_NAME


.. _contributing_changes_delete-merged-branch:

Delete your merged branch (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once your feature branch is accepted into upstream, you’ll probably
want to get rid of the branch. First, merge upstream develop into your
branch so git knows it is safe to delete your branch:

.. code-block:: shell

  git fetch upstream
  git checkout develop
  git merge upstream/develop

Then you can do:

.. code-block:: shell

  git branch -d BRANCH_NAME

Make sure you use a lower-case -d, or else git won’t warn you if your
feature branch has not actually been merged.

The branch will still exist on GitHub, so to delete it there do:

.. code-block:: shell

  git push origin --delete BRANCH_NAME


.. _contributing_changes_tips:

Tips for a successful pull request
-----------------------------------------

If you have made it to the
:ref:`Review your code <contributing_changes_review>` phase
, one of the core
contributors may take a look. Please note however that a handful of
people are responsible for reviewing all of the contributions, which
can often lead to bottlenecks.

To improve the chances of your pull request being reviewed, you should:

- **Reference an open issue** for non-trivial changes to clarify the PR’s purpose
- **Keep your pull requests as simple as possible**. Larger PRs take longer to review
- Keep :ref:`updating your pull request <contributing_changes_update-pull-request>`, either by request or every few days


.. _contributing_after-pull-request:

What happens after the pull
-----------------------------------------


.. _contributing_after-pull-request_review:

Reviewing the Pull request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once a new issue is created, a maintainer adds
`labels <https://github.com/gdcc/dataverse_tests/labels>`_
, an assignee and a
`milestone <https://github.com/gdcc/dataverse_tests/milestones>`_
to it. Labels are used to separate between issue types and the
status of it, show effected module(s) and to prioritize tasks.
Also at least one responsible person for the next steps is assigned
, and often a milestone too.

The next steps may consist of requests from the assigned person(s)
for further work, questions on
some changes or the okay for the pull request to be merged.

Once all actions are done, including review and documentation, the issue
gets closed. The issue then lives on as an open and transparent
documentation of the work done.


.. _contributing_after-pull-request_create-release:

Create a release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, to plan a release, the maintainers:

- define, which issues are part of it and the version number
- create a new milestone for the release (named after the version number)
- and assign all selected issues to the milestone

Once all issues related to the release are closed (except the ones
related to release activities), the release can be created. This includes:

- review documentation and code changes
- write release notes
- write a release announcement
- update version number
- merge ``develop`` to ``master``
- tag release name to commit (e. g. ``0.3.2``), push branch and create pull request

You can find the full release history at :ref:`community_history` and on
`GitHub <https://github.com/gdcc/dataverse_tests/releases>`_.

**Versioning**

For Dataverse Tests, `Semantic versioning <https://semver.org/>`_ is used for releases.
