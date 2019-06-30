# import inspect
import logging

from copy import deepcopy

from synotools.models.config.base import ConfigBase

# log_file = "./logfile.log"
log_level = logging.INFO


class PasswordMaskingFilter(logging.Filter):
    """Demonstrate how to filter sensitive data:"""

    def filter(self, record):
        if isinstance(record.args, ConfigBase):
            record.args = PasswordMaskingFilter.sanitize_config(record.args)

        return True

    @staticmethod
    def sanitize_config(config):
        if not isinstance(config, ConfigBase):
            return config

        config_copy = deepcopy(config)

        try:
            # This is done in two steps to avoid setting password
            # values to config objects that do not have one
            password_value = config_copy.password
            config_copy.password = "********"
        except (AttributeError, NameError):
            pass

        return config_copy


def get_logger(module_name):
    logging.basicConfig(level=log_level, filemode="w+")

    logger = logging.getLogger(module_name)
    logger.addFilter(PasswordMaskingFilter())

    return logger
