import collections
import logging
import os
import stat
import subprocess
import sys
import textwrap

import pkg_resources

logger = logging.getLogger(__name__)
Result = collections.namedtuple("Result", "rcode, stdout, stderr")


class LinuxRunner:
    """Responsible for running commands on linux systems."""

    def __init__(self, context):
        self.context = context

    def __call__(self, cmd, capture_output=False):

        params = {}

        if capture_output:
            params["stderr"] = subprocess.PIPE
            params["stdout"] = subprocess.PIPE

        cmdline = " ".join(cmd)
        logger.debug(f"Running command: {cmdline}")
        result = subprocess.run(cmd, **params)

        if capture_output:
            stdout = result.stdout.decode("utf-8")
            stderr = result.stderr.decode("utf-8")

            return Result(result.returncode, stdout, stderr)

    def _detect_terminal(self):
        """Determine which terminal the user is using."""
        logger.debug("Attempting to detect user's terminal")

        # Terminal detection is done using the bundled bash script `detect_terminal.sh`
        script = pkg_resources.resource_filename(
            "stylo.cli.scripts", "detect_terminal.sh"
        )

        result = self([script], capture_output=True)

        if result.rcode != 0:
            logger.debug("--> Unable to determine terminal")
            return None

        output = result.stdout.replace("\n", "")
        return output.split("\t")

    def _write_script(self, name, contents):
        """Write a script to a temporary location."""
        path = os.path.join(self.context.tmp_dir, name)
        logger.debug(f"Writing script: {path}")

        contents.insert(0, "#!/bin/bash")

        with open(path, "w") as f:

            for line in contents:
                logger.debug(textwrap.indent(line, "--> "))
                f.write(line + "\n")

        # Ensure that the file will be read/write/exec.
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
        return path

    def launch(self, cmds, quiet, oneshot):
        """Run commmands in a new window."""

        # This works by writing two scripts to a temporary location and executing
        # them.
        # - run.sh: Contains the commands that the user wants to run
        # - launch.sh: Runs the first script in a way that stops it from blocking the
        #              current terminal.
        name, path = self._detect_terminal()
        runpath = self._write_script("run.sh", cmds)

        launch_script = [f"{path} -e {runpath} &", "disown -h %%"]
        launchpath = self._write_script("launch.sh", launch_script)

        self([launchpath])


class Runner:
    """This is responsible for running commands across the various operating systems."""

    def __init__(self, context):

        if sys.platform == "linux":
            self.run = LinuxRunner(context)

    def launch(self, cmds, quiet=True, oneshot=True):
        """Run commands in a new window."""
        return self.run.launch(cmds, quiet, oneshot)
