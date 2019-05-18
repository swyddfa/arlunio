import enum
import logging
import pkg_resources

logger = logging.getLogger(__name__)


def load_parameters():
    """Load all of the available parameters."""
    logger.debug("Loading parameters")

    parameters = []

    for parameter in pkg_resources.iter_entry_points("stylo.parameters"):
        logger.debug("Loading parameter: {}".format(parameter.name))
        parameters.append((parameter.name, parameter.load()))

    return enum.Enum("Parameters", parameters)
