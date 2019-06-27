from unittest.mock import Mock


def create_syno_config_mock():
    config_mock = Mock()
    config_mock.FIELDS = ["username", "password", "port", "ip"]

    config_mock.username = "user_mock"
    config_mock.password = "password_mock"
    config_mock.port = "9999"
    config_mock.ip = "host_mock"

    return config_mock
