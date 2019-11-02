import logging
import subprocess
import sys

logger = logging.getLogger(__name__)


class Repl:
    """Launch an interactive prompt."""

    def run(self):
        subprocess.run([sys.executable])
