import logging
import os
import pkg_resources
import shutil
import subprocess

logger = logging.getLogger(__name__)


class Tutorial:
    def __init__(self, context):
        self.context = context

    def copy_resources(self, destination):
        """Copy the tutorial resources to the given destination."""
        logger.debug(f"Copying tutorial resources to: {destination}")

        def exclude_item(item, path):
            return any([not os.path.isdir(path), item.startswith("."), "__" in item])

        for item in pkg_resources.resource_listdir("stylo.tutorial", "."):
            path = pkg_resources.resource_filename("stylo.tutorial", item)

            if exclude_item(item, path):
                logger.debug(f"--> {item}, skipping")
                continue

            logger.debug(f"--> {item}")
            dest = os.path.join(destination, item)
            shutil.copytree(path, dest, copy_function=shutil.copy)

    def launch(self):
        """Launch a jupyter lab instance in the tutorial directory."""

        tutorial_dir = os.path.join(self.context.cache_dir, "tutorial")

        if not os.path.exists(tutorial_dir):
            logger.debug(f"Tutorial content does not exist")
            self.copy_resources(tutorial_dir)


def register(cli, click):
    """Here we expose our command line interface."""

    @cli.command()
    @click.pass_obj
    def tutorial(context):
        """Launch the tutorial."""

        tutorial = Tutorial(context)
        tutorial.launch()
