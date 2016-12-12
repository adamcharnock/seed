.. Seed documentation master file, created by
   sphinx-quickstart on Fri Feb 10 12:11:25 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Seed
===========

.. toctree::
   :maxdepth: 2
   

Seed is designed to make releasing PyPi packages trivially
easy. For example, the ``release`` command will:

* Increment the version number in ``VERSION``
* Update CHANGES.txt with commit summaries & authors
* Tag the release
* Commit the above changes
* Register/upload your package to PyPi

Requires Python >= 2.7 or Python >= 3.4

Installation
============

Installing Seed is easy using pip::

    pip install seed

PyPi registration
-----------------

To start releasing packages you are also going to need to 
`register with PyPi <http://pypi.python.org/pypi?%3Aaction=register_form>`_. Now place 
your login details into ``~/.pypirc`` as follows::

    [server-login]
    username:yourusername
    password:yourpassword

.. note::

    Storing your password in plaintext is clearly not ideal. If anyone knows of a workaround
    I would love to hear it.

Getting started
===============

Packages without existing releases
----------------------------------

If you need an entirely fresh package then you can create a skeleton as follows::

    seed create --dry-run  # Do a dry run to make sure everything looks right
    seed create

You can also pass a few options to the ``create`` command. See the help for details::

    seed help create

You can then do a release using::

    # For the first release you must use --initial:
    seed release --initial

    # Subsequent releases can be done via ONE of:
    seed release --bug    # A bug version pump (i.e. 0.0.1)
    seed release --minor  # A minor version pump (i.e. 0.1.0)
    seed release --major  # A major version pump (i.e. 1.0.0)
    seed release          # Equivalent to seed release --bug

    # More details about how to perform releases
    seed help release


Packages with existing releases
----------------------------------

Packages with existing release will need the following:

 * A ``/VERSION`` file containing the latest version, such as ``1.2.0``
 * A git tag with the same name as the version (i.e. ``1.2.0``) pointing to the relevant commit

You can then release it using::

    # Do a dry run to make sure everything looks right
    seed release --dry-run

    # Do the release using ONE of:
    seed release --bug    # A bug version pump (i.e. 0.0.1)
    seed release --minor  # A minor version pump (i.e. 0.1.0)
    seed release --major  # A major version pump (i.e. 1.0.0)
    seed release          # Equivalent to seed release --bug

    # More details about how to perform releases
    seed help release


Change log
==========

0.11.2
------

 * Default package creation now supports Manifest files by default

0.11.1
------

 * Dropping support for Python 2.6 & 3.3. Now supporting >= 2.7 and >= 3.4.

0.11.0
------

 * **Breaking change**: Tags are now created in the form '1.2.3' rather than 'v1.2.3'. This
   is a more standard notation but will cause issues with packages which are using the
   former notation. Solutions are:

   * Create a new tag in the form '1.2.3' which points to your latest release
   * Set the environment variable ``SEED_VERSION_PREFIX=v``


Source
======

Is on `GitHub <https://github.com/adamcharnock/seed>`_.

Credits & about the author
==========================

The structure of Seed is heavily based on that of `pip <https://github.com/pypa/pip/>`_.

You can find me on...

* `adamcharnock.com <https://adamcharnock.com>`_
* `GitHub <http://github.com/adamcharnock>`_

