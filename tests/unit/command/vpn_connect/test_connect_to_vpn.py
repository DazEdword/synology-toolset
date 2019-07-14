from unittest.mock import patch

from synotools.commands.vpn_connect import connect_to_vpn
from tests.unit.fixtures import create_syno_config_mock


@patch("synotools.commands.vpn_connect.Connection")
@patch("synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock())
def test_gets_synology_config_details(syno_config_mock, deluge_config_mock, *_):
    connect_to_vpn()
    syno_config_mock.assert_called_once()


@patch("synotools.commands.vpn_connect.get_logger")
@patch("synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.Connection")
def test_creates_fabric_connection_with_correct_sudo_config(
    connection_mock, config_mock, *_
):
    connect_to_vpn()

    config_mock.assert_called_once_with(
        overrides={"sudo": {"password": "password_mock"}}
    )


@patch("synotools.commands.vpn_connect.logger")
@patch("synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.Connection")
def test_creates_fabric_connection_with_correct_credentials(
    connection_mock, config_mock, *_
):
    connect_to_vpn()

    connection_mock.assert_called_once_with(
        host="host_mock", user="user_mock", config=config_mock.return_value
    )


@patch("synotools.commands.vpn_connect.logger")
@patch("synotools.commands.vpn_connect.SynoConfig", return_value=create_syno_config_mock())
@patch("synotools.commands.vpn_connect.Config")
@patch("synotools.commands.vpn_connect.is_vpn_enabled")
@patch("synotools.commands.vpn_connect.Connection")
def test_checks_whether_vpn_connection_is_already_being_used(
    connection_mock, is_vpn_enabled_mock, *_
):
    connection_mock.return_value.stdout = "Command output."
    connect_to_vpn()

    is_vpn_enabled_mock.assert_called_once_with(connection_mock.return_value)
