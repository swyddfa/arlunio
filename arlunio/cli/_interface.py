import argparse
import inspect
import logging

from typing import Any, Dict, List

import attr

logger = logging.getLogger(__name__)


def _build_bool_option(parameter: inspect.Parameter) -> Dict[str, Any]:
    """Provide the argparse options for a boolean option."""
    params = {"action": "store_false" if parameter.default is True else "store_true"}

    return params


def _build_float_option(parameter: inspect.Parameter) -> Dict[str, Any]:
    """Provide the argparse options for a float option."""
    params = {
        "type": float,
        "default": None if parameter.default == parameter.empty else parameter.default,
    }

    return params


def _build_int_option(parameter: inspect.Parameter) -> Dict[str, Any]:
    """Provides the argparse options for an integer option."""
    params = {
        "type": int,
        "default": None if parameter.default == parameter.empty else parameter.default,
    }

    return params


_STD_TYPES = {
    bool: _build_bool_option,
    float: _build_float_option,
    int: _build_int_option,
}


@attr.s(auto_attribs=True)
class CliOption:
    """Represents a command line option."""

    name: str
    """The name of the option."""

    description: str = None
    """Description about what the option controls."""

    args: Dict[str, Any] = attr.Factory(dict)
    """Extra arguments required to express this option in argparse."""

    @classmethod
    def fromparam(cls, parameter: inspect.Parameter):
        """Construct an instance of a cli option from a type annotation."""
        params = {"name": "--" + parameter.name.replace("_", "-")}
        builder = _STD_TYPES.get(parameter.annotation, None)

        if builder is None:
            raise TypeError(f"Unsupported cli option type: {parameter.annotation}")

        params["args"] = builder(parameter)
        return cls(**params)

    @classmethod
    def frommethod(cls, f):
        """Return a list of command line options, constructed from the given
        function."""
        options = []

        for param in inspect.signature(f).parameters.values():
            # Ignore the 'self' parameter in classes.
            if param.name == "self":
                continue

            options.append(cls.fromparam(param))

        return options


@attr.s(auto_attribs=True)
class CliCommand:
    """Class that represents a command on the command line."""

    name: str
    """The name of the command, this will be used to invoke it on the command line."""

    summary: str = None
    """Short, one line description of the command."""

    description: str = None
    """Extended, detailed description of the command and its options."""

    options: List[CliOption] = attr.Factory(list)
    """List of command line options, these will be exposed as flags on the command."""

    @classmethod
    def fromcmd(cls, name: str, cmd):
        """Create an instance of a command, based on a single command class."""

        if not hasattr(cmd, "run") or not callable(cmd.run):
            raise TypeError("Missing expected method: 'run'")

        docstring = inspect.getdoc(cmd)
        summary = "..." if docstring is None else docstring.split("\n")[0]

        params = {
            "name": name,
            "options": CliOption.frommethod(cmd.run),
            "summary": summary,
        }

        return cls(**params)


def build_command_parser(
    name: str, command, parent: argparse._SubParsersAction
) -> None:
    """Given a command defintion, define its command line interface.

    :param name: The name of the command, as it should be invoked from the command line.
    :param command: The class that defines the command's implementation.
    :param parent: The parent cli entity the command should hang off of.
    """
    cmd = CliCommand.fromcmd(name, command)
    parser = parent.add_parser(
        cmd.name, help=cmd.summary, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    names = []
    for option in cmd.options:
        names.append(option.name[2:])
        parser.add_argument(option.name, **option.args)

    def run(args: argparse.Namespace):
        params = {opt: getattr(args, opt) for opt in names}
        logger.debug("Parsed arguments: %s", params)

        instance = command()
        instance.run(**params)

    parser.set_defaults(run=run)
