import logging
import os
import shutil
import time

import pkg_resources

import arlunio.cli as cli

from .runner import Runner

logger = logging.getLogger(__name__)


class Tutorial(cli.Command):
    """Launch the interactive tutorial.

    This will launch a jupyter-lab instance in a folder containing a collection
    of jupyter notebook files that contain the tutorial. These files are yours
    and you are free to edit them as you see fit.

    You can also reset the tutorial at any time by launching the tutorial
    with the --reset flag. WARNING: This will delete any changes you have
    made to the tutorial directory, be sure to back up anything you wish to
    preserve BEFORE running the command with this flag

    :param reset: Reset the tutorial to its default state

    """

    def run(self, reset: bool = False):
        """Launch the tutorial.
        """

        if reset:
            print("I'm a resetted tutorial!")
            return

        print("I am a tutorial!")


class _tutorial:
    def __init__(self, context):
        self.context = context
        self.runner = Runner(context)

    def copy_resources(self, destination):
        """Copy the tutorial resources to the given destination."""
        logger.debug(f"Copying tutorial resources to: {destination}")
        os.makedirs(destination)

        def exclude_item(item, path):
            return any([item.startswith("."), "__" in item])

        for item in pkg_resources.resource_listdir("arlnuio.tutorial", "."):
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
