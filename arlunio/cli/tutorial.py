import logging
import os
import shutil
import time

import pkg_resources

from .runner import Runner

logger = logging.getLogger(__name__)


class Tutorial:
    def __init__(self, context):
        self.context = context
        self.runner = Runner(context)

    def copy_resources(self, destination):
        """Copy the tutorial resources to the given destination."""
        logger.debug(f"Copying tutorial resources to: {destination}")
        os.makedirs(destination)

        def exclude_item(item, path):
            return any([item.startswith("."), "__" in item])

        for item in pkg_resources.resource_listdir("stylo.tutorial", "."):
            path = pkg_resources.resource_filename("stylo.tutorial", item)

            if exclude_item(item, path):
                logger.debug(f"--> {item}, skipping")
                continue

            logger.debug(f"--> {item}")
            dest = os.path.join(destination, item)

            if os.path.isdir(path):
                shutil.copytree(path, dest, copy_function=shutil.copy)
            else:
                shutil.copy(path, dest)

    def launch(self, edit, reset):
        """Launch a jupyter lab instance in the tutorial directory.

        For developers there is a hidden `--edit` flag that can be used to open
        an instance that will allow us to edit the source of the tutorial.
        """
        if not edit:
            tutorial_dir = os.path.join(self.context.cache_dir, "tutorial")

            if reset and os.path.exists(tutorial_dir):
                logger.debug("Removing existing tutorial content.")
                shutil.rmtree(tutorial_dir)

            if not os.path.exists(tutorial_dir):
                logger.debug(f"Tutorial content does not exist")
                self.copy_resources(tutorial_dir)
        else:
            logger.debug("Editing tutorial sources")
            tutorial_dir = pkg_resources.resource_filename("stylo.tutorial", "")

        logger.info("Launching tutorial...")

        cmds = [f"cd {tutorial_dir}", "jupyter-lab"]
        self.runner.launch(cmds)

        time.sleep(1)


def register(cli, click):
    """Here we expose our command line interface."""

    @cli.command()
    @click.option("-e", "--edit", is_flag=True, hidden=True)
    @click.option(
        "-r", "--reset", is_flag=True, help="Reset the tutorial to its default state."
    )
    @click.pass_obj
    def tutorial(context, edit, reset):
        """Launch the tutorial."""

        tutorial = Tutorial(context)
        tutorial.launch(edit, reset)
