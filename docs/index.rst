.. Python Packager documentation master file, created by
   sphinx-quickstart on Fri Feb 10 12:11:25 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Packager's documentation!
===========================================

.. toctree::
   :maxdepth: 2
   

Installation
============

::

    pip install python-packager

Getting started
===============

If you need an entirely fresh package then you can do this::

    pythonpackager create

You can also pass a few options to the `create` command. See the help for details::

    pythonpackager help create


If you already have a package you can release it using::

    pythonpackager release

Again, options are documented here::

    pythonpackager help release

**Notes on releasing:** The release process makes a bunch of assumptions 
about your project. If you created your project using the `create` command, 
then you are probably fine, but you may need to do a little hacking otherwise.

Source
======

Is on GitHub_.

The name
========

Sucks, any suggestions?

.. _GitHub: https://github.com/adamcharnock/python-packager