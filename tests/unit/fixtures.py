from unittest.mock import Mock

from synotools.models.config.syno import SynoConfig


def create_syno_config_mock():
    """Mock of the class"""
    config_mock = Mock()
    config_mock.FIELDS = ["username", "password", "port", "ip"]

    config_mock.username = "user_mock"
    config_mock.password = "password_mock"
    config_mock.port = "9999"
    config_mock.ip = "host_mock"

    return config_mock


def create_syno_config_fake():
    """Instance of the class, but with fake values.
    It is .env independent"""
    config_fake = SynoConfig(
        username="user_mock",
        password="password_mock",
        port=9999,
        ip="host_mock",
    )

    return config_fake


def create_deluge_config_mock():
    config_mock = Mock()
    config_mock.FIELDS = ["username", "password", "port", "ip"]

    config_mock.username = "deluge_user_mock"
    config_mock.password = "deluge_password_mock"
    config_mock.port = "8888"
    config_mock.ip = "deluge_service_host_mock"

    return config_mock
