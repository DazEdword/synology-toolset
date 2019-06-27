import logging

from models.base import Model
from settings import get_environmental_variable


class ConfigBase(Model):
    """Model subclass that populates attributes via config file."""

    _config_prefix = None

    def __init__(self):
        if not self._config_prefix:
            logging.warning(
                f"A config prefix is required to instance {self.__class__.__name__}"
            )
            return

        for field in self.FIELDS:
            setattr(self, field, self.get_field_from_config(self._config_prefix, field))

    def get_field_from_config(self, config_prefix, field):
        return get_environmental_variable(f"{config_prefix}_{field.upper()}")
