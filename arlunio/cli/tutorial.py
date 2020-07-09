import logging
import pathlib
import shutil
import subprocess

import appdirs
import pkg_resources

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

    def run(self, reset: bool = False):
        tutorial_dir = pathlib.Path(
            appdirs.user_data_dir(appname="arlunio", appauthor="swyddfa"), "tutorial"
        )

        if reset and tutorial_dir.exists():
            message = (
                "Existing tutorial resources detected\n"
                "This command will DELETE any existing tutorial resources\n\n"
            )
            logger.info(message)
            response = input("Do you wish to continue? [y/N] ")

            if not response.lower().startswith("y"):
                return 0

            shutil.rmtree(tutorial_dir)

        if not tutorial_dir.exists():
            src = pkg_resources.resource_filename("arlunio.tutorial", ".")
            shutil.copytree(src, tutorial_dir)
            logger.info("Copied tutorial resources to %s", tutorial_dir)

        try:
            subprocess.run(["jupyter-lab"], cwd=tutorial_dir)
        except FileNotFoundError:
            logger.info(
                "Unable to start jupyterlab, please make sure it is installed"
                " and try again"
            )
