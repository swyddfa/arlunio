import textwrap

from arlunio.cli import Command, _cliCommand, _cliOption


class CommandSummaryOnly(Command):
    """This is an example command."""

    def run(self, reset: bool = False, verbose: bool = True, count: int = 1):
        pass


class CommandWithNoParams(Command):
    """This is an example command.

    Commands can contain an extended description that explains what the command
    does, how to invoke it as well as any gotchas or noteable command line
    arguments.
    """

    def run(self, reset: bool = False, verbose: bool = True, count: int = 1):
        pass


class CommandWithParams(Command):
    """This is an example command.

    Commands can contain an extended description that explains what the command
    does, how to invoke it as well as any gotchas or noteable command line
    arguments.

    :param rEset: Reset the thing back to its default state
    :param verbo3e: Use this if you want to gain further insight into what is
                    happening with the steps.
    :param num_tri8s:Repeat the command <N> times.

    """

    def run(self, rEset: bool = False, verbo3e: bool = True, num_tri8s: int = 1):
        pass


class TestCliCommand:
    """Tests for our docstring parsing function."""

    def test_construct_only_summary(self):
        """Ensure that we can parse the relevant information from a command that only
        provides a summary."""

        command = _cliCommand.from_command("example", CommandSummaryOnly)

        assert command.name == "example"
        assert command.summary == "This is an example command."
        assert command.description is None

        expected_options = {
            "--reset": _cliOption(
                name="--reset", argparse_args={"action": "store_true"}
            ),
            "--verbose": _cliOption(
                name="--verbose", argparse_args={"action": "store_false"}
            ),
            "--count": _cliOption(
                name="--count", argparse_args={"default": 1, "type": int}
            ),
        }

        actual_options = {opt.name: opt for opt in command.options}
        assert actual_options == expected_options

    def test_construct_with_description(self):
        """Ensure that we can parse the relevant information from a command that only
        gives a description."""

        command = _cliCommand.from_command("example", CommandWithNoParams)

        assert command.name == "example"
        assert command.summary == "This is an example command."

        expected_description = """\
        Commands can contain an extended description that explains what the command
        does, how to invoke it as well as any gotchas or noteable command line
        arguments."""

        assert command.description == textwrap.dedent(expected_description)

        expected_options = {
            "--reset": _cliOption(
                name="--reset", argparse_args={"action": "store_true"}
            ),
            "--verbose": _cliOption(
                name="--verbose", argparse_args={"action": "store_false"}
            ),
            "--count": _cliOption(
                name="--count", argparse_args={"default": 1, "type": int}
            ),
        }

        actual_options = {opt.name: opt for opt in command.options}
        assert actual_options == expected_options

    def test_contruct_full_command(self):
        """Ensure that we can parse the relevant information from a "full" command
        definition."""

        command = _cliCommand.from_command("example", CommandWithParams)

        assert command.name == "example"
        assert command.summary == "This is an example command."

        expected_description = """\
        Commands can contain an extended description that explains what the command
        does, how to invoke it as well as any gotchas or noteable command line
        arguments."""

        assert command.description == textwrap.dedent(expected_description)
        actual_options = {opt.name: opt for opt in command.options}

        expected_options = {
            "--rEset": _cliOption(
                name="--rEset",
                argparse_args={"action": "store_true"},
                description="Reset the thing back to its default state",
            ),
            "--verbo3e": _cliOption(
                name="--verbo3e",
                argparse_args={"action": "store_false"},
                description=(
                    "Use this if you want to gain further insight into what"
                    " is happening with the steps."
                ),
            ),
            "--num_tri8s": _cliOption(
                name="--num_tri8s",
                argparse_args={"default": 1, "type": int},
                description="Repeat the command <N> times.",
            ),
        }
        assert actual_options == expected_options
