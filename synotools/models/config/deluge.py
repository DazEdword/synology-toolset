from synotools.models.config import ConfigBase


class DelugeConfig(ConfigBase):
    username: str = None
    password: str = None
    port: str = None
    ip: str = None

    _config_prefix = "DELUGE"
