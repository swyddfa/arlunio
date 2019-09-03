import argparse
import inspect
import logging
import re
import typing as t

import attr

logger = logging.getLogger(__name__)


class Command:
    """A command on the command line."""


@attr.s(auto_attribs=True)
class _cliOption:
    """Class that represents a cli option and relevant parameters."""

    name: str
    description: str = None
    argparse_args: t.Dict[str, t.Any] = attr.Factory(dict)

    @classmethod
    def from_parameter(cls, parameter: inspect.Parameter):
        params = {"name": "--" + parameter.name}
        argparse_args = {}

        if parameter.annotation == bool:
            if parameter.default:
                argparse_args["action"] = "store_false"
            else:
                argparse_args["action"] = "store_true"

        else:
            argparse_args["default"] = parameter.default
            argparse_args["type"] = parameter.annotation

        params["argparse_args"] = argparse_args
        return cls(**params)


def parse_options(method: callable) -> t.Dict[str, _cliOption]:
    """Given a method that implements a command, extract the information required to
    expose its arguments on the command line."""

    options = {}

    for param in inspect.signature(method).parameters.values():

        if param.name == "self":
            continue

        options[param.name] = _cliOption.from_parameter(param)

    return options


@attr.s(auto_attribs=True)
class _cliCommand:
    """Class that represents a command in a way that makes it easy for us to
    generate the command line interface from it."""

    name: str
    """The name of the command, as exposed on the command line."""

    summary: str = None
    """A short description of the command, as shown in the command list."""

    description: str = None
    """A more detailed description of the command, as shown in its dedicated
    help text"""

    options: t.List[_cliOption] = attr.Factory(list)
    """A list of command line options, with the information required to expose them
    via argparse."""

    @classmethod
    def from_command(cls, name: str, cmd: Command):
        # It 'works', it's not pretty, I don't like it
        params = {"name": name, "options": parse_options(getattr(cmd, "run"))}
        docstring = inspect.getdoc(cmd)

        param_tag = re.compile(":param ([a-zA-Z0-9_]+): ?([\\s\\w><.]+):?")

        try:

            summary_end = docstring.index("\n\n")
        except ValueError:
            params["summary"] = docstring
            params["options"] = list(params["options"].values())
            return cls(**params)

        params["summary"] = docstring[:summary_end]

        # Take into account the fact that index returns the index at the
        # start of the '\n\n' patternd
        description_start = summary_end
        next_parameter = param_tag.search(docstring[description_start:])

        if next_parameter is None:
            description = docstring[description_start:]
            params["description"] = description.lstrip().rstrip()
            params["options"] = list(params["options"].values())
            return cls(**params)

        description_end = description_start + next_parameter.span()[0]
        params["description"] = (
            docstring[description_start:description_end].rstrip().lstrip()
        )
        start = description_start

        while next_parameter is not None:
            name, helptext = next_parameter.groups()

            # Clean the text
            helptext = helptext.replace("\n", "")
            helptext = re.sub("[ ]+", " ", helptext)
            params["options"][name].description = helptext

            start += next_parameter.span()[1] - 1
            next_parameter = param_tag.search(docstring[start - 1 :])

        params["options"] = list(params["options"].values())
        return cls(**params)


def construct_parser(
    name: str, cmd: Command, subparser: argparse._SubParsersAction
) -> None:

    """Given a command instance and an argument parser, constuct the command line
    interface.

    :param name: The name of the command as it should be exposed on the command line.
    :param cmd: The class that represents the implementation of the command
    :param subparser: The subparsers object we can use to create our command with.
    """

    command = _cliCommand.from_command(name, cmd)
    parser = subparser.add_parser(
        command.name,
        help=command.summary,
        description=command.description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    option_names = [opt.name[2:] for opt in command.options]

    for option in command.options:
        parser.add_argument(
            option.name, help=option.description, **option.argparse_args
        )

    def run(args: argparse.Namespace):
        params = {opt: getattr(args, opt) for opt in option_names}
        logger.debug(f"Parsed arguments: {params}")

        command = cmd()
        command.run(**params)

    parser.set_defaults(run=run)
