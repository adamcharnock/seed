.. Seed documentation master file, created by
   sphinx-quickstart on Fri Feb 10 12:11:25 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Seed's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   

Seed is an experiment in making releasing PyPi packages trivially 
easy. For example, the ``release`` command will:

* Increment the version number in ``__init__.py``
* Update CHANGES.txt with commit summaries & authors
* Tag the release
* Commit the above changes
* Register/upload your package to PyPi

I am not sure if a need for this exists, but my hope is that it will 
lower the time & effort needed to create and release Python packages.

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

If you need an entirely fresh package then you can do this::

    seed create

You can also pass a few options to the ``create`` command. See the help for details::

    seed help create


If you already have a package you can release it using::

    seed release

Again, options are documented here::

    seed help release

**Notes on releasing:** The release process makes a bunch of assumptions 
about your project. If you created your project using the ``create`` command, 
then you are probably fine, but you may need to do a little hacking otherwise.

Source
======

Is on `GitHub <https://github.com/adamcharnock/seed>`_.

Other notes & about the author
==============================

The structure of Seed is heavily based on that of `pip <https://github.com/pypa/pip/>`_. 
It is still a bit rough around the edges, but the basic stuff is there.

I find myself managing a lot of packages as I always have a number of Django projects on the go 
and sharing reusable code is always a plus. I also use Heroku a lot, but Heroku doesn't play 
nicely when installing dependencies via external URLs, hence my desire to release more packages 
to PyPi rather than just installing them right out of GutHub.

You can find me on...

* `Twitter <http://twitter.com/adamcharnock>`_
* `GitHub <http://github.com/adamcharnock>`_

I work on...

* `PlayNice.ly <http://playnice.ly>`_ - Project management for software developers
* `Continuous.io <http://continuous.io>`_ - Hosted continuous integration (beta)