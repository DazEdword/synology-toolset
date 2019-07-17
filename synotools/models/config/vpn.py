from synotools.models.config import ConfigBase


class VpnConfig(ConfigBase):
    id: str = None
    name: str = None
    protocol: str = None

    _config_prefix = "VPN"
