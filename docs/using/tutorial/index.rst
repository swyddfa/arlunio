.. _using_tutorial:

Tutorial
========

.. toctree::
   :hidden:

   getstarted/index

.. nbtutorial::


.. only:: html

   .. note::

      There is also an interactive version of this tutorial available if you have
      :code:`stylo` setup on your machine. It can be launched by running the command::

          $ stylo tutorial

      This will start a `Jupyter Lab`_ instance that contains an interactive notebook
      version of this tutorial.

Welcome to stylo's tutorial! If this is your first time here please do take the
time to read through this page to help you get the most out of it. However
before we go any further it is worth checking that you have the latest version
of :code:`stylo`

.. doctest::

   >>> import stylo as st
   >>> st.__version__
   '0.10.0'

About this Tutorial
-------------------

This tutorial is broken down into a number of sections each focused on a
particular aspect of stylo. The sections are self contained so feel free to
jump around and see where your interests take you. However keep in mind that
each of tutorials within a section will build up each other so be sure to
tackle them in order. Each tutorial will contain a number of examples and some
short excercises which aim to demonstrate the core ideas and how they can be
used in practise.

Currently the following sections are available.

.. |Getting Started| replace:: :ref:`Getting Started: <using_tutorial_getstarted>`

- |Getting Started| If you are new to stylo start here.
- **Background:** There are a number of mathematical concepts at play in the
  core of stylo. While it's not necessary to understand them it can certainly
  help to at least be familiar with them. The tutorials in this section aim to
  introduce these concepts to you.


.. only:: nbtutorial

   Resetting the Tutorial
   ----------------------

   You are free to play around with and change **any** of the code you see here
   in this tutorial - in fact we encourage it! The only way you are truly going
   to develop an intuition for how the various concepts in stylo interact is to
   experiment. Dont't worry about breaking anything either, if you ever get to
   the point where you wish you could start over you can! At any time you can
   relaunch the tutorial with the command :code:`stylo tutorial --reset` which
   will reset **everything** back to its default state so that you can start
   fresh.

   **This command will revert any changes you make to the tutorial - including
   deleting any additional notebooks you have created. Be sure to back up anything
   you wish to save before running this command.**


.. _Jupyter Lab: https://jupyterlab.readthedocs.io/en/stable/