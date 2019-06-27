from models.config.base import ConfigBase


class Syno(ConfigBase):
    username: str = None
    password: str = None
    port: str = None
    ip: str = None

    _config_prefix = "SYNOLOGY"