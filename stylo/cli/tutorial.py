import logging


logger = logging.getLogger(__name__)


class Tutorial:
    def __init__(self, context):
        self.context = context

    def launch(self):
        logger.debug("Launching the tutorial." "")


def register(cli, click):
    """Here we expose our command line interface."""

    @cli.command()
    @click.pass_obj
    def tutorial(context):
        """Launch the tutorial."""

        tutorial = Tutorial(context)
        tutorial.launch()
