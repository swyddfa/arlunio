import inspect

from typing import List

import py.test

from arlunio.cli._interface import CliCommand, CliOption


def mkparam(name, type_, default=None):
    """Construct parameter instances for test purposes."""
    pos = inspect.Parameter.POSITIONAL_OR_KEYWORD
    value = default if default is not None else inspect.Parameter.empty

    return inspect.Parameter(name, pos, default=value, annotation=type_)


BOOL_STORE_TRUE = {"action": "store_true"}
BOOL_STORE_FALSE = {"action": "store_false"}
INT_NO_DEFAULT = {"type": int, "default": None}
INT_WITH_DEFAULT = lambda v: {"type": int, "default": v}  # noqa: E731
FLOAT_NO_DEFAULT = {"type": float, "default": None}
FLOAT_WITH_DEFAULT = lambda v: {"type": float, "default": v}  # noqa: E731


@py.test.mark.parametrize(
    "parameter,expected",
    [
        (mkparam("reset", bool), CliOption(name="--reset", args=BOOL_STORE_TRUE)),
        (mkparam("num_cats", int), CliOption("--num-cats", args=INT_NO_DEFAULT)),
        (mkparam("radius", float), CliOption("--radius", args=FLOAT_NO_DEFAULT)),
        (
            mkparam("reset", bool, default=False),
            CliOption("--reset", args=BOOL_STORE_TRUE),
        ),
        (
            mkparam("reset", bool, default=True),
            CliOption("--reset", args=BOOL_STORE_FALSE),
        ),
        (
            mkparam("num_cats", int, default=12),
            CliOption("--num-cats", args=INT_WITH_DEFAULT(12)),
        ),
        (
            mkparam("radius", float, default=3.14),
            CliOption(name="--radius", args=FLOAT_WITH_DEFAULT(3.14)),
        ),
    ],
)
def test_cli_option_from_std_types(parameter, expected):
    """Ensure we can construct a CliOption based on the information we get
    from type annotations for standard types."""

    opt = CliOption.fromparam(parameter)
    assert opt == expected


def test_cli_option_unexpected_type():
    """Ensure that we raise an appropriate exception if we are given a type
    we cannot handle."""

    with py.test.raises(TypeError) as err:
        param = mkparam("collection", List[int])
        CliOption.fromparam(param)

    assert "Unsupported cli option type" in str(err.value)
    assert "List" in str(err.value)


def simple_func(x: int, y: float = 0.5):
    pass


def class_method(self, reset: bool, num_cats: int = 3):
    pass


@py.test.mark.parametrize(
    "method,expected",
    [
        (
            simple_func,
            [
                CliOption(name="--x", args=INT_NO_DEFAULT),
                CliOption(name="--y", args=FLOAT_WITH_DEFAULT(0.5)),
            ],
        ),
        (
            class_method,
            [
                CliOption(name="--reset", args=BOOL_STORE_TRUE),
                CliOption(name="--num-cats", args=INT_WITH_DEFAULT(3)),
            ],
        ),
    ],
)
def test_cli_option_from_method(method, expected):
    """Ensure we can construct a list of CliOptions from a given method."""

    opts = CliOption.frommethod(method)
    assert opts == expected


def test_single_cmd_no_run_method():
    """Ensure we raise an appropriate error when given a class with no run method."""

    class BadCommand:
        pass

    with py.test.raises(TypeError) as err:
        CliCommand.fromcmd("test", BadCommand)

    assert "Missing expected method" in str(err.value)
    assert "run" in str(err.value)


def test_single_cmd_run_attribute():
    """Ensure we raise an appropriate error when given a class whose 'run' attribure is
    not callable"""

    class BadCommand:
        run = 23

    with py.test.raises(TypeError) as err:
        CliCommand.fromcmd("test", BadCommand)

    assert "Missing expected method" in str(err.value)
    assert "run" in str(err.value)


class AddCommand:
    """A single line summary.

    Further information on usage follows
    """

    def run(self, x: int, y: int = 1):
        pass


ADD_COMMAND = CliCommand(
    name="test",
    summary="A single line summary.",
    options=[
        CliOption(name="--x", args=INT_NO_DEFAULT),
        CliOption(name="--y", args=INT_WITH_DEFAULT(1)),
    ],
)


@py.test.mark.parametrize("definition,expected", [(AddCommand, ADD_COMMAND)])
def test_single_cmd(definition, expected):
    """Ensure we can construct appropriate command defintions from a given class"""

    cmd = CliCommand.fromcmd("test", definition)
    assert cmd == expected
