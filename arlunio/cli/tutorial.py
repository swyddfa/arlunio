import logging
import os
import shutil
import subprocess

import pkg_resources

import appdirs

logger = logging.getLogger(__name__)


class Tutorial:
    """Launch the interactive tutorial.

    This will launch a jupyter-lab instance in a folder containing a collection
    of jupyter notebook files that contain the tutorial. These files are yours
    and you are free to edit them as you see fit.

    You can also reset the tutorial at any time by launching the tutorial
    with the --reset flag. WARNING: This will delete any changes you have
    made to the tutorial directory, be sure to back up anything you wish to
    preserve BEFORE running the command with this flag

    :param reset: reset the tutorial to its default state
    """

    def _copy_resources(self, destination):
        """Copy the tutorial resources to the given destination."""
        logger.debug(f"Copying tutorial resources to {destination}")
        os.makedirs(destination)

        def exclude_item(item, path):
            return any([item.startswith("."), "__" in item])

        for item in pkg_resources.resource_listdir("arlunio.tutorial", "."):
            path = pkg_resources.resource_filename("arlunio.tutorial", item)

            if exclude_item(item, path):
                logger.debug(f"--> {item}, skipping")
                continue

            logger.debug(f"--> {item}")
            dest = os.path.join(destination, item)

            if os.path.isdir(path):
                shutil.copytree(path, dest, copy_function=shutil.copy)
            else:
                shutil.copy(path, dest)

    def run(self, reset: bool = False):
        tutorial_dir = os.path.join(
            appdirs.user_data_dir(appname="arlunio", appauthor="swyddfa"), "tutorial"
        )

        if reset and os.path.exists(tutorial_dir):
            logger.info("Existing tutorial found found, resetting...")
            shutil.rmtree(tutorial_dir)

        if not os.path.exists(tutorial_dir):
            logger.info("Copying tutorial resources...")
            self._copy_resources(tutorial_dir)

        subprocess.run(["jupyter-lab"], cwd=tutorial_dir)
