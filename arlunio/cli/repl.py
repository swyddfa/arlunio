import logging
import subprocess
import sys

import arlunio.cli as cli

logger = logging.getLogger(__name__)


class Repl(cli.Command):
    """Launch an interactive prompt."""

    def run(self):
        subprocess.run([sys.executable])
