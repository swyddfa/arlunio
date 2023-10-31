.. _users:

User Guide
==========

Welcome to the user guide! It is made up from a number of guided projects that
each try to focus on a particular aspect of :code:`arlunio`. Each project
should be self contained so feel free to try them in whichever order you fancy.

.. nbtutorial::

- :ref:`users_getstarted`: New users should start here.

.. only:: html

   .. tip::

      There is also an interactive version of the user guide available if you
      have :code:`arlunio` already setup on your machine. Though it requires a
      few extra dependencies which can be installed with the command::

         $ pip install arlunio[examples]

      Assuming you have everything installed, the interactive version of this
      guide can be launced with the command::

         $ arlunio tutorial


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

.. toctree::
   :hidden:

   getstarted/index
