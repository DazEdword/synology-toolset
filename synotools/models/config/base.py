import logging

from synotools.models.base import Model
from synotools.settings import Settings


class ConfigBase(Model):
    """Model subclass that populates attributes via config file."""

    _config_prefix = None
    _settings = Settings()

    def __init__(self, **data):
        # If no keys are passed, values for fields will be taken from .env
        if not data:
            if not self._config_prefix:
                logging.warning(
                    f"A config prefix is required to instance {self.__class__.__name__}"
                )
                return

            data = {}
            for field in self.FIELDS:
                data[field] = self.get_field_from_config(self._config_prefix, field)

        super().__init__(**data)

    def get_field_from_config(self, config_prefix, field):
        return self._settings.get_environmental_variable(
            f"{config_prefix}_{field.upper()}"
        )
