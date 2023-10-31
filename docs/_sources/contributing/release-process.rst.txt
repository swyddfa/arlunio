Release Process
===============

While the process of making beta releases is completely automated, in order to
make a "real" release there are some manual steps that still need to be
performed. This page serves as a checklist to make sure that no steps are
forgotten

1. Start the release process by opening a pull request in the main
   `swyddfa/arlunio`_ repository, one that looks to merge :code:`develop`
   into :code:`master`

2. On a local copy of the :code:`develop` branch, generate the changelog entry
   for this release with :code:`towncrier`::

      (.env) $ towncrier --version=v<VERSION>

   It will ask if it is ok to delete the changelog snippets in the
   :code:`changes/` directory. Say yes.

3. Commit and push the removal of these files along with the updated changelog
   to update the pull request.

4. Wait to ensure that all the workflow actions pass before merging the pull
   request with the :code:`Create a merge commit` option. The merge will then
   trigger the automated release pipeline which will package :code:`arlunio`
   and publish it to PyPi.

5. Once the pipline has finished it will have created the release on our
   `releases`_ page, but the changelog entry will be missing. However the entry
   should be identical to the previous beta release, so copy and paste it over.

6. Delete the :code:`build-number-X` tag to reset the beta version counter.

7. Checkout the :code:`master` branch locally and pull down the latest changes.

8. Checkout :code:`develop` and merge in :code:`master`

9. Bump the version number in :code:`arlunio/_version.py` to the next candidate
   release number.

10. Commit and push to the :code:`develop` branch.

.. _releases: https://github.com/swyddfa/arlunio/releases/
.. _swyddfa/arlunio: https://github.com/swyddfa/arlunio
