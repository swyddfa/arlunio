.. _users:

User Guide
==========

.. nbtutorial::


Welcome to the user guide! It is made up from a number of guided projects that each try
to focus on a particular aspect of :code:`arlunio`. Each project should be self
contained so feel free to try them in whichever order you fancy.

.. only:: html

   .. note::

      There is also an interactive version of the user guide available if you
      have :code:`arlunio` setup on your machine. It can be launched by running
      the command::

         $ arlunio tutorial

      This will open a `Jupyter Lab`_ instance pointed at this section of the
      documentation.


.. only:: nbtutorial

   .. note::

      Being an interactive guide you are of course free to play around with and
      change **any** of the code you see here - in fact we encourage it! The
      only way to truly gain an intuition for how the concepts introduced here
      work will be to experiment.

      There's no need to worry about breaking anything either, if you ever get
      to the point where you wish you could start over you can! At any time you
      can close and re-launch the tutorial with the command
      :code:`arlunio tutorial --reset` which will reset this folder back to its
      default state.

      **This command will revert any changes to this folder - including
      deleting any additional notebooks you have created. Be sure to back up
      anything important before running this command.**


The user guide is made up of the following sections

- |Chess|: Build a tool for visualising chess games.

.. toctree::
   :hidden:

   chess/index


.. |Chess| replace:: :ref:`Chess <users_chess>`
.. _Jupyter Lab: https://jupyterlab.readthedocs.io/en/stable/